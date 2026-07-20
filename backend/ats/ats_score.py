class ATSScorer:
    """
    Calculate ATS score from the skill comparison.
    """

    @staticmethod
    def calculate(match_result: dict) -> dict:

        match_percentage = match_result["match_percentage"]

        ats_score = round(match_percentage)

        if ats_score >= 90:
            recommendation = "Excellent Match"
        elif ats_score >= 75:
            recommendation = "Good Match"
        elif ats_score >= 60:
            recommendation = "Average Match"
        else:
            recommendation = "Needs Improvement"

        return {
            "ats_score": ats_score,
            "recommendation": recommendation
        }