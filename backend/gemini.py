import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class GeminiLLM:
    """
    Gemini LLM wrapper.
    """

    def __init__(self):

        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )

    def generate(self, prompt: str):

        response = self.model.invoke(prompt)

        return response.content