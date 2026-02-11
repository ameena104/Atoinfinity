import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Atoinfinity", layout="wide")
st.title("🚀 Atoinfinity: Capability Intelligence")

with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Paste Gemini API Key:", type="password")
    role = st.text_input("Target Job Role:")
    company = st.text_input("Target Company:")

user_input = st.text_area("Current Skills & Experience:")

if st.button("Generate Strategy"):
    if not api_key or not user_input or not role:
        st.warning("Please fill in the API Key, Target Role, and your Skills.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            full_prompt = f"Role: {role}\nCompany: {company}\nSkills: {user_input}\nAnalyze gaps and provide a 30-60-90 day roadmap."
            
            with st.spinner("Analyzing..."):
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
        except Exception as e:
            st.error(f"API Error: {str(e)}")