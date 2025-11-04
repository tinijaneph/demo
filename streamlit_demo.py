# streamlit_app.py
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="HR Co-Pilot MVP", layout="wide")
st.title("HR Co-Pilot – LIVE in our Free GCP POD")
st.markdown("**Zero cost | 14-day MVP | 4 agents | $720K Year-1 impact**")

# MOCK DATA (replace with BigQuery later)
employees = pd.DataFrame([
    {"id": "E12345", "name": "Maya Chen",    "dept": "Sales",     "tenure":14, "rating":4.2, "ot":28,  "risk":78, "email":"maya@company.com"},
    {"id": "E12346", "name": "Liam Park",    "dept": "Eng",       "tenure":36, "rating":4.8, "ot":12,  "risk":22, "email":"liam@company.com"},
    {"id": "E12347", "name": "Sofia Patel",   "dept": "Finance",   "tenure":8,  "rating":3.1, "ot":65,  "risk":91, "email":"sofia@company.com"},
])

courses = ["SQL for HR", "Vertex AI Basics", "People Analytics 101", "Predictive HR"]
mentors = ["Sarah (HR Tech)", "Raj (Data Science)", "Ana (L&D)"]

tab1, tab2, tab3, tab4 = st.tabs([
    "Attrition Radar", "Skill Spark", "Policy Bot", "Onboarding Guide"
])

# ────────────────────── 1. ATTRITION RADAR ──────────────────────
with tab1:
    st.header("Attrition Radar")
    st.write("Predict who’s leaving — 60 days early")
    emp = st.selectbox("Select employee", employees["id"] + " – " + employees["name"], key="a")
    if st.button("Run Prediction", key="a1"):
        row = employees[employees["id"] == emp.split()[0]].iloc[0]
        risk = row["risk"] + random.randint(-7, 9)
        st.metric("Flight Risk", f"{risk}%", delta=f"{random.choice(['-12%', '+5%', '-8%'])} vs last month")
        
        st.subheader("3 Instant Retention Actions")
        actions = [
            "Schedule 1:1 coffee chat (auto-book Outlook)",
            "Offer $500 LinkedIn Learning budget",
            "Fast-track to mentor program"
        ]
        for a in actions:
            st.write(f"→ {a}")
        
        if st.button("Send Alert Email to Manager", key="a2"):
            st.success(f"Email sent to {row.name}'s manager:\n\nSubject: Retention Alert – {row.name}\nRisk: {risk}%\nActions booked automatically.")
            st.balloons()

# ────────────────────── 2. SKILL SPARK ──────────────────────
with tab2:
    st.header("Skill Spark")
    st.write("Turn any goal into a 90-day upskill plan")
    goal = st.text_input("Your next role", "Become a People Analytics Lead", key="s1")
    if st.button("Generate My Path", key="s2"):
        st.success("Personalized 90-Day Upskilling Plan")
        for c in random.sample(courses, 3):
            st.write(f"Course: {c} – 4 hrs – [Enrol Now](#)")
        st.write("**Recommended Mentors**")
        for m in random.sample(mentors, 2):
            st.write(f"Mentor: {m} – [Book 15-min](#)")
        
        if st.button("Email Plan to Myself", key="s3"):
            st.success(f"90-day plan emailed to you!\n\nGoal: {goal}\n3 courses + 2 mentors booked.")
            st.download_button("Download PDF Plan", "Your_90_Day_Plan.pdf")

# ────────────────────── 3. POLICY BOT (ADVANCED) ──────────────────────
with tab3:
    st.header("Policy & Benefits Bot")
    st.write("94% of questions answered in 0.8s — with auto-email")
    question = st.text_input("Ask HR anything", "How much paternity leave?", key="p1")
    manager_email = st.text_input("Your manager's email (optional)", "alex@company.com", key="p2")
    
    if st.button("Get Answer + Email", key="p3"):
        answers = {
            "paternity": "14 weeks fully paid + 4 weeks flexible",
            "bonus": "Paid March 15th, avg $4,200 net",
            "remote": "Up to 3 days/week, equipment provided",
            "learning": "$1,000 annual budget, no approval needed"
        }
        q = question.lower()
        answer = next((v for k, v in answers.items() if k in q), "I found this in the handbook →")
        
        st.success(f"**Answer:** {answer}")
        st.metric("HR tickets deflected", "94%", "75% fewer calls")
        
        if st.button("Send Answer to My Manager", key="p4"):
            st.success(f"Policy email sent to {manager_email}\n\nSubject: HR Policy – {question}\nAnswer: {answer}\nLink to full handbook attached.")
            st.balloons()

# ────────────────────── 4. ONBOARDING GUIDE (ADVANCED) ──────────────────────
with tab4:
    st.header("Onboarding Guide")
    st.write("30% faster ramp-up — fully automated")
    name = st.text_input("New hire name", "Alex Rivera", key="o1")
    start_date = st.date_input("Start date", datetime.today() + timedelta(days=7), key="o2")
    
    if st.button("Launch 30-Day Journey", key="o3"):
        st.success(f"Welcome {name}! Your journey starts {start_date.strftime('%b %d')}")
        timeline = [
            ("Day 0", "Laptop shipped + IT access"),
            ("Day 1", "Welcome lunch + Team intro"),
            ("Day 3", "1:1 with manager (booked)"),
            ("Day 7", "HR training + Benefits enrolled"),
            ("Day 14", "First project assigned"),
            ("Day 30", "30-day check-in + feedback")
        ]
        for day, task in timeline:
            st.write(f"**{day}** → {task}")
        
        if st.button("Email Full Plan to New Hire", key="o4"):
            st.success(f"Onboarding plan emailed to {name}!\nCalendar invites sent.\nLaptop tracking: In transit.")
            st.image("https://i.imgur.com/8Q8.jpg", caption="Welcome kit shipped!", width=300)

st.caption("Built by [Your Name] | 100% free GCP POD | Week-6 demo ready | Pick any 2 → live in 14 days")
