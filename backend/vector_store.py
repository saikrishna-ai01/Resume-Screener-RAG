import chromadb


class VectorStore:
    """
    Stores and retrieves document embeddings using ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_or_create_collection(
            name="resume_chunks"
        )

    def add_documents(self, chunks: list, embeddings: list):
        """
        Store chunks and their embeddings in ChromaDB.
        """

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(
                f"{chunk['document_type']}_{chunk['filename']}_{chunk['chunk_id']}"
            )

            documents.append(chunk["text"])

            metadatas.append({
                "filename": chunk["filename"],
                "document_type": chunk["document_type"],
                "chunk_id": chunk["chunk_id"]
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding: list[float], k: int = 3):
        """
        Retrieve the most similar chunks.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

    def count(self) -> int:
        """
        Return the total number of stored documents.
        """
        return self.collection.count()

    def clear(self):
        """
        Remove all documents from the collection without deleting the collection.
        """
        try:
            data = self.collection.get()

            if data["ids"]:
                self.collection.delete(ids=data["ids"])

        except Exception:
            pass