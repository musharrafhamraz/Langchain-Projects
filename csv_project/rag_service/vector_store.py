from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import os

class VectorStoreManager:
    def __init__(self, embedding_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vector_store = None

    def create_vector_store(self, chunks):
        """Create FAISS vector store from document chunks"""
        self.vector_store = FAISS.from_documents(chunks, self.embedding_model)
        return self.vector_store

    def get_retriever(self, k=4):
        """Get retriever from vector store"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        return self.vector_store.as_retriever(search_kwargs={"k": k})