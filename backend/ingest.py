from backend.chunker import ResumeChunker
from backend.embeddings import EmbeddingService
from backend.vector_store import VectorStore


class ResumeIngestion:

    def __init__(self):
        self.chunker = ResumeChunker()
        self.embedding = EmbeddingService()
        self.vector_store = VectorStore()

    def ingest(self, filename: str, text: str):

        chunks = self.chunker.create_chunks(
            filename=filename,
            document_type="resume",
            text=text
        )

        documents = [chunk["text"] for chunk in chunks]

        vectors = self.embedding.embed_documents(documents)

        self.vector_store.add_documents(
            chunks,
            vectors
        )

        return {
            "chunks": len(chunks),
            "status": "stored"
        }