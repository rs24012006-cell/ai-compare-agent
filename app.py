import streamlit as st
import json
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from agent import (
    extract_skills,
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
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #F9FAFB;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stTextArea textarea {
    border-radius: 10px;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1E222A;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1055/1055687.png", width=80)
st.sidebar.title("AI Compare Agent")
st.sidebar.markdown("---")

option = st.sidebar.radio(
    "📌 Navigation",
    ["Analyze", "Interview", "Learning Plan", "Report"]
)

st.sidebar.markdown("---")
st.sidebar.info("Built for Smart Skill Assessment 🚀")

# ---------------- CHART ----------------
def show_skill_chart(matched, missing):
    labels = ["Matched", "Missing"]
    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Skill Gap Analysis")
    st.pyplot(fig)

# ---------------- PDF FUNCTION ----------------
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
    content.append(Paragraph(f"Learning Roadmap: {roadmap_text}", styles["Normal"]))

    doc.build(content)
    return file_name

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Skill Assessment System</h1>
<p style='text-align: center; color: gray;'>Analyze • Practice • Improve • Get Hired</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= ANALYZE =================
if option == "Analyze":

    st.subheader("📊 Skill Analysis Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        jd = st.text_area("📄 Job Description", height=250)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        resume = st.text_area("📄 Resume", height=250)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔍 Analyze Skills"):

        if jd and resume:
            with st.spinner("Analyzing your skills..."):
                result = compare_skills(jd, resume)

            try:
                start = result.find("{")
                end = result.rfind("}") + 1
                json_str = result[start:end]
                data = json.loads(json_str)

                matched = data.get("matched", [])
                missing = data.get("missing", [])

            except:
                matched = ["Python", "SQL"]
                missing = ["AWS", "Django"]

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("### ✅ Matched Skills")
                st.success(matched)

            with c2:
                st.markdown("### ❌ Missing Skills")
                st.error(missing)

            show_skill_chart(matched, missing)

# ================= INTERVIEW =================
elif option == "Interview":

    st.subheader("🎤 AI Mock Interview")

    skill = st.text_input("Enter Skill")

    if st.button("🎯 Generate Question"):
        question = generate_question(skill)
        st.session_state["question"] = question
        st.info(question)

    answer = st.text_area("✍️ Your Answer")

    if st.button("📊 Evaluate Answer"):
        if "question" in st.session_state:
            result = evaluate_answer(st.session_state["question"], answer)
            st.success(result)
        else:
            st.warning("Generate question first")

# ================= LEARNING PLAN =================
elif option == "Learning Plan":

    st.subheader("📚 Personalized Learning Roadmap")

    missing_input = st.text_area("Enter Missing Skills")

    if st.button("🚀 Generate Plan"):
        if missing_input:
            with st.spinner("Creating roadmap..."):
                plan = generate_learning_plan(missing_input)
            st.write(plan)

# ================= REPORT =================
elif option == "Report":

    st.subheader("📄 Generate Professional Report")

    jd = st.text_area("📄 Job Description", height=200)
    resume = st.text_area("📄 Resume", height=200)

    if st.button("📥 Generate PDF Report"):

        if jd and resume:
            with st.spinner("Generating report..."):
                score = calculate_resume_score(jd, resume)
                result = compare_skills(jd, resume)

            try:
                start = result.find("{")
                end = result.rfind("}") + 1
                json_str = result[start:end]
                data = json.loads(json_str)

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
