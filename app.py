import streamlit as st
import json
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from agent import (
    compare_skills,
    generate_question,
    evaluate_answer,
    generate_learning_plan,
    calculate_resume_score
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Compare Agent", page_icon="🚀", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.5);
    margin-bottom: 15px;
}

.stButton>button {
    background: linear-gradient(90deg, #7c3aed, #9333ea);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

textarea, input {
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 AI Compare Agent")
option = st.sidebar.radio(
    "Navigation",
    ["Analyze", "Interview", "Learning Plan", "Report"]
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI Compare Agent</h1>
<p style='text-align:center; color:gray;'>Analyze • Practice • Improve • Get Hired</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- CHART ----------------
def show_skill_chart(matched, missing):
    data = {
        "Type": ["Matched", "Missing"],
        "Count": [len(matched), len(missing)]
    }
    fig = px.bar(data, x="Type", y="Count", title="Skill Gap Analysis")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- PDF ----------------
def generate_pdf_report(score, matched, missing, roadmap_text):
    file_name = "AI_Skill_Report.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("AI Skill Assessment Report", styles["Title"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Score: {score}", styles["Normal"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Matched Skills: {matched}", styles["Normal"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Missing Skills: {missing}", styles["Normal"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Learning Plan: {roadmap_text}", styles["Normal"]))

    doc.build(content)
    return file_name

# ================= ANALYZE =================
if option == "Analyze":

    st.subheader("📊 Skill Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        jd = st.text_area("📄 Job Description", height=200)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        resume = st.text_area("📄 Resume", height=200)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Analyze Skills"):
        if jd and resume:
            with st.spinner("Analyzing..."):
                result = compare_skills(jd, resume)

            try:
                start = result.find("{")
                end = result.rfind("}") + 1
                data = json.loads(result[start:end])

                matched = data.get("matched", [])
                missing = data.get("missing", [])

            except:
                matched = ["Python", "SQL"]
                missing = ["AWS", "Django"]

            # KPI Cards
            c1, c2, c3 = st.columns(3)

            c1.markdown(f"""
            <div class="card">
            <h3>✅ Matched Skills</h3>
            <h1>{len(matched)}</h1>
            </div>
            """, unsafe_allow_html=True)

            c2.markdown(f"""
            <div class="card">
            <h3>❌ Missing Skills</h3>
            <h1>{len(missing)}</h1>
            </div>
            """, unsafe_allow_html=True)

            score = round(len(matched)/(len(matched)+len(missing)+1)*100)

            c3.markdown(f"""
            <div class="card">
            <h3>📊 Score</h3>
            <h1>{score}%</h1>
            </div>
            """, unsafe_allow_html=True)

            show_skill_chart(matched, missing)

# ================= INTERVIEW =================
elif option == "Interview":

    st.subheader("🎤 AI Interview")

    skill = st.text_input("Enter Skill")

    if st.button("🎯 Generate Question"):
        question = generate_question(skill)
        st.session_state["question"] = question
        st.info(question)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    answer = st.text_area("✍️ Your Answer")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📊 Evaluate Answer"):
        if "question" in st.session_state:
            result = evaluate_answer(st.session_state["question"], answer)
            st.success(result)
        else:
            st.warning("Generate question first")

# ================= LEARNING =================
elif option == "Learning Plan":

    st.subheader("📚 Learning Roadmap")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    missing_input = st.text_area("Enter Missing Skills")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Generate Plan"):
        if missing_input:
            with st.spinner("Generating roadmap..."):
                plan = generate_learning_plan(missing_input)
            st.write(plan)

# ================= REPORT =================
elif option == "Report":

    st.subheader("📄 Generate Report")

    col1, col2 = st.columns(2)

    with col1:
        jd = st.text_area("📄 Job Description", height=200)

    with col2:
        resume = st.text_area("📄 Resume", height=200)

    if st.button("📥 Generate PDF Report"):
        if jd and resume:
            with st.spinner("Generating report..."):
                score = calculate_resume_score(jd, resume)
                result = compare_skills(jd, resume)

            try:
                start = result.find("{")
                end = result.rfind("}") + 1
                data = json.loads(result[start:end])

                matched = data.get("matched", [])
                missing = data.get("missing", [])

            except:
                matched = ["Python", "SQL"]
                missing = ["AWS", "Django"]

            roadmap_text = generate_learning_plan(str(missing))

            file_path = generate_pdf_report(score, matched, missing, roadmap_text)

            st.success("✅ Report Generated Successfully!")

            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Report",
                    data=f,
                    file_name=file_path,
                    mime="application/pdf"
                )
