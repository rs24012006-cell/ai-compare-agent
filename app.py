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

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Dashboard")
st.sidebar.info("AI Skill Assessment System")

option = st.sidebar.radio(
    "Navigate",
    ["Analyze", "Interview", "Learning Plan", "Report"]
)

# ---------------- CHART ----------------
def show_skill_chart(matched, missing):
    labels = ["Matched Skills", "Missing Skills"]
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

# ---------------- TITLE ----------------
st.title("🚀 AI Compare Agent")
st.markdown("### Smart Skill Assessment & Learning System")
st.divider()

# ================= ANALYZE =================
if option == "Analyze":

    st.markdown("## 📊 Skill Analysis Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        jd = st.text_area("📄 Job Description", height=250)

    with col2:
        resume = st.text_area("📄 Resume", height=250)

    if st.button("Analyze Skills"):

        if jd and resume:
            st.success("Analyzing...")

            result = compare_skills(jd, resume)

            try:
                # SAFE JSON EXTRACTION
                start = result.find("{")
                end = result.rfind("}") + 1
                json_str = result[start:end]

                data = json.loads(json_str)

                matched = data.get("matched", [])
                missing = data.get("missing", [])

            except:
                st.warning("AI did not return proper JSON. Using fallback.")

                matched = ["Python", "SQL"]
                missing = ["AWS", "Django"]

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("✅ Matched Skills")
                st.success(matched)

            with c2:
                st.subheader("❌ Missing Skills")
                st.error(missing)

            st.divider()
            show_skill_chart(matched, missing)

# ================= INTERVIEW =================
elif option == "Interview":

    st.header("🎤 AI Interview")

    skill = st.text_input("Enter skill (e.g. Python, SQL)")

    if st.button("Generate Question"):
        question = generate_question(skill)
        st.session_state["question"] = question
        st.info(question)

    answer = st.text_area("Your Answer")

    if st.button("Evaluate Answer"):
        if "question" in st.session_state:
            result = evaluate_answer(st.session_state["question"], answer)
            st.success(result)
        else:
            st.warning("Generate question first")

# ================= LEARNING PLAN =================
elif option == "Learning Plan":

    st.header("📚 Learning Roadmap")

    missing_input = st.text_area("Enter Missing Skills")

    if st.button("Generate Plan"):
        if missing_input:
            plan = generate_learning_plan(missing_input)
            st.write(plan)

# ================= REPORT =================
elif option == "Report":

    st.header("📄 Generate Report")

    jd = st.text_area("📄 Job Description", height=200)
    resume = st.text_area("📄 Resume", height=200)

    if st.button("Generate PDF Report"):

        if jd and resume:
            st.info("Generating report...")

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
                st.warning("AI did not return proper JSON. Using fallback.")

                matched = ["Python", "SQL"]
                missing = ["AWS", "Django"]

            roadmap_text = generate_learning_plan(str(missing))

            file_path = generate_pdf_report(score, matched, missing, roadmap_text)

            st.success("PDF Generated Successfully!")

            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name=file_path,
                    mime="application/pdf"
                )
