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

# ---------------- CHART ----------------
def show_skill_chart(matched, missing):
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(matched), len(missing)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Skill Gap Analysis")
    st.pyplot(fig)


st.title("AI Compare Agent 🚀")

# ---------------- INPUT ----------------
jd = st.text_area("📄 Job Description")
resume = st.text_area("📄 Resume")

# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Skills", key="btn1"):

    if jd and resume:
        st.info("Analyzing...")

        # Extract skills (optional display)
        jd_skills = extract_skills(jd)
        resume_skills = extract_skills(resume)

        st.subheader("JD Skills")
        st.write(jd_skills)

        st.subheader("Resume Skills")
        st.write(resume_skills)

        # Compare skills
        result = compare_skills(jd, resume)

        try:
            data = json.loads(result)

            matched = data.get("matched", [])
            missing = data.get("missing", [])

            st.subheader("Matched Skills")
            st.write(matched)

            st.subheader("Missing Skills")
            st.write(missing)

            show_skill_chart(matched, missing)

        except:
            st.error("AI output is not valid JSON")
            st.write(result)


# ---------------- SCORE ----------------
st.header("📊 Resume Score")

if jd and resume:
    if st.button("Get Resume Score", key="score_btn"):
        score = calculate_resume_score(jd, resume)
        st.subheader("Your Score")
        st.write(score)

# ---------------- INTERVIEW ----------------
st.header("🎤 AI Interview")

skill = st.text_input("Enter skill (e.g. Python, SQL)")

if st.button("Generate Question", key="btn2"):
    question = generate_question(skill)
    st.session_state["question"] = question
    st.write(question)

answer = st.text_area("Your Answer")

if st.button("Evaluate Answer", key="btn3"):
    if "question" in st.session_state:
        result = evaluate_answer(st.session_state["question"], answer)
        st.write(result)
    else:
        st.warning("Generate question first")

# ---------------- LEARNING ROADMAP ----------------
st.header("📚 Learning Roadmap Generator")

missing_input = st.text_area("Enter missing skills")

if st.button("Generate Learning Plan", key="learning_btn"):
    if missing_input:
        plan = generate_learning_plan(missing_input)
        st.subheader("Your Plan")
        st.write(plan)

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

st.header("📄 Download Report")

if st.button("Generate PDF Report"):
    if jd and resume:

        score = calculate_resume_score(jd, resume)

        result = compare_skills(jd, resume)

        try:
            import json
            data = json.loads(result)
            matched = data.get("matched", [])
            missing = data.get("missing", [])

            roadmap_text = generate_learning_plan(str(missing))

            file_path = generate_pdf_report(score, matched, missing, roadmap_text)

            st.success("PDF Generated Successfully!")
            st.write("Download file:", file_path)

        except:
            st.error("Error generating PDF. AI output issue.")