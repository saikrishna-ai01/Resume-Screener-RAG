from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()


class EmbeddingService:
    """
    Singleton Gemini Embedding Service.
    """

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        return cls._model

    def embed_query(self, text: str):
        return self.get_model().embed_query(text)

    def embed_documents(self, documents: list[str]):
        return self.get_model().embed_documents(documents)