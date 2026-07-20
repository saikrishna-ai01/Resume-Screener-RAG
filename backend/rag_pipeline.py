from backend.llm.gemini import GeminiLLM
from backend.prompts.rag_prompt import RAGPrompt
from backend.retriever import ResumeRetriever


class RAGPipeline:

    def __init__(self):

        self.retriever = ResumeRetriever()
        self.llm = GeminiLLM()

    def ask(self, question: str):

        results = self.retriever.retrieve(question)

        documents = results.get("documents")

        if documents is not None and len(documents) > 0:
            context = "\n\n".join(documents[0])
        else:
            context = ""

        prompt = RAGPrompt.create(
            context=context,
            question=question
        )

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "answer": answer,
            "context": context
        }