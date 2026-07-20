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
            query_embedding = self.embedding_service.embed_query(question)
            results = self.vector_store.search(
                query_embedding=query_embedding,
                k=top_k
            )

            if results is None:
                return {
                    "question": question,
                    "context": "",
                    "answer": "No results returned from ChromaDB."
                }

            documents = results.get("documents")

            if documents is None or len(documents) == 0:
                return {
                    "question": question,
                    "context": "",
                    "answer": "No relevant information found in the database."
                }

            documents = documents[0]

            if not documents:
                return {
                    "question": question,
                    "context": "",
                    "answer": "No relevant information found in the database."
                }

            context = "\n\n".join(documents)

            prompt = RAGPrompt.create(
                context=context,
                question=question
            )

            try:
               answer = self.gemini.generate(prompt)
            except Exception as e:
                answer = (
                    "⚠️ AI Answer is temporarily unavailable because the Gemini API quota has been exceeded. "
                    "Please try again later or configure another Gemini API key."
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