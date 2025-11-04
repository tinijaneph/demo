# streamlit_app.py
# HR Co-Pilot – 5 High-Impact GCP Agents
# Built for HR domain pilot (Vertex AI + BigQuery foundation)
import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="HR Co-Pilot – 5 Agents", layout="wide")
st.title("HR Co-Pilot – 5 High-Impact Agents (GCP HR Pod)")
st.caption("Powered by Vertex AI, BigQuery & Looker Studio | Demo by Doanh Pham")

# ─────────────────── MOCK DATA ───────────────────
employees = pd.DataFrame([
    {"id": "E101", "name": "Maya Chen", "dept": "Sales", "tenure": 14, "rating": 4.2, "ot": 28, "risk": 78, "sentiment": 0.42},
    {"id": "E102", "name": "Liam Park", "dept": "Engineering", "tenure": 36, "rating": 4.8, "ot": 12, "risk": 22, "sentiment": 0.81},
    {"id": "E103", "name": "Sofia Patel", "dept": "Finance", "tenure": 8, "rating": 3.1, "ot": 65, "risk": 91, "sentiment": 0.33},
])
courses = ["People Analytics 101", "Vertex AI for HR", "Data Storytelling for Leaders"]
policies = {
    "vacation": "Employees are entitled to 20 days of paid vacation annually.",
    "parental": "14 weeks fully paid parental leave + 4 weeks flexible option.",
    "remote": "Hybrid policy: minimum 2 days in office; flexible Fridays.",
    "benefits": "Health, dental, vision, 401k matching, and annual wellness stipend."
}

# ─────────────────── TABS ───────────────────
tabs = st.tabs([
    "1️⃣ Attrition Prediction",
    "2️⃣ Sentiment & Engagement",
    "3️⃣ Time & Workforce Analytics",
    "4️⃣ Training & Development Recommender",
    "5️⃣ HR Policy & Benefits Copilot"
])

# ── 1️⃣ ATTRITION PREDICTION ─────────────────────────
with tabs[0]:
    st.header("Agent 1: Attrition Prediction")
    st.write("Predict which employees are most likely to leave and why.")
    emp = st.selectbox("Select Employee", employees["name"], key="attrition")
    if st.button("Run Prediction", key="attr_btn"):
        row = employees[employees["name"] == emp].iloc[0]
        risk = row["risk"] + random.randint(-5, 5)
        st.metric("Attrition Risk", f"{risk}%", delta=f"{random.choice(['+3%', '-2%', '+6%'])}")
        if risk > 70:
            st.warning(f"⚠️ High risk detected for {emp}. Recommended: career chat, mentor match, learning incentive.")
        else:
            st.success(f"{emp} shows stable retention outlook.")
        st.bar_chart({"Performance": row["rating"]*20, "Engagement": row["sentiment"]*100, "Tenure": row["tenure"]})

# ── 2️⃣ SENTIMENT & ENGAGEMENT MONITOR ─────────────────────────
with tabs[1]:
    st.header("Agent 2: Sentiment & Engagement Monitor")
    st.write("Use NLP to analyze employee sentiment from surveys or feedback.")
    comment = st.text_area("Paste a recent myPulse comment:", "Feeling burned out lately with extra hours.")
    if st.button("Analyze Sentiment", key="sentiment"):
        score = random.randint(45, 90)
        st.metric("Sentiment Score", f"{score}%", delta=f"{random.choice(['+4%', '-6%'])}")
        if score < 60:
            st.error("Negative sentiment detected → Notify HR Business Partner.")
        elif score < 75:
            st.warning("Neutral to mixed tone → Recommend pulse follow-up survey.")
        else:
            st.success("Positive sentiment detected.")
        st.line_chart([random.randint(40, 85) for _ in range(6)])

# ── 3️⃣ TIME & WORKFORCE ANALYTICS ─────────────────────────
with tabs[2]:
    st.header("Agent 3: Time & Workforce Analytics")
    st.write("Monitor overtime, fatigue, and absenteeism trends.")
    emp = st.selectbox("Choose Employee", employees["name"], key="time")
    if st.button("Generate Report", key="time_btn"):
        row = employees[employees["name"] == emp].iloc[0]
        st.metric("Overtime Hours (This Month)", f"{row['ot']} hrs", "↑5h vs last month")
        if row["ot"] > 40:
            st.warning("⚠️ Fatigue risk detected → Recommend auto-rest scheduling.")
        else:
            st.success("Workload normal range.")
        st.bar_chart({"Week1": 8, "Week2": 12, "Week3": 10, "Week4": 6})

# ── 4️⃣ TRAINING & DEVELOPMENT RECOMMENDER ─────────────────────────
with tabs[3]:
    st.header("Agent 4: Training & Development Recommender")
    st.write("Recommend personalized learning and mentorship options.")
    goal = st.text_input("Career goal / next role:", "People Analytics Lead")
    if st.button("Generate Development Plan", key="train_btn"):
        recs = random.sample(courses, 2)
        st.success(f"Recommended learning for '{goal}'")
        for r in recs:
            st.write(f"📘 {r} – [Enroll]")
        st.write(f"👥 Mentor matched: {random.choice(['Sarah', 'Raj', 'Ana'])}")

# ── 5️⃣ HR POLICY & BENEFITS COPILOT ─────────────────────────
with tabs[4]:
    st.header("Agent 5: HR Policy & Benefits Copilot")
    st.write("Ask questions about HR policies and get instant, compliant answers.")
    q = st.text_input("Ask HR Copilot", "How much parental leave do we have?")
    if st.button("Get Answer", key="policy_btn"):
        found = None
        for k, v in policies.items():
            if k in q.lower():
                found = v
                break
        if found:
            st.success(found)
        else:
            st.info("Policy not found – forwarding to HR shared inbox.")
    st.metric("Response Accuracy (Pilot)", "93%")
    st.metric("Tickets Deflected", "88%")

st.markdown("---")
st.caption("Demo: 5 HR AI Agents | Built for GCP Vertex AI + BigQuery pilot | © 2025 Doanh Pham")
