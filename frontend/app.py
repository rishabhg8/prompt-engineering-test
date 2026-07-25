import os
import sys

# Ensure root workspace directory is on sys.path to prevent module collision
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from frontend.components.guardrail_checker import render_guardrail_checker
from frontend.components.mcq_quiz import render_mcq_quiz

st.set_page_config(
    page_title="Prompt Engineering Test",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject GitHub Dark Mode CSS stylesheet
css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state navigation
if "nav_choice" not in st.session_state:
    st.session_state["nav_choice"] = "🎯 Prompt Test"

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 🎯 Interview Platform")
    st.caption("Prompt Engineering Evaluation")
    st.markdown("---")
    
    choice = st.radio(
        "Modules",
        options=[
            "🎯 Prompt Test",
            "🧩 Diagnostic Quiz"
        ],
        index=0
    )
    st.session_state["nav_choice"] = choice
    st.markdown("---")
    st.caption("Candidate Evaluation Engine")

# --- MAIN CONTENT CONTROLLER ---
selected = st.session_state["nav_choice"]

if "Quiz" in selected or "MCQ" in selected:
    render_mcq_quiz()
else:
    render_guardrail_checker()
