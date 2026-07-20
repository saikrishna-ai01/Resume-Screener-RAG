from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Generates vector embeddings using HuggingFace.
    """

    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a single query.
        """
        return self.model.embed_query(text)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """
        return self.model.embed_documents(documents)