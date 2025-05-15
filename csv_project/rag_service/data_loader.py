from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

class CSVDataLoader:
    def __init__(self, chunk_size=250, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def load_and_split(self, file_path):
        """Load CSV file and split into chunks"""
        # Create a temporary file path if needed
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        loader = CSVLoader(file_path=file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        print(f"Loaded {len(documents)} documents and split into {len(chunks)} chunks.")
        return chunks