class SkillMatcher:
    """
    Compare resume skills with job description skills.
    """

    @staticmethod
    def compare(
        resume_skills: list[str],
        jd_skills: list[str]
    ) -> dict:

        resume_set = set(skill.lower() for skill in resume_skills)
        jd_set = set(skill.lower() for skill in jd_skills)

        matched = sorted(
            skill for skill in jd_skills
            if skill.lower() in resume_set
        )

        missing = sorted(
            skill for skill in jd_skills
            if skill.lower() not in resume_set
        )

        additional = sorted(
            skill for skill in resume_skills
            if skill.lower() not in jd_set
        )

        if len(jd_set) == 0:
            percentage = 0.0
        else:
            percentage = round(
                (len(matched) / len(jd_set)) * 100,
                2
            )

        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "additional_skills": additional,
            "match_percentage": percentage
        }