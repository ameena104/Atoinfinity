import streamlit as st
import google.generativeai as genai

# UI Setup
st.set_page_config(page_title="Career Agent", layout="wide")
st.title("🚀 Capability Intelligence Platform")

# Sidebar for Setup
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    target_role = st.text_input("Target Job Title (e.g., Senior Data Scientist)")
    target_company = st.text_input("Target Company (Optional)")

# Main Input
user_skills = st.text_area("List your current skills/experience:")

if st.button("Generate Roadmap"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a Career Architect. Analyze the gap between:
        Current Skills: {user_skills}
        Target Role: {target_role} at {target_company}
        
        Provide:
        1. Skill Gap Analysis (Market Benchmarked)
        2. 30-60-90 Day Adaptive Roadmap
        3. Behavioral Confidence Tip
        4. Specific Company Alignment Advice
        """
        
        with st.spinner("Agent analyzing market data..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)