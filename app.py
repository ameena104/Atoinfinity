import os
import streamlit as st
import google.generativeai as genai

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="Atoinfinity", layout="wide")
st.title("🚀 Atoinfinity: Capability Intelligence")

# ----------------------------
# Secrets / env key (NO UI input)
# ----------------------------
api_key = os.getenv("Gemini_API")
if not api_key:
st.error(
"Missing environment variable **Gemini_API**.\n\n"
"- If using GitHub: add it as a Secret named `Gemini_API`\n"
"- If deploying (Streamlit Cloud/Render/Azure): set `Gemini_API` as an environment variable"
)
st.stop()

# Configure Gemini once
try:
genai.configure(api_key=api_key)
except Exception as e:
st.error(f"Failed to configure Gemini API: {e}")
st.stop()

# ----------------------------
# Sidebar inputs
# ----------------------------
with st.sidebar:
st.header("Setup")

role = st.text_input("Target Job Role", placeholder="e.g., Cloud Infrastructure Engineer")
company = st.text_input("Target Company (Optional)", placeholder="e.g., FBD Insurance / Google / Amazon")
experience_level = st.selectbox(
"Experience Level",
["Entry Level", "Mid Level", "Senior Level", "Architect/Leadership"],
index=2,
)

output_style = st.selectbox(
"Output Style",
["Concise (bullet points)", "Detailed (with examples)"],
index=0,
)

model_name = st.selectbox(
"Model",
["gemini-2.0-flash-lite", "gemini-2.0-flash"],
index=0,
help="Flash is usually higher quality but may be slower/costlier depending on your plan.",
)

temperature = st.slider(
"Creativity (temperature)",
min_value=0.0,
max_value=1.0,
value=0.6 if "Concise" in output_style else 0.75,
step=0.05,
)

# ----------------------------
# Main input
# ----------------------------
user_input = st.text_area(
"Current Skills & Experience",
height=220,
placeholder="Paste your skills, projects, tools, years of experience, achievements, and responsibilities…",
)

col1, col2 = st.columns([1, 1])

with col1:
generate = st.button("Generate Strategy", type="primary")

with col2:
st.caption("Tip: include tools, years, project impact (time saved, cost reduced), and incidents handled.")

# ----------------------------
# Prompt builder
# ----------------------------
def build_prompt(role: str, company: str, experience_level: str, user_input: str, output_style: str) -> str:
detail_hint = (
"Keep it crisp and bullet-heavy."
if "Concise" in output_style
else "Add brief examples and a bit more explanation where useful."
)

company_line = f"Target Company: {company}" if company.strip() else "Target Company: (not specified)"

return f"""
You are a senior career strategist and enterprise technology mentor.

Target Role: {role}
{company_line}
Experience Level: {experience_level}

Candidate Profile:
{user_input}

Deliverables (use markdown headings '##' and bullet points):
1) Readiness score /100 with 3 reasons.
2) Strengths (5 bullets).
3) Skill gaps: Must-have vs Nice-to-have (role aligned).
4) 30-60-90 day roadmap with weekly actions (realistic and measurable).
5) 3 portfolio projects (each with outcomes + suggested tech stack + what to showcase).
6) Certifications (only if genuinely useful; avoid unnecessary ones).
7) Interview prep plan: system design + behavioral + role-specific questions.
8) A 1-minute elevator pitch tailored to the role.

Guidance:
- Avoid generic advice; be concrete and actionable.
- Prefer outcomes, metrics, and artifacts (docs, diagrams, GitHub, runbooks).
- {detail_hint}
""".strip()

# ----------------------------
# Generate
# ----------------------------
if generate:
if not role.strip() or not user_input.strip():
st.warning("Please fill in **Target Job Role** and **Current Skills & Experience**.")
st.stop()

prompt = build_prompt(role, company, experience_level, user_input, output_style)

try:
model = genai.GenerativeModel(
model_name=model_name,
generation_config={
"temperature": float(temperature),
"top_p": 0.9,
"max_output_tokens": 2048,
},
)

with st.spinner("Analyzing..."):
response = model.generate_content(prompt)

text = getattr(response, "text", None)
if not text:
st.error("No text received from the model. Try again or switch model.")
st.stop()

st.success("Strategy generated!")
st.markdown(text)

# Optional: download as markdown
st.download_button(
label="Download as Markdown",
data=text.encode("utf-8"),
file_name="atoinfinity_strategy.md",
mime="text/markdown",
)

except Exception as e:
st.error(f"API Error: {str(e)}")
