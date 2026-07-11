import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

# Try local .env first
api_key = os.getenv("GROQ_API_KEY")

# If deployed on Streamlit Cloud, use Streamlit Secrets
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("GROQ_API_KEY was not found.")
    st.stop()