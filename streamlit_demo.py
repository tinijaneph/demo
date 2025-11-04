# streamlit_app.py
import streamlit as st
import pandas as pd
import random
from google.cloud import bigquery

st.set_page_config(page_title="HR Co-Pilot", layout="wide")
st.title("🔮 HR Co-Pilot – Live in our GCP POD")

bq = bigquery.Client()

tab1, tab2 = st.tabs(["Attrition Radar", "Skill Spark"])

with tab1:
    emp_id = st.text_input("Employee ID", "E12345")
    if st.button("Predict Risk"):
        # Mock query – replace with real BQ table
        sql = f"SELECT tenure_months, last_rating, overtime_hrs FROM `hr_dataset.employees` WHERE emp_id='{emp_id}'"
        df = bq.query(sql).to_dataframe()
        if df.empty:
            st.error("ID not found – try E12345")
        else:
            row = df.iloc[0]
            risk = min(99, int(15 + row.tenure_months*0.5 + (5-row.last_rating)*10 + row.overtime_hrs*0.3))
            st.metric("Flight Risk", f"{risk}%", delta=f"{random.randint(5,15)}% vs last month")
            st.write("**3 Retention Ideas**")
            st.write("1. Schedule 1:1 with manager")
            st.write("2. Offer LinkedIn Learning budget")
            st.write("3. Fast-track to mentor program")

with tab2:
    goal = st.text_input("Career goal", "Become a People Analytics Lead")
    if st.button("Find My Path"):
        courses = ["SQL for HR", "Vertex AI Basics", "Predictive Analytics"]
        mentors = ["Sarah (HR Tech)", "Raj (Data Science)"]
        st.success("Your 90-day plan")
        for c in courses:
            st.write(f"✅ {c} – 4 hrs – [Enrol](#)")
        st.write("**Mentors**")
        for m in mentors:
            st.write(f"👤 {m} – [Book 15 min](#)")

st.caption("Built on Vertex AI + BigQuery – zero extra cost")
