import os
import pdfplumber
from docx import Document


def extract_pdf_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass
    return text


def extract_docx_text(file):
    text = ""
    try:
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception:
        pass
    return text


def extract_text(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext == ".pdf":
        return extract_pdf_text(uploaded_file)

    elif ext == ".docx":
        return extract_docx_text(uploaded_file)

    elif ext == ".txt":
        return uploaded_file.read().decode("utf-8")

    return ""