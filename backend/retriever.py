from backend.embeddings import EmbeddingService
from backend.vector_store import VectorStore


class ResumeRetriever:
    """
    Retrieves the most relevant resume chunks from ChromaDB.
    """

    def __init__(self):
        self.embedding = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(self, query: str, k: int = 3):

        query_embedding = self.embedding.embed_query(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            k=k
        )

        return results
    