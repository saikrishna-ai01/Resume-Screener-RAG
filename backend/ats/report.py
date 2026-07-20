class ATSReport:
    """
    Generate a structured ATS report.
    """

    @staticmethod
    def generate(
        comparison: dict,
        score: dict
    ) -> dict:

        matched = comparison["matched_skills"]
        missing = comparison["missing_skills"]
        additional = comparison["additional_skills"]

        strengths = []

        if matched:
            strengths.append(
                f"Matches {len(matched)} required technical skills: {', '.join(matched)}."
            )

        if additional:
            strengths.append(
                f"Has {len(additional)} additional technical skills beyond the job requirements."
            )
            strengths.append(
                "Resume demonstrates knowledge beyond the minimum job requirements."
            )

        improvements = []

        if missing:
            improvements.append(
                f"Consider adding experience or projects related to: {', '.join(missing)}."
            )

            improvements.append(
                "Customize the resume to better match the job description."
            )

        return {
            "ats_score": score["ats_score"],
            "recommendation": score["recommendation"],
            "matched_skills": matched,
            "missing_skills": missing,
            "additional_skills": additional,
            "strengths": strengths,
            "improvements": improvements
        }