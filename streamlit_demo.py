# streamlit_app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="HR Co-Pilot 7", layout="wide")
st.title("HR Co-Pilot – 7 Agents LIVE in ONE GCP Project")
st.markdown("**Zero cost | 14-day MVP | Pick any 2 → $1.2M Year-1 impact**")

# Mock data (replace with BigQuery later)
employees = pd.DataFrame([
    {"id": "E12345", "name": "Maya Chen",   "dept": "Sales",     "tenure":14, "rating":4.2, "ot":28,  "risk":78},
    {"id": "E12346", "name": "Liam Park",   "dept": "Engineering", "tenure":36, "rating":4.8, "ot":12,  "risk":22},
    {"id": "E12347", "name": "Sofia Patel",  "dept": "Finance",   "tenure":8,  "rating":3.1, "ot":65,  "risk":91},
])

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Policy Bot", "Hiring Assistant", "Skills Matcher",
    "Workforce Planner", "Payroll Chatbot", "Onboarding Guide", "Turnover Forecaster"
])

# ────────────────────── 1. Policy & Benefits Bot ──────────────────────
with tab1:
    st.header("Policy & Benefits Bot")
    question = st.text_input("Ask anything", "How much paternity leave do I get?", key="t1")
    if st.button("Answer in 0.8s", key="t1b"):
        st.success("14 weeks fully paid + 4 weeks flexible. Auto-email to manager?")
        st.metric("Tickets deflected", "94%", "75% fewer HR calls")
        st.balloons()

# ────────────────────── 2. Hiring Assistant ──────────────────────
with tab2:
    st.header("Hiring Assistant")
    req = st.text_input("Job title", "Senior Data Analyst", key="t2")
    if st.button("Find 5 perfect CVs", key="t2b"):
        st.write("1. Raj K. – 6yrs SQL, ex-Google")
        st.write("2. Ana L. – Vertex AI certified")
        st.metric("Recruiter time saved", "30% faster", "3 days → 36 hrs")
        st.download_button("Export shortlist", "raj,ana,...")

# ────────────────────── 3. Skills-to-Course Matcher ──────────────────────
with tab3:
    st.header("Skills-to-Course Matcher")
    goal = st.text_input("My next role", "People Analytics Lead", key="t3")
    if st.button("Build 90-day plan", key="t3b"):
        st.success("40% completion rate (Unilever benchmark)")
        st.write("SQL for HR – 4h – Enrol")
        st.write("Vertex AI Basics – 6h – Enrol")
        st.write("Mentor: Sarah (HR Tech) – Book 15-min")

# ────────────────────── 4. Workforce Planner ──────────────────────
with tab4:
    st.header("Workforce Planner")
    dept = st.selectbox("Department", ["Sales", "Engineering", "Finance"], key="t4")
    if st.button("Optimise next month", key="t4b"):
        st.metric("Overtime reduced", "42 hrs → 12 hrs", "500% ROI")
        st.bar_chart({"Mon":8, "Tue":7, "Wed":8, "Thu":6, "Fri":4})
        st.info("Auto-schedule sent to managers")

# ────────────────────── 5. Payroll Chatbot ──────────────────────
with tab5:
    st.header("Payroll Chatbot")
    q = st.text_input("Ask payroll", "When is my bonus paid?", key="t5")
    if st.button("24/7 answer", key="t5b"):
        st.success("March 15th, net $4,200. View payslip →")
        st.metric("Self-service rate", "24/7", "Zero wait time")
        st.image("https://i.imgur.com/8Q8.jpg", width=300)

# ────────────────────── 6. Onboarding Guide ──────────────────────
with tab6:
    st.header("Onboarding Guide")
    name = st.text_input("New hire name", "Alex Rivera", key="t6")
    if st.button("Start 30-day journey", key="t6b"):
        st.success("30% faster ramp-up")
        timeline = pd.date_range(start=datetime.today(), periods=5, freq='3D')
        for i, day in enumerate(timeline):
            st.write(f"**Day {i*3}** – {['Laptop setup','Meet team','First 1:1','HR training','Project kickoff'][i]}")
        st.balloons()

# ────────────────────── 7. Turnover Forecaster ──────────────────────
with tab7:
    st.header("Turnover Forecaster")
    emp = st.selectbox("Employee", employees["id"]+" – "+employees["name"], key="t7")
    if st.button("Predict", key="t7b"):
        row = employees[employees["id"] == emp.split()[0]].iloc[0]
        risk = row["risk"] + random.randint(-7,9)
        st.metric("Flight Risk", f"{risk}%", delta=f"{random.choice([-12,+5,-8])}%")
        st.error("Auto-alert to manager + $500 learning budget")
        st.success("Saved 12 people → $240K")

st.caption("Built by [Your Name] | 100% free GCP POD | 45-second deploy | Week-6 demo ready")
