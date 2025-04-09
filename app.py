import streamlit as st

try:
    st.write("✅ API Key:", st.secrets["api_key"])
except KeyError:
    st.error("❌ Gemini API Key not found in Streamlit secrets.")
