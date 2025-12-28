import io

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pdfplumber  # for PDF text extraction [web:120][web:137]

from preprocess import clean_resume, extract_skills
from clustering import cluster_skills, get_embeddings
from scoring import score_candidate

st.set_page_config(page_title="AI Resume Parser", layout="wide")

# ----------------- STYLES & TITLE -----------------
st.markdown(
    """
<style>
.main {padding: 2rem;}
.stMetric {background-color: #1f77b4;}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🤖 AI Resume Parser")
st.markdown(
    "**Transform hiring with contextual skill analysis beyond keyword matching**"
)

# ----------------- SIDEBAR -----------------
st.sidebar.header("🎯 Job Requirements")
job_python = st.sidebar.slider("Python Skills", 0, 5, 2)
job_leadership = st.sidebar.slider("Leadership Experience", 0, 5, 1)
job_web = st.sidebar.slider("Web Development", 0, 5, 1)
job_data = st.sidebar.slider("Data Analysis", 0, 5, 2)

job_weights = {
    "python": job_python / 10,
    "leadership": job_leadership / 10,
    "web": job_web / 10,
    "data": job_data / 10,
}

# Keep resumes across tabs
if "resumes" not in st.session_state:
    st.session_state["resumes"] = []

# ----------------- TABS -----------------
tab1, tab2, tab3 = st.tabs(
    ["📄 Upload Resumes", "📊 Analysis Dashboard", "⚙️ Batch Processing"]
)

# ================= TAB 1: UPLOAD =================
with tab1:
    uploaded_files = st.file_uploader(
        "Upload resumes (.txt or .pdf)",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    def extract_text_from_pdf(uploaded_file):
        """Extract text from a PDF UploadedFile using pdfplumber."""
        raw = uploaded_file.read()
        buffer = io.BytesIO(raw)
        text_pages = []
        with pdfplumber.open(buffer) as pdf:
            for page in pdf.pages:
                text_pages.append(page.extract_text() or "")
        return "\n".join(text_pages)

    if uploaded_files:
        resumes = []
        for file in uploaded_files:
            name_lower = file.name.lower()

            # ----- PDF -----
            if name_lower.endswith(".pdf"):
                content = extract_text_from_pdf(file)  # [web:120][web:125]
            # ----- TXT or other text-like -----
            else:
                raw_bytes = file.read()
                try:
                    content = raw_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    content = raw_bytes.decode("latin-1", errors="ignore")  # [web:135][web:138]

            # basic guard: empty text from bad PDFs
            if not content.strip():
                st.warning(f"⚠️ No text extracted from {file.name}. Skipping.")
                continue

            skills = extract_skills(content)
            resumes.append(
                {
                    "filename": file.name,
                    "content": content,
                    "cleaned": clean_resume(content),
                    "skills": skills,
                }
            )

        if resumes:
            st.session_state["resumes"] = resumes
            st.success(f"✅ Processed {len(resumes)} resumes")

            st.subheader("Preview (first resume)")
            st.text_area(
                "Raw Content",
                resumes[0]["content"][:2000],
                height=250,
            )
        else:
            st.error("No valid text detected in uploaded files.")

# ================= TAB 2: ANALYSIS =================
with tab2:
    resumes = st.session_state.get("resumes", [])

    if resumes:
        scores = []
        skill_phrases = []

        for resume in resumes:
            score = score_candidate(resume["skills"], {}, job_weights)
            scores.append(score)

            phrases = list(resume["skills"].keys())
            skill_phrases.extend(
                [f"{p}: {c}" for p, c in resume["skills"].items()]
            )

        df = pd.DataFrame(
            {
                "Resume": [r["filename"] for r in resumes],
                "Score": scores,
                "Python": [r["skills"].get("python", 0) for r in resumes],
                "Leadership": [
                    r["skills"].get("leadership", 0) for r in resumes
                ],
                "Web": [r["skills"].get("web", 0) for r in resumes],
                "Data": [r["skills"].get("data", 0) for r in resumes],
            }
        )

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Best Candidate", f"{df['Score'].max():.1f}/10")
        with col2:
            st.metric("Average Score", f"{df['Score'].mean():.1f}/10")
        with col3:
            st.metric("Unique Skill Tags", len(set(skill_phrases)))
        with col4:
            st.metric("Resumes Processed", len(resumes))

        # Score distribution
        fig = px.histogram(
            df, x="Score", nbins=10, title="Candidate Score Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Skills radar for top 3
        fig_radar = go.Figure()
        for _, row in df.sort_values("Score", ascending=False).head(3).iterrows():
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=[row["Python"], row["Leadership"], row["Web"], row["Data"]],
                    theta=["Python", "Leadership", "Web", "Data"],
                    fill="toself",
                    name=row["Resume"][:15],
                )
            )
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True,
            title="Top Candidates - Skill Profile",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.dataframe(
            df.sort_values("Score", ascending=False), use_container_width=True
        )
    else:
        st.info("Upload resumes in the first tab to see analysis.")

# ================= TAB 3: BATCH CSV =================
with tab3:
    st.header("Batch Upload & Download Results")
    csv_file = st.file_uploader("Upload CSV with resumes", type="csv")

    if csv_file:
        df_batch = pd.read_csv(csv_file)

        if "resume_text" not in df_batch.columns:
            st.error("CSV must contain a 'resume_text' column.")
        else:
            results = []
            for idx, row in df_batch.iterrows():
                skills = extract_skills(row["resume_text"])
                score = score_candidate(skills, {}, job_weights)
                results.append(
                    {
                        "candidate_id": idx,
                        "score": score,
                        "skills": skills,
                        "recommendation": (
                            "Hire"
                            if score >= 7
                            else "Review"
                            if score >= 5
                            else "Reject"
                        ),
                    }
                )

            result_df = pd.DataFrame(results)
            st.dataframe(result_df)

            csv_out = result_df.to_csv(index=False)
            st.download_button(
                "Download Results", csv_out, "resume_scores.csv"
            )

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown(
    "Built with **Streamlit**, **NLTK**, **Sentence Transformers**, **pdfplumber**, and **Scikit-learn**."
)
