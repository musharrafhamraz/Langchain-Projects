# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableLambda
# from langchain_core.output_parsers import StrOutputParser

# class WebRag:
#     def __init__(self):
#         self.embedding_model = HuggingFaceEmbeddings(
#             model_name="name of the model"
#         )
#         self.splitter = RecursiveCharacterTextSplitter(
#             chunk_size=300,
#             chunk_overlap=50
#         )
#         self.str_parser = StrOutputParser()
#         self.llm_model = "model name"

#     def rag_pipeline(self, text: str):
#         chunks = self.splitter.create_documents([text])
#         vector_store = FAISS.from_documents(chunks, self.embedding_model)
#         retriever = vector_store.as_retriever(search_type = 'similarity',
#                                               search_kargs = {"k": 6})
#         prompt_template = """

#             You are a helpful assistant.
#             Only answer from the provided context.
#             if there is insufficinet context, say "I can't answer what you asked."

#             Context: {context}
#             Question: {question}

#             """
#         prompt = PromptTemplate(
#             template=prompt_template,
#             input_variables=["context", "question"]
                
#             )
        
#         return (
#             RunnableSequence(retriever, prompt, self.llm_model, self.str_parser)
#         )

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableSequence
# from langchain.llms import HuggingFaceHub  # or any other LLM you're using

class WebRag:
    def __init__(self, product_data):
        self.embedding_model = "HuggingFaceEmbeddings(model_name=sentence-transformers/all-MiniLM-L6-v2)"
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        self.str_parser = StrOutputParser()
        self.llm_model = "HuggingFaceHub(repo_id=google/flan-t5-base, model_kwargs=)"

        text_blocks = [p['description'] + " " + str(p['specifications']) for p in product_data]
        docs = self.splitter.create_documents(text_blocks)
        self.vector_store = FAISS.from_documents(docs, self.embedding_model)

        self.retriever = self.vector_store.as_retriever(search_type='similarity', search_kwargs={"k": 5})
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

        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm_model
            | self.str_parser
        )

    def query(self, question: str):
        return self.chain.invoke(question)
