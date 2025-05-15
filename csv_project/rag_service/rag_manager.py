from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

class RAGManager:
    def __init__(self, retriever):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.retriever = retriever
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama3-70b-8192"
        )
        self.setup_chain()

    def setup_chain(self):
        """Setup RAG chain"""
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, question):
        """Query the RAG system"""
        return self.rag_chain.invoke(question)