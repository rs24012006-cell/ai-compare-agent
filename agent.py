import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Extract technical skills from this text:\n{text}"
            }
        ]
    )
    return response.choices[0].message.content


# ---------------- SKILL COMPARISON ----------------
def compare_skills(jd, resume):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
Compare Job Description and Resume.

Return ONLY valid JSON like this:
{{
  "matched": ["skill1", "skill2"],
  "missing": ["skill3", "skill4"],
  "weak": ["skill5"]
}}

JD:
{jd}

Resume:
{resume}
"""
            }
        ]
    )
    return response.choices[0].message.content


# ---------------- INTERVIEW QUESTION ----------------
def generate_question(skill):
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Ask one technical interview question for {skill}"
            }
        ]
    )
    return response.choices[0].message.content


# ---------------- ANSWER EVALUATION ----------------
def evaluate_answer(question, answer):
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
Evaluate this answer:

Question: {question}
Answer: {answer}

Give:
- score out of 10
- short feedback
"""
            }
        ]
    )
    return response.choices[0].message.content

def generate_learning_plan(missing_skills):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
Create a structured learning plan for these skills:

{missing_skills}

Include:
- 7 day roadmap
- daily tasks
- best free resources
- estimated time per topic
"""
            }
        ]
    )
    return response.choices[0].message.content


def calculate_resume_score(jd, resume):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
Compare Job Description and Resume and give a score out of 100.

JD:
{jd}

Resume:
{resume}

Return ONLY:
- Score (0-100)
- Short reason (2-3 lines)
"""
            }
        ]
    )
    return response.choices[0].message.content