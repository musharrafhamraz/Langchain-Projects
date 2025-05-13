from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_groq import ChatGroq


class WebRag:
    def __init__(self, product_data):
        load_dotenv()
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        # LangChain-compatible Groq LLM
        self.llm_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama3-70b-8192"  # Update to match correct Groq model
        )

        # Text Embedding and Splitting
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        self.str_parser = StrOutputParser()

        # Prepare documents for vector store
        text_blocks = [p['description'] + " " + str(p['specifications']) + " " + str(p['price']) for p in product_data]
        docs = self.splitter.create_documents(text_blocks)
        self.vector_store = FAISS.from_documents(docs, self.embedding_model)
        self.retriever = self.vector_store.as_retriever(search_type='similarity', search_kwargs={"k": 5})

        # Prompt
        self.prompt = PromptTemplate(
            template="""
                You are a helpful assistant.
                Only answer from the provided context.
                If there's insufficient context, say: "I can't answer what you asked."

                Context:
                {context}

                Question:
                {question}
                """,
            input_variables=["context", "question"]
        )

        # Chain definition
        # self.chain = (
        #     {"context": self.retriever, "question": RunnablePassthrough()}
        #     | self.prompt
        #     | self.llm_model
        #     | self.str_parser
        # )
        self.chain = (
    {
        "context": RunnableLambda(lambda x: self.retriever.invoke(x["question"])),
        "question": RunnableLambda(lambda x: x["question"]),
    }
    | self.prompt
    | self.llm_model
    | self.str_parser
)

    def query(self, question: str):
        print(f"Running query for: {question}")
        return self.chain.invoke({"question": question})
