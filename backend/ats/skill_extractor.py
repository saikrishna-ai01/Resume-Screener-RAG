import re


class SkillExtractor:
    """
    Extract technical skills from resume or job description.
    """

    SKILLS = {
        "Python",
        "SQL",
        "FastAPI",
        "Flask",
        "Django",
        "Java",
        "C++",
        "JavaScript",
        "TypeScript",
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "GCP",
        "Git",
        "Linux",
        "MongoDB",
        "MySQL",
        "PostgreSQL",
        "Redis",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "Scikit-learn",
        "OpenCV",
        "YOLO",
        "LangChain",
        "LangGraph",
        "ChromaDB",
        "FAISS",
        "Pinecone",
        "RAG",
        "LLM",
        "Gemini",
        "Transformers",
        "Pandas",
        "NumPy",
        "Power BI",
        "Snowflake"
    }

    @classmethod
    def extract(cls, text: str) -> list[str]:

        text_lower = text.lower()

        found = []

        for skill in cls.SKILLS:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text_lower):
                found.append(skill)

        return sorted(found)