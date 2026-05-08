from src.cleaner import clean_text, preprocess_text
from src.skill_extractor import extract_skills
from src.matcher import calculate_similarity
from src.parser import parse_resume
from src.recommender import generate_recommendation


def analyze_resume(resume_text, job_description):
    cleaned_resume = preprocess_text(clean_text(resume_text))
    cleaned_jd = preprocess_text(clean_text(job_description))

    similarity = calculate_similarity(cleaned_resume, cleaned_jd)

    skills = extract_skills(resume_text)
    parsed = parse_resume(resume_text)

    skill_score = min(len(skills) * 8, 100)

    exp_score = 70
    edu_score = 75

    final_score = (
        similarity * 0.45
        + skill_score * 0.30
        + exp_score * 0.15
        + edu_score * 0.10
    )

    final_score = round(min(final_score, 100), 2)

    missing_skills = max(0, 10 - len(skills))

    if final_score >= 80:
        decision = "Shortlist"
    elif final_score >= 60:
        decision = "Hold"
    else:
        decision = "Reject"

    recommendation = generate_recommendation(
        final_score,
        missing_skills
    )

    return {
        "Name": parsed["Name"],
        "Email": parsed["Email"],
        "Phone": parsed["Phone"],
        "Education": parsed["Education"],
        "Experience": parsed["Experience"],
        "ATS Score": final_score,
        "Skills Found": len(skills),
        "Skill List": ", ".join(skills),
        "Missing Skills": missing_skills,
        "Decision": decision,
        "Recommendation": recommendation
    }