from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

class Analysis:
    """ 
    Analyze telemetry data based on Formula SAE Guidelines
    """

    def __init__(self, pdf_directory=None):
        """ 
        Initialize elements to use for analysis
        """
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
        # Use absolute path for PDF directory
        if pdf_directory is None:
            pdf_directory = os.path.abspath(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'data',
                'training'
            ))
        
        self.pdf_directory = pdf_directory
        # raise error if pdf directory does not exist
        if not os.path.exists(self.pdf_directory):
            os.makedirs(self.pdf_directory)
            raise ValueError(f"Created PDF directory at {self.pdf_directory}. Please add PDF files before analyzing.")
            
        # Verify PDF files exist
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        
        # raise error if no pdf files are found
        if not pdf_files:
            raise ValueError(f"No PDF files found in {self.pdf_directory}. Directory exists but is empty.")
        
        self.llm = OpenAI(
            temperature=0,
            openai_api_key=api_key
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
        
    def _preprocess_data(self, df):
        """ 
        Convert timestamps to a datatime object
        """
        # convert the timestamp column in the dataframe to a timestamp object
        df['date'] = df['timestamp'].apply(lambda x: self._parse_timestamp(x, 'date'))
        df['time'] = df['timestamp'].apply(lambda x: self._parse_timestamp(x, 'time'))
        df.drop(columns=['timestamp'], inplace=True)

        # reorder columns
        columns = ['date', 'time'] + [col for col in df.columns 
                                    if col not in ['date', 'time', 'timestamp']]
        # return the final dataframe
        return df[columns]
    
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

    def analyze_telemetry(self, df: pd.DataFrame):
        """ 
        Analyze telemetry data using the knowledge base
        """
        # Preprocess the data first
        df = self._preprocess_data(df)
        
        # Create retrieval chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm, # response generation
            chain_type="stuff", # use the document as context
            retriever=self.knowledge_base.as_retriever() # retrieves elements from knowledge base
        )

        # Format data for analysis
        data_description = self._format_data_for_analysis(df)

        # generate prompt
        prompt = f"""
        You are an expert in Formula SAE telemetry data and analysis of electric race cars.
        You will analyze telemetry data based on the provided guidelines:
        {data_description}

        Identify any values that are:
        1. Outside of the safe operating ranges
        2. Showing concerning trends or patterns of behavior over time
        3. Requiring immediate attention

        Format the response a concise, short structured analysis with clear recommendations. 
        Assume that the driver will be referencing this analysis during a live race and need to 
        make decisions within within minutes. The information should be concise and easy to digest.
        """

        # run the chain
        result = qa_chain.run(prompt)
        return result

    def _format_data_for_analysis(self, df: pd.DataFrame):
        """
        Format DataFrame into a string for analysis
        """
        # Create summary of the data
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
