from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import pandas as pd
import os
from dotenv import load_dotenv

class Analysis:
    """ 
    Analyze telemetry data based on Formula SAE Guidelines
    """

    def __init__(self, pdf_dictionary="../data/training"):
        """ 
        Initialize elements to use for analysis
        """
        load_dotenv()
        self.llm = OpenAI(temperature=0)
        self.pdf_dictionary = pdf_dictionary
        self.knowledge_base = self._create_knowledge_base()
    
    def _create_knowledge_base(self):
        """ 
        Create knowledge base from PDF files
        """
        documents = []

        # load all pdfs in the directory
        for file in os.listdir(self.pdf_dictionary):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(self.pdf_dictionary, file))
                documents.extend(loader.load())
        
        # split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # create embeddings
        # used for similarity search to extract relevant information
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(texts, embeddings)

    def analyze_telemetry(self, df: pd.DataFrame):
        """ 
        Analyze telemetry data using the knowledge base
        """
        # create a retrieval chain
        # pipeline used to query the knowledge base
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm, # response generation
            chain_type="stuff", # use the document as context
            retriever=self.knowledge_base.as_retriever() # retrieves elements from knowledge base
        )

        # convert data
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
        # ex: Telemetry data for period 1 to 10
        summary = f"Telemetry data for period {df['period'].iloc[0]} to {df['period'].iloc[-1]}\n\n"

        # add a summary for each column
        for column in ['motorSPD', 'motorTEMP', 'packVOLT', 'packTEMP', 'packCURR', 'packCCL']:
            summary += f"{column}:\n"
            summary += f" - Range: {df[column].min()} to {df[column].max()}\n"
            summary += f" - Average: {df[column].mean():.2f}\n"

        return summary

