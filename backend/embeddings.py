from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Singleton Embedding Service.
    Loads the embedding model only once.
    """

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        return cls._model

    def embed_query(self, text: str) -> list[float]:
        return self.get_model().embed_query(text)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        return self.get_model().embed_documents(documents)