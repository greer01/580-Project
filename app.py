import streamlit as st
from src.db import add_golfer, list_golfers, get_golfer
from src.ai_coach import ask_ai_coach, generate_practice_plan, performance_audit

st.title("CaddySense Golf Performance AI Coach and Recommendation System")

menu = st.sidebar.selectbox(
    "Choose an option",
    [
        "Add Golfer",
        "View Golfers",
        "Ask AI Coach",
        "Generate Practice Plan",
        "Generate Performance Audit",
    ]
)