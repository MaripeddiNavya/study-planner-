# main.py

from studbud import get_study_plan  # Import the study plan function
import streamlit as st

st.title("📚 StudBud: AI Study Planner")

# Get user inputs
departments = ["Engineering", "Pharmacy", "Medical", "Arts", "Commerce", "Science", "Law", "Management", "Others"]
selected_department = st.selectbox("Select Your Department", departments)
user_query = st.text_area("🎯 Describe your study needs")

if st.button("📝 Generate Study Plan"):
    if user_query:
        study_plan = get_study_plan(selected_department, user_query)
        st.subheader("📅 Your AI-Generated Study Plan:")
        st.write(study_plan)
    else:
        st.warning("⚠️ Please enter your study preferences.")
