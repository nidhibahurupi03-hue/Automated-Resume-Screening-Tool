SKILLS_DB = [
    "python", "sql", "machine learning", "data analysis",
    "pandas", "numpy", "git", "github",
    "api", "apis", "oop", "problem solving",
    "scikit-learn", "nlp", "spacy",
    "streamlit", "docker", "aws", "cloud"
]


def extract_skills(text):
    found = []

    text = text.lower()

    for skill in SKILLS_DB:
        if skill in text:
            found.append(skill)

    return list(set(found))