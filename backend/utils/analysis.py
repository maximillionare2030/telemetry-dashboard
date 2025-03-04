from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from client.influxv1 import InfluxDBHandler
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class Analysis:
    """ 
    Analyze telemetry data based on Formula SAE Guidelines
    """

    def __init__(self):
        """ 
        Initialize elements to use for analysis
        """
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.llm = OpenAI(temperature=0)
        self.pdf_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'training')
        
        # initialize influxdb client
        self.influx = InfluxDBHandler(
            host='localhost',
            port=8086,
            database='telemetry'
        )
        
        self.knowledge_base = self._create_knowledge_base()
    
    def _parse_timestamp(self, timestamp_str, return_type):
        """ 
        Parse timestamp based on the return type
        """
        # format timestamp to remove the 'Z'
        timestamp_str = timestamp_str.replace('000Z', '')
        dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
        
        if return_type == 'date':
            return dt.strftime('%Y-%m-%d')
        elif return_type == 'time':
            return dt.strftime('%H:%M:%S')
        else:
            raise ValueError(f"Invalid return type: {return_type}")
    
    def _create_knowledge_base(self):
        """ 
        Create knowledge base from PDF files
        """
        documents = []

        # load all pdfs in the directory
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {self.pdf_directory}")
            
        for file in pdf_files:
            loader = PyPDFLoader(os.path.join(self.pdf_directory, file))
            documents.extend(loader.load())
        
        # split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # create embeddings
        # used for similarity search to extract relevant information
        embeddings = OpenAIEmbeddings()
        # store information as a searchable vector database
        return FAISS.from_documents(texts, embeddings) 

    def _format_data_for_analysis(self, data):
        if isinstance(data, pd.DataFrame):
            return self._format_dataframe(data)
        elif isinstance(data, dict):
            return self._format_measurements(data)
        else:
            raise ValueError("Unsupported data format for analysis")

    def _format_dataframe(self, df):
        summary = f"Telemetry data analysis from {df['date'].iloc[0]} {df['time'].iloc[0]} to {df['date'].iloc[-1]} {df['time'].iloc[-1]}\n\n"
        
        # Add statistics for each telemetry metric
        metrics = ['motorSPD', 'motorTEMP', 'packVOLT', 'packTEMP', 'packCURR', 'packCCL']
        for metric in metrics:
            if metric in df.columns:
                summary += f"{metric}:\n"
                summary += f"  Min: {df[metric].min()}\n"
                summary += f"  Max: {df[metric].max()}\n"
                summary += f"  Average: {df[metric].mean():.2f}\n"
                summary += f"  Latest Value: {df[metric].iloc[-1]}\n\n"
        
        return summary

    def _format_measurements(self, all_data):
        return "\n".join([
            f"{measurement}: {len(points)} points" 
            for measurement, points in all_data.items()
        ])

    async def analyze_data(self, message: str = None):
        try:
            # Get measurements and their data points
            measurements = self.influx.get_measurements()
            if not measurements:
                return "No measurements found in the database. Please upload data first."
            
            # Collect data points from all measurements
            all_data = {}
            for measurement in measurements:
                points = self.influx.get_points(measurement)
                if points:
                    all_data[measurement] = points
            
            if not all_data:
                return "No data points found in measurements."
            
            data_summary = self._format_data_for_analysis(all_data)
            prompt = self._create_analysis_prompt(data_summary, message)

            # Get relevant sources and run analysis first
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.knowledge_base.as_retriever(),
                return_source_documents=True 
            )
            
            try:
                # run the analysis
                chain_response = qa_chain.invoke(prompt)
                analysis = chain_response["result"]
                source_docs = chain_response.get("source_documents", [])
                
                if not source_docs:
                    logger.warning("No source documents returned from QA chain")
                
                # Format sources with content actually used in analysis
                sources = []
                for doc in source_docs:
                    # Clean the content by removing empty lines and headers/footers
                    content_lines = doc.page_content.split('\n')
                    cleaned_lines = []
                    
                    # remove empty lines and headers/footers
                    for line in content_lines:
                        line = line.strip()
                        # Skip empty lines and headers/footers
                        if (not line or 
                            "Formula SAE® Rules" in line or 
                            "© 2024" in line or
                            line.startswith("Page") or
                            len(line) < 20):
                            continue
                        cleaned_lines.append(line)
                    
                    # Find lines that appear in the analysis
                    relevant_lines = []

                    # break up analysis into sentences
                    analysis_sentences = [s.strip() for s in analysis.split('.') if s.strip()]
                    
                    # extract relevant line segments from the lines
                    for line in cleaned_lines:
                        # Check if any part of the line is used in any analysis sentence
                        for sentence in analysis_sentences:
                            # Look for any part of the line that is in the analysis sentence
                            if any(
                                segment in sentence 
                                for segment in [line[i:i+10] # check if part of line matches segment
                                for i in range(len(line)-9)]
                                if len(segment) >= 10 # check if segment is at least 10 characters long
                            ):
                                # if a line matches a sentence, add it to the relevant lines
                                relevant_lines.append(line)
                                logger.info(f"Found relevant line: {line[:40]}...")
                                break
                    
                    # if relevant lines are found, add them to the sources
                    if relevant_lines:
                        sources.append({
                            "title": os.path.basename(doc.metadata['source']),
                            "content": f"{relevant_lines[0][:40]}..." if len(relevant_lines[0]) > 40 else relevant_lines[0],
                            "page": f"Page {doc.metadata['page']}"
                        })
                
                if not sources:
                    logger.warning("No relevant sources found for the analysis")
                    sources = [{
                        "title": "Note",
                        "content": "No specific rule references found",
                        "page": "N/A"
                    }]
                
                return {
                    "analysis": analysis,
                    "sources": sources
                }
                
            except Exception as e:
                logger.error(f"Error processing sources: {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error extracting relevant content: {str(e)}"
                )
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def _create_analysis_prompt(self, data_summary, message=None):
        base_prompt = prompt = f"""
        You are an expert in Formula SAE telemetry data and analysis of electric race cars.
        You will analyze telemetry data stored inside of the influxdb database based on the provided guidelines:
        {data_summary}

        Identify any values that are:
        1. Outside of the safe operating ranges
        2. Showing concerning trends or patterns of behavior over time
        3. Requiring immediate attention

        Formatting Rules: Format the response a concise, short structured analysis with clear recommendations. 
        Assume that the driver will be referencing this analysis during a live race and need to 
        make decisions within within minutes. The information should be concise and easy to digest.
        Ensure that the response is readable. Only the first 1-3 sentences should be in paragraph form
        and should summarize the analysis. The next parts of the response should ONLY be in listed format,
        ensure that the response is in list format either in bullet points or in a numbered list. 
        The response shall not surpass 100 words. Also ensure that you are using line breaks to 
        separate the different sections of the response.

        Context: Assume that the context is that an experienced engineer is reviewing data after a race and wants to 
        know what parts of the vehicle they need to fix for the next race. Assume that there is a time constraint
        and they need to make decisions quickly. Make the recommendations extremely clear and non-generic. After 
        reading the response, the engineer should be able to know exactly what parts of the vehicle they need to 
        fix and how to fix them. Ensure that the formatting follows the rules under "Formatting Rules".

        if the user asks for something that strays from this prompt, provide a response only if the 
        user asks for something that is relevant to the telemetry data. If their question is irrelevant,
        politely decline to answer and ask if they would like to know something else.
        """
        
        if message:
            base_prompt += f"\nUser question: {message}"
            
        return base_prompt

    def analyze_nominal_ranges(self, metrics_data):
        """ 
        Analyze if a metric is outside of a nominal range
        Nominal ranges pulled from the FSAE handbook
        """
        nominal_ranges = {
            'Motor speed': {'min': 1500, 'max': 8500},  # Updated based on operational tolerances for typical motors
            'Motor temp': {'min': 10, 'max': 90},       # Reflecting enhanced thermal management requirements
            'Pack voltage': {'min': 250, 'max': 600},   # Aligning with the maximum permissible voltage of 600 V DC :contentReference[oaicite:0]{index=0}
            'Pack temp': {'min': 10, 'max': 60},        # Maximum accumulator cell temperature is capped at 60°C :contentReference[oaicite:1]{index=1}
            'Pack current': {'min': -120, 'max': 250},  # Adjusted to accommodate peak currents during dynamic events
            'Pack ccl': {'min': 0, 'max': 120}          # Charge current limits considering cell and safety constraints
        }

        analysis = {}

        # analyze each metric inside of the metrics_data list
        for metric, value in metrics_data.items():
            if metric in nominal_ranges:
                if value < nominal_ranges[metric]['min']:
                    analysis[metric] = 'below' # tag with the status
                elif value > nominal_ranges[metric]['max']:
                    analysis[metric] = 'above' # tag with the status
                else:
                    analysis[metric] = 'nominal' # tag with the status

        return analysis
