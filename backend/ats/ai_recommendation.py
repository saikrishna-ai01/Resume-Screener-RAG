from backend.llm.gemini import GeminiLLM


class AIRecommendation:
    """
    Generate ATS recommendations using Gemini.
    """

    def __init__(self):
        self.llm = GeminiLLM()

    def generate(
        self,
        report: dict
    ) -> str:

        prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the following ATS report.

ATS Score:
{report['ats_score']}

Recommendation:
{report['recommendation']}

Matched Skills:
{', '.join(report['matched_skills'])}

Missing Skills:
{', '.join(report['missing_skills'])}

Additional Skills:
{', '.join(report['additional_skills'])}

Strengths:
{', '.join(report['strengths'])}

Provide:

# Overall Resume Review
Briefly evaluate the resume.

# ATS Score Analysis
Explain why this ATS score was assigned.

# Matched Skills
Mention the strongest matched skills.

# Missing Skills
Explain the impact of the missing skills.

# Resume Improvement Suggestions
Provide practical suggestions to improve the resume.

# Recommended Projects
Suggest 2–3 projects relevant to the missing skills.

# Recommended Certifications
Suggest certifications that strengthen the profile.

# Final Hiring Recommendation
Choose one:
- Strongly Recommend
- Recommend
- Consider After Improvements
- Not Recommended

Keep the response concise, professional, and use Markdown headings.
"""

        return self.llm.generate(prompt)