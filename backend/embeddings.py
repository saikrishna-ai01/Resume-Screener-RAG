from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


class EmbeddingService:

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = GoogleGenerativeAIEmbeddings(
                             model="text-embedding-004",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        return cls._model

    def embed_query(self, text):
        return self.get_model().embed_query(text)

    def embed_documents(self, documents):
        return self.get_model().embed_documents(documents)