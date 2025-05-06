from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings

class RAGService:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    def create_pipeline(self, text: str):
        """Create RAG pipeline from text"""
        chunks = self.text_splitter.create_documents([text])
        vector_store = FAISS.from_documents(chunks, self.embedding_model)
        retriever = vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 4}
        )

        prompt_template = """
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, say you don't know.

        Context: {context}
        Question: {question}
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=['context', 'question']
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        return (
            RunnableParallel({
                "context": retriever | RunnableLambda(format_docs),
                "question": RunnablePassthrough()
            })
            | prompt
            | StrOutputParser()
        )