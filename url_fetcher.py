import requests
from io import BytesIO
import pdfplumber
from docx import Document


def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()

        # PDF
        if "pdf" in content_type or url.lower().endswith(".pdf"):
            text = ""
            with pdfplumber.open(BytesIO(response.content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text

        # DOCX
        elif (
            "word" in content_type
            or url.lower().endswith(".docx")
        ):
            text = ""
            doc = Document(BytesIO(response.content))
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text

        # TXT / HTML fallback
        else:
            return response.text

    except Exception:
        return ""