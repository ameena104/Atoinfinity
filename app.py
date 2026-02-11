import os
import streamlit as st
import google.generativeai as genai

# === PAGE SETUP ===
st.set_page_config(page_title="Atoinfinity", layout="wide")
st.title("🚀 Atoinfinity: Capability Intelligence")

# === GEMINI API SETUP ===
api_key = os.getenv("Gemini_API")
if not api_key:
    st.error("""
    **Missing Gemini_API environment variable**
    
    **GitHub Codespaces**: Add as Secret `Gemini_API`
    **Streamlit Cloud/Render**: Set as Environment Variable
    """)
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Gemini API config failed: {e}")
    st.stop()

# === SIDEBAR INPUTS ===
with st.sidebar:
    st.header("🎯 Setup")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Target Job Role", placeholder="Cloud Infrastructure Engineer")
    with col2:
        company = st.text_input("Target Company", placeholder="Google / Amazon")
    
    experience_level = st.selectbox(
        "Experience Level", 
        ["Entry", "Mid", "Senior", "Architect/Lead"],
        index=2
    )
    
    st.subheader("Output Style")
    output_style = st.radio(
        "Format", 
        ["📝 Concise (bullets)", "📚 Detailed (examples)"],
        horizontal=True
    )
    
    col3, col4 = st.columns(2)
    with col3:
        model_name = st.selectbox("Model", ["gemini-2.0-flash-lite", "gemini-2.0-flash"])
    with col4:
        temperature = st.slider("Creativity", 0.0, 1.0, 0.6, 0.05)

# === MAIN INPUT ===
col_a, col_b = st.columns([3, 1])
with col_a:
    user_input = st.text_area(
        "📋 Current Skills & Experience",
        height=200,
        placeholder="""• 5+ years infrastructure engineering
• Terraform, Kubernetes, AWS/GCP
• Led migration saving $200k/year
• Built CI/CD pipelines (GitHub Actions)
• On-call incident management..."""
    )
with col_b:
    st.info("💡 **Tip**: Include tools, years, metrics, projects")

# === ACTION BUTTONS ===
col_btn1, col_btn2 = st.columns([2, 1])
with col_btn1:
    generate = st.button("🚀 Generate Strategy", type="primary", use_container_width=True)
with col_btn2:
    st.caption("Include: tools, impact metrics, achievements")

# === PROMPT BUILDER ===
@st.cache_data
def build_prompt(role, company, experience_level, user_input, output_style):
    detail_hint = "📏 Keep crisp, bullet-heavy" if "Concise" in output_style else "💡 Add examples"
    company_line = f"Company: {company}" if company.strip() else "Company: Any"
    
    return f"""
**Senior Career Strategist** - Target: {role} ({experience_level}) at {company_line}

**Candidate Profile:**
{user_input}

**DELIVERABLES** (markdown ## headings + bullets):
1. Readiness Score /100 + 3 reasons
2. **Strengths** (top 5 bullets)  
3. **Skill Gaps**: Must-have vs Nice-to-have
4. **30-60-90 Day Roadmap** (weekly actions)
5. **3 Portfolio Projects** (outcomes + tech stack)
6. **Certifications** (only high-ROI ones)
7. **Interview Prep**: System design + behavioral
8. **1-Min Elevator Pitch**

**Style**: {detail_hint}
**Focus**: Concrete metrics, GitHub repos, outcomes
    """.strip()

# === GENERATE STRATEGY ===
if generate:
    if not role.strip() or not user_input.strip():
        st.warning("⚠️ Please add **Job Role** and **Your Skills**")
        st.stop()
    
    with st.spinner("🤖 Generating your career strategy..."):
        prompt = build_prompt(role, company, experience_level, user_input, output_style)
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt, generation_config={"temperature": temperature})
        
        st.markdown("## 🎯 **Your Career Strategy**")
        st.markdown(response.text)
        
        # Download button
        st.download_button(
            "💾 Download Strategy",
            response.text,
            f"atoinfinity-strategy-{role.replace(' ', '-')}.md",
            "text/markdown"
        )
