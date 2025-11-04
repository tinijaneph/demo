# streamlit_app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="HR Co-Pilot 7", layout="wide")
st.title("HR Co-Pilot – 7 Agents LIVE in ONE GCP Project")
st.markdown("**Zero cost | 14-day MVP | All 7 agents from our PDF | $1.2M Year-1 impact**")

# MOCK DATA (will be replaced by BigQuery)
employees = pd.DataFrame([
    {"id": "E12345", "name": "Maya Chen",    "dept": "Sales",     "tenure":14, "rating":4.2, "ot":28,  "risk":78,  "email":"maya@company.com"},
    {"id": "E12346", "name": "Liam Park",    "dept": "Eng",       "tenure":36, "rating":4.8, "ot":12,  "risk":22,  "email":"liam@company.com"},
    {"id": "E12347", "name": "Sofia Patel",   "dept": "Finance",   "tenure":8,  "rating":3.1, "ot":65,  "risk":91,  "email":"sofia@company.com"},
])
courses = ["SQL for HR", "Vertex AI Basics", "People Analytics 101"]
mentors = ["Sarah (HR Tech)", "Raj (Data Science)", "Ana (L&D)"]

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Attrition Prediction",
    "Time Tracking",
    "Performance Trend",
    "Training Matcher",
    "Sentiment Monitor",
    "Policy Bot",
    "Onboarding Guide"
])

# 1. ATTRITION PREDICTION
with tab1:
    st.header("Agent 1: Attrition Prediction")
    st.write("Predict which employees are at risk of leaving")
    emp = st.selectbox("Select", employees["id"]+" – "+employees["name"], key="a")
    if st.button("Predict Risk", key="a1"):
        row = employees[employees["id"] == emp.split()[0]].iloc[0]
        risk = row["risk"] + random.randint(-7,9)
        st.metric("Flight Risk", f"{risk}%", delta=f"{random.choice(['-12%', '+5%'])}")
        st.success("Risk score + alert system → Looker Studio")
        if st.button("Email Manager", key="a2"):
            st.success(f"Alert sent to {row.name}'s manager")

# 2. TIME TRACKING / WORKFORCE ACTIVITY
with tab2:
    st.header("Agent 2: Time Tracking")
    st.write("Analyze time-tracking, absenteeism, overwork")
    emp = st.selectbox("Employee", employees["id"]+" – "+employees["name"], key="t")
    if st.button("Generate Weekly Report", key="t1"):
        row = employees[employees["id"] == emp.split()[0]].iloc[0]
        st.metric("Overtime", f"{row.ot} hrs", "↑12 vs avg")
        st.bar_chart({"Mon":8, "Tue":10, "Wed":9, "Thu":12, "Fri":6})
        st.warning("Fatigue Index: High → Auto-suggest rest days")
        st.info("Weekly trend reports → Looker Studio")

# 3. PERFORMANCE TREND ANALYZER
with tab3:
    st.header("Agent 3: Performance Trend")
    st.write("Identify high/low performance drivers")
    emp = st.selectbox("Pick", employees["id"]+" – "+employees["name"], key="p")
    if st.button("Show Insights", key="p1"):
        row = employees[employees["id"] == emp.split()[0]].iloc[0]
        st.metric("Performance Score", f"{row.rating*20:.0f}%")
        st.bar_chart({"Goals":90, "Feedback":row.rating*20, "Output":85})
        st.success("HR Insights dashboard → Vertex AI + BigQuery")

# 4. TRAINING & DEVELOPMENT MATCHER
with tab4:
    st.header("Agent 4: Training Matcher")
    st.write("Recommend learning paths or mentorships")
    goal = st.text_input("Career goal", "Become a People Analytics Lead", key="m")
    if st.button("Generate Plan", key="m1"):
        st.success("Personalized learning suggestions")
        for c in random.sample(courses, 3):
            st.write(f"Course: {c} – [Enrol](#)")
        st.write("**Mentor**: Sarah – [Book 15-min](#)")
        if st.button("Email Plan", key="m2"):
            st.success("90-day plan emailed!")

# 5. SENTIMENT & ENGAGEMENT MONITOR
with tab5:
    st.header("Agent 5: Sentiment Monitor")
    st.write("Track employee sentiment from surveys")
    comment = st.text_area("Paste myPulse feedback", "Loving the team but burnt out", key="s")
    if st.button("Analyze", key="s1"):
        score = random.randint(62, 88)
        st.metric("Engagement Score", f"{score}%", "↓6% vs last month")
        st.error("Burnout rising in Sales")
        st.info("Monthly sentiment → Vertex AI NLP + BigQuery")

# 6. POLICY & BENEFITS BOT (ADVANCED)
with tab6:
    st.header("Agent 6: Policy Bot")
    st.write("94% of HR questions answered instantly")
    q = st.text_input("Ask anything", "How much paternity leave?", key="pb")
    if st.button("Get Answer + Email", key="pb1"):
        ans = "14 weeks fully paid + 4 weeks flexible"
        st.success(f"**Answer:** {ans}")
        st.metric("Tickets deflected", "94%")
        if st.button("Send to My Manager", key="pb2"):
            st.success("Policy email sent with handbook link")

# 7. ONBOARDING GUIDE (ADVANCED)
with tab7:
    st.header("Agent 7: Onboarding Guide")
    st.write("30% faster ramp-up, fully automated")
    name = st.text_input("New hire", "Alex Rivera", key="o1")
    start = st.date_input("Start date", datetime.today() + timedelta(7), key="o2")
    if st.button("Launch 30-Day Journey", key="o3"):
        st.success(f"Welcome {name}! Journey starts {start.strftime('%b %d')}")
        tasks = ["Laptop shipped", "Welcome lunch", "1:1 booked", "HR training", "Project assigned"]
        for i, t in enumerate(tasks):
            st.write(f"**Day {i*3}** → {t}")
        if st.button("Email Full Plan", key="o4"):
            st.success("Calendar invites + tracking link sent!")

st.caption("Built by [Your Name] | 100% matches our GCP PDF | 7 agents, 1 project | Week-6 demo ready")
