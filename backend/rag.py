from backend.embeddings import EmbeddingService
from backend.vector_store import VectorStore
from backend.prompts.rag_prompt import RAGPrompt
from backend.llm.gemini import GeminiLLM


class RAGPipeline:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.gemini = GeminiLLM()

    def ask(self, question: str, top_k: int = 5):

        try:
            # Generate query embedding
            query_embedding = self.embedding_service.embed_query(question)

            # Retrieve relevant chunks
            results = self.vector_store.search(
                query_embedding=query_embedding,
                k=top_k
            )

            if not results or not results.get("documents"):
                return {
                    "question": question,
                    "context": "",
                    "answer": "No relevant information found."
                }

            documents = results["documents"][0]

            if not documents:
                return {
                    "question": question,
                    "context": "",
                    "answer": "No relevant information found."
                }

            context = "\n\n".join(documents)

            prompt = RAGPrompt.create(
                context=context,
                question=question
            )

            try:
                answer = self.gemini.generate(prompt)
            except Exception:
                answer = (
                    "⚠️ AI Answer is temporarily unavailable because the Gemini API "
                    "is unavailable or the quota has been exceeded."
                )

            return {
                "question": question,
                "context": context,
                "answer": answer
            }

        except Exception as e:
            return {
                "question": question,
                "context": "",
                "answer": f"RAG Error: {str(e)}"
            }