def generate_recommendation(score, missing_skills):
    if score >= 85:
        return "Highly recommended for interview round."

    elif score >= 70:
        if missing_skills <= 2:
            return "Good profile. Consider shortlist."
        return "Potential candidate, needs skill improvement."

    elif score >= 55:
        return "Average fit. Keep on hold."

    return "Not recommended for current role."