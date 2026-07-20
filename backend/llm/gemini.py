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
            model="gemini-flash-latest",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )

    def generate(self, prompt: str) -> str:

        response = self.model.invoke(prompt)

        content = response.content

       # Normal string response
        if isinstance(content, str):
            return content

       # List response
        if isinstance(content, list):
            texts = []

            for item in content:
                if isinstance(item, dict):
                    if "text" in item:
                        texts.append(item["text"])
                else:
                    text = getattr(item, "text", None)
                    if text:
                        texts.append(text)

            return "\n".join(texts)

        return str(content)