from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_text):
    docs = [resume_text, job_text]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(docs)

    score = cosine_similarity(matrix[0:1], matrix[1:2])

    return round(float(score[0][0]) * 100, 2)