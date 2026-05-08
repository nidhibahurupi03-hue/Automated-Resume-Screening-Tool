import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.extractor import extract_text
from src.url_fetcher import fetch_url_content
from src.analyzer import analyze_resume

st.set_page_config(
    page_title="ATS Intelligence X",
    page_icon="🚀",
    layout="wide"
)

# ---------------- THEME ----------------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp{
    background: radial-gradient(circle at top right,#0b1026,#050816 55%);
    color:white;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.hero{
    padding:28px;
    border-radius:24px;
    background: linear-gradient(135deg,#00d2ff,#3a47d5,#7b2ff7);
    box-shadow:0 0 40px rgba(80,120,255,.35);
    margin-bottom:22px;
}

.kpi{
    background: rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(16px);
    border-radius:22px;
    padding:22px;
    text-align:center;
    box-shadow:0 0 25px rgba(0,255,255,.08);
}

.kpi-num{
    font-size:34px;
    font-weight:700;
    color:#3ddcff;
}

.card{
    background: rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(16px);
    border-radius:22px;
    padding:22px;
    box-shadow:0 0 25px rgba(0,255,255,.08);
}

.badge-green{
    background:#16a34a;
    padding:6px 14px;
    border-radius:999px;
    display:inline-block;
}

.badge-yellow{
    background:#ca8a04;
    padding:6px 14px;
    border-radius:999px;
    display:inline-block;
}

.badge-red{
    background:#dc2626;
    padding:6px 14px;
    border-radius:999px;
    display:inline-block;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class='hero'>
    <h1 style='margin:0;'>🚀 ATS Intelligence X</h1>
    <p style='margin:8px 0 0 0;font-size:18px;color:#eef7ff;'>
        AI Resume Screening • Smart Ranking • Recruiter Analytics
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
job_description = st.text_area(
    "📋 Paste Job Description",
    height=180
)

uploaded_files = st.file_uploader(
    "📤 Upload Resume Files",
    type=["pdf","docx","txt"],
    accept_multiple_files=True
)

resume_urls = st.text_area(
    "🔗 Resume URLs (one per line)",
    height=100
)

# ---------------- ANALYZE ----------------
if st.button("🔍 Analyze Candidates", use_container_width=True):

    if not job_description:
        st.warning("Please paste Job Description")
        st.stop()

    results = []

    # Uploads
    if uploaded_files:
        for file in uploaded_files:
            text = extract_text(file)
            if text:
                r = analyze_resume(text, job_description)
                if isinstance(r, dict):
                    r["Candidate"] = file.name
                    results.append(r)

    # URLs
    if resume_urls.strip():
        for url in resume_urls.splitlines():
            url = url.strip()
            if url:
                text = fetch_url_content(url)
                if text:
                    r = analyze_resume(text, job_description)
                    if isinstance(r, dict):
                        r["Candidate"] = url
                        results.append(r)

    if not results:
        st.warning("No resumes found")
        st.stop()

    df = pd.DataFrame(results)
    df = df.sort_values("ATS Score", ascending=False).reset_index(drop=True)
    df["Display Name"] = [f"Candidate {i+1}" for i in range(len(df))]

    total = len(df)
    shortlist = len(df[df["Decision"] == "Shortlist"])
    hold = len(df[df["Decision"] == "Hold"])
    reject = len(df[df["Decision"] == "Reject"])
    top_score = round(df["ATS Score"].max(), 2)

    # ---------------- KPI ----------------
    c1,c2,c3,c4,c5 = st.columns(5)

    kpis = [
        ("Candidates", total),
        ("Shortlisted", shortlist),
        ("Hold", hold),
        ("Rejected", reject),
        ("Top Score", f"{top_score}%")
    ]

    for col,(label,val) in zip([c1,c2,c3,c4,c5],kpis):
        with col:
            st.markdown(f"""
            <div class='kpi'>
                <div class='kpi-num'>{val}</div>
                <div>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- LEADERBOARD ----------------
    st.markdown("## 🏆 Leaderboard")

    medals = ["🥇","🥈","🥉"]

    for i,row in df.head(3).iterrows():
        medal = medals[i] if i < 3 else "🏅"

        decision = row["Decision"]

        if decision == "Shortlist":
            badge = "<span class='badge-green'>Shortlist</span>"
        elif decision == "Hold":
            badge = "<span class='badge-yellow'>Hold</span>"
        else:
            badge = "<span class='badge-red'>Reject</span>"

        st.markdown(f"""
        <div class='card'>
            <h3>{medal} {row.get('Name','Unknown')} — {row['ATS Score']}%</h3>
            {badge}
            <p>{row.get('Recommendation','')}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- CHARTS ----------------
    st.markdown("## 📈 Recruiter Analytics")

    col1,col2 = st.columns(2)

    with col1:
        fig = px.bar(
            df,
            x="Display Name",
            y="ATS Score",
            text="ATS Score"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            df,
            names="Decision",
            hole=.65
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- ATS Gauge ----------------
    st.markdown("## 🎯 ATS Match Meter")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=top_score,
        title={'text': "Top Candidate Score"},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "#3ddcff"},
            'steps': [
                {'range':[0,50], 'color':"#3b0d0d"},
                {'range':[50,75], 'color':"#403000"},
                {'range':[75,100], 'color':"#0b3b1f"},
            ]
        }
    ))

    gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )

    st.plotly_chart(gauge, use_container_width=True)

    # ---------------- TABLE ----------------
    st.markdown("## 📋 Candidate Ranking")

    show_cols = [
        "Display Name",
        "Name",
        "ATS Score",
        "Decision",
        "Recommendation"
    ]

    available = [c for c in show_cols if c in df.columns]

    st.dataframe(
        df[available],
        use_container_width=True
    )

    # ---------------- PROFILE ----------------
    top = df.iloc[0].to_dict()

    st.markdown("## 👑 Top Candidate Profile")

    left,right = st.columns([1,3])

    with left:
        st.markdown("## 👤")

    with right:
        st.subheader(top.get("Name","Unknown"))
        st.caption(top.get("Email","Not Found"))

        st.write("📞 Phone:", top.get("Phone","Not Found"))
        st.write("🎓 Education:", top.get("Education","Not Found"))
        st.write("💼 Experience:", top.get("Experience","0-1 years"))
        st.write("🛠 Skills:", top.get("Skill List","None"))
        st.write("❌ Missing Skills:", top.get("Missing Skills",0))
        st.write("⭐ ATS Score:", f"{top.get('ATS Score',0)}%")
        st.write("📌 Decision:", top.get("Decision","Unknown"))

    st.info("🧠 AI Recommendation: " + top.get("Recommendation","No recommendation"))

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Recruiter Report",
        csv,
        "ats_report.csv",
        "text/csv",
        use_container_width=True
    )