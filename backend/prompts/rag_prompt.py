class RAGPrompt:

    @staticmethod
    def create(context: str, question: str):

        return f"""
You are an AI Resume Screening Assistant.

Answer ONLY using the resume information provided below.

If the answer is not present in the resume, reply:

"I couldn't find that information in the resume."

Resume Context:

{context}

Question:

{question}

Answer:
"""
