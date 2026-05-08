# 🚀 ATS Intelligence X – AI Resume Screening Tool

## 📌 Overview

ATS Intelligence X is an advanced AI-powered Resume Screening Tool built using Python, NLP, and Streamlit.

This project simulates how modern Applicant Tracking Systems (ATS) analyze resumes against job descriptions and shortlist candidates automatically.

It extracts candidate details, matches skills, calculates ATS scores, ranks applicants, and generates recruiter-friendly reports.

---

## ✨ Features

* 📤 Upload Resume (PDF / DOCX / TXT)
* 🔗 Analyze resumes directly from URL
* 🧠 AI Resume Parsing (Name, Email, Phone, Education, Experience)
* 🔍 Skill Extraction using NLP
* 📊 ATS Score Calculation
* 🏆 Candidate Ranking
* 🟢 Shortlist / 🟡 Hold / 🔴 Reject Decision
* 📈 Recruiter Analytics Dashboard
* 🎯 ATS Match Meter
* 📥 CSV Report Download
* 🌐 Premium Streamlit UI

---

## 🛠 Tech Stack

* Python
* Streamlit
* Pandas
* spaCy
* Scikit-learn
* TF-IDF
* Cosine Similarity
* Regex
* Plotly

---

## 📂 Project Structure

```bash
Automated-Resume-Screening-Tool/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│
├── src/
│   ├── extractor.py
│   ├── cleaner.py
│   ├── matcher.py
│   ├── skill_extractor.py
│   ├── url_fetcher.py
│   ├── parser.py
│   ├── recommender.py
│   └── analyzer.py
│
├── resumes/
├── outputs/
├── images/
└── docs/
```

---

## ⚙ Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

---

## 📊 Workflow

Resume Upload / URL → Text Extraction → Cleaning → Skill Extraction → JD Matching → ATS Score → Ranking → Recommendation → Report Generation

---

## 🎯 Industry Relevance

This project is useful for:

* HR Tech
* AI Recruitment Platforms
* Resume Screening Automation
* NLP Applications
* Python Automation Projects
* Data Analytics Projects

---

## 📌 Sample Output

* ATS Score: 88%
* Decision: Shortlist
* Recommendation: Highly recommended for interview round

---

## 👩‍💻 Developer

Built as an industry-oriented Python + AI/NLP portfolio project.
