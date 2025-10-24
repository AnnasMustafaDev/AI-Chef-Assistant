import os
import json
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Together

class RecipeAssistantService:
    def __init__(self, pdf_path: Optional[str] = None, faiss_index_path: str = "faiss_index"):
        self.pdf_path = pdf_path
        self.faiss_index_path = faiss_index_path
        self.embeddings = self._initialize_embeddings()
        self.llm = self._initialize_llm()
        self.vector_store = None
        self.retriever = None
        self.chain = None

    def _initialize_embeddings(self):
        from langchain_community.embeddings import FakeEmbeddings
        return FakeEmbeddings(size=1024)

    def _initialize_llm(self):
        from langchain_community.llms import Ollama
        return Ollama(
            model="mistral",
            temperature=0.7
        )

    def initialize_vector_db(self, recreate: bool = False):
        if not recreate and os.path.exists(self.faiss_index_path):
            self.vector_store = FAISS.load_local(self.faiss_index_path, self.embeddings, allow_dangerous_deserialization=True)
        elif self.pdf_path:
            loader = PyPDFLoader(self.pdf_path)
            pages = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
            splits = text_splitter.split_documents(pages)
            self.vector_store = FAISS.from_documents(splits, self.embeddings)
            self.vector_store.save_local(self.faiss_index_path)
        else:
            raise ValueError("PDF path is required to create new vector store")

        self.retriever = self.vector_store.as_retriever(search_kwargs={'k': 5})
        self.chain = self._create_chain()
        return self.vector_store

    def _create_chain(self):
        prompt_template = """
        <s>[INST] You are a Home Chef assistant specialized in Pakistani cuisine. Your task is to help users
        create authentic Pakistani recipes using traditional cooking methods. Use only the information from
        the provided context. Be friendly and helpful in your responses.

        Context: {context}

        Question: {question}

        Structure your answer as:
        1. Start with a warm greeting
        2. List ingredients with Pakistani measurements (e.g., pao, ser, chammach)
        3. Provide step-by-step cooking instructions
        4. Include traditional cooking tips
        5. End with serving suggestions

        Return the response in JSON format with the following structure:
        {
            "greeting": "greeting message",
            "ingredients": ["ingredient1", "ingredient2", ...],
            "instructions": ["step1", "step2", ...],
            "cooking_tips": ["tip1", "tip2", ...],
            "serving_suggestions": ["suggestion1", "suggestion2", ...]
        }

        If you don't know the answer, return a JSON with an "error" field.
        [/INST] </s>
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        return (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def get_recipe(self, query: str):
        if not self.chain:
            raise RuntimeError("Vector database not initialized. Call initialize_vector_db() first")
        response = self.chain.invoke(query)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Unable to parse recipe response"}
