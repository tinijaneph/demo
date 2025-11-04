# streamlit_app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="HR Co-Pilot", layout="wide")
st.title("HR Co-Pilot – LIVE in our GCP POD")
st.markdown("**Zero cost | 2 agents | 14-day MVP**")

# MOCK DATA (replace later with real BQ)
employees = pd.DataFrame([
    {"emp_id": "E12345", "name": "Maya Chen", "tenure_months": 14, "last_rating": 4.2, "overtime_hrs": 28, "risk": 78},
    {"emp_id": "E12346", "name": "Liam Park", "tenure_months": 36, "last_rating": 4.8, "overtime_hrs": 12, "risk": 22},
    {"emp_id": "E12347", "name": "Sofia Patel", "tenure_months": 8, "last_rating": 3.1, "overtime_hrs": 65, "risk": 91},
])

courses = ["SQL for HR", "People Analytics 101", "Vertex AI Basics", "Predictive HR"]
mentors = ["Sarah (HR Tech Lead)", "Raj (Data Science)", "Ana (L&D Director)"]

tab1, tab2, tab3 = st.tabs(["Attrition Radar", "Skill Spark", "ROI Calculator"])

with tab1:
    st.header("Attrition Radar")
    emp_id = st.selectbox("Pick an employee", employees["emp_id"] + " – " + employees["name"])
    if st.button("Run Prediction"):
        row = employees[employees["emp_id"] == emp_id.split()[0]].iloc[0]
        risk = row["risk"] + random.randint(-5, 8)
        st.metric("Flight Risk", f"{risk}%", delta=f"{random.choice(['-12%', '+5%', '-8%'])} vs last month")
        
        st.subheader("3 Instant Retention Actions")
        actions = [
            "Schedule 1:1 coffee chat (auto-book in Outlook)",
            "Offer $500 LinkedIn Learning budget",
            "Fast-track to mentor program"
        ]
        for a in actions:
            st.write(f"→ {a}")

with tab2:
    st.header("Skill Spark")
    goal = st.text_input("Your career goal", "Become a People Analytics Lead")
    if st.button("Generate My 90-Day Path"):
        st.success("Your Personalized Upskilling Plan")
        for c in random.sample(courses, 3):
            st.write(f"Course: {c} – 4 hrs – [Enrol](#)")
        st.write("**Recommended Mentors**")
        for m in random.sample(mentors, 2):
            st.write(f"Mentor: {m} – [Book 15-min intro](#)")

with tab3:
    st.header("Live ROI Calculator")
    saved = st.slider("Employees you retain", 0, 50, 12)
    cost_per_hire = st.number_input("Avg replacement cost ($)", 15000, 30000, 20000)
    st.metric("Year-1 Savings", f"${saved * cost_per_hire:,.0f}")
    st.balloons()

st.caption("Built by [Your Name] | Runs 100% inside our free GCP POD | Ready for Week-6 demo")
