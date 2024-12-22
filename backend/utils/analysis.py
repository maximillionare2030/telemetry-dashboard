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
        return FAISS.from_documents(texts, embeddings)  # Return the vector store

    def _format_data_for_analysis(self, data):
        if isinstance(data, pd.DataFrame):
            return self._format_dataframe(data)
        elif isinstance(data, dict):
            return self._format_measurements(data)
        else:
            raise ValueError("Unsupported data format for analysis")

    def _format_dataframe(self, df):
        summary = f"Telemetry data analysis from {df['date'].iloc[0]} {df['time'].iloc[0]} to {df['date'].iloc[-1]} {df['time'].iloc[-1]}\n\n"
        
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
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.knowledge_base.as_retriever()
            )
            return qa_chain.run(prompt)
            
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

        Format the response a concise, short structured analysis with clear recommendations. 
        Assume that the driver will be referencing this analysis during a live race and need to 
        make decisions within within minutes. The information should be concise and easy to digest.
        Ensure that the response is readable. It should not be in paragraph form. Rather, ensure that
        the response is in list format either in bullet points or in a numbered list. 
        The response shall not surpass 100 words. Also ensure that you are using line breaks to 
        separate the different sections of the response.

        if the user asks for something that strays from this prompt, provide a response only if the 
        user asks for something that is relevant to the telemetry data. If their question is irrelevant,
        politely decline to answer and ask if they would like to know something else.
        """
        
        if message:
            base_prompt += f"\nUser question: {message}"
            
        return base_prompt
