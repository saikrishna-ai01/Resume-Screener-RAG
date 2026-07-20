from backend.utils import (
    extract_skills,
    extract_experience,
    extract_education
)


class JobDescriptionAnalyzer:

    def analyze(self, text: str) -> dict:

        return {

            "skills": extract_skills(text),

            "experience": extract_experience(text),

            "education": extract_education(text),

            "text": text

        }