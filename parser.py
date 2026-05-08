import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_email(text):
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return emails[0] if emails else "Not Found"


def extract_phone(text):
    phones = re.findall(r"\+?\d[\d\s\-]{8,15}", text)
    return phones[0] if phones else "Not Found"


def extract_name(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Unknown"


def extract_education(text):
    education_keywords = [
        "bachelor",
        "b.tech",
        "be",
        "mca",
        "msc",
        "bsc",
        "diploma",
        "master",
        "phd"
    ]

    lower = text.lower()

    found = [e for e in education_keywords if e in lower]

    return ", ".join(found) if found else "Not Found"


def extract_experience(text):
    match = re.findall(r"(\d+)\+?\s+years?", text.lower())

    if match:
        return f"{match[0]} years"

    return "0-1 years"


def parse_resume(text):
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Education": extract_education(text),
        "Experience": extract_experience(text)
    }