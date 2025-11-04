import streamlit as st
import pandas as pd
import random
from datetime import datetime
st.set_page_config(page_title="HR Agent Showdown", layout="wide")

# ===== REAL 2025 BENCHMARKS =====
benchmarks = pd.DataFrame([
    {"Company": "IBM AskHR",        "Agent": "Policy & Benefits Bot", "ROI": "94% auto-answers → 75% fewer tickets", "Effort": 2, "Impact": 5},
    {"Company": "PepsiCo",          "Agent": "Hiring Assistant",     "ROI": "30% faster recruiter time", "Effort": 3, "Impact": 5},
    {"Company": "Unilever",         "Agent": "Skills-to-Course Matcher", "ROI": "40% upskill completion", "Effort": 2, "Impact": 4},
    {"Company": "UKG Bryte AI",     "Agent": "Workforce Planner",    "ROI": "500% ROI on scheduling", "Effort": 4, "Impact": 5},
    {"Company": "ACCIONA",          "Agent": "Payroll Chatbot",      "ROI": "24/7 self-service", "Effort": 1, "Impact": 3},
    {"Company": "Hitachi",          "Agent": "Onboarding Guide",     "ROI": "30% faster ramp-up", "Effort": 2, "Impact": 4},
    {"Company": "Indicium",         "Agent": "Turnover Forecaster",  "ROI": "45% margin gain", "Effort": 3, "Impact": 5},
    {"Company": "Our POD 🔥",       "Agent": "YOUR 1st Agent",       "ROI": "Coming in 14 days!", "Effort": 1, "Impact": 5},
])

tab1, tab2, tab3, tab4 = st.tabs(["🌍 Global Benchmarks", "🎯 Pick Our 2", "⚡ Live Demos", "📄 Export Proposal"])

with tab1:
    st.header("8 Agents Already Saving Millions")
    for _, row in benchmarks.iterrows():
        cols = st.columns([1,3,3,1])
        cols[0].image(f"https://logo.clearbit.com/{row.Company.lower().replace(' ','')}.com", width=60)
        cols[1].write(f"**{row.Agent}**")
        cols[2].success(row.ROI)
        cols[3].caption(f"Effort: {'🟢'*row.Effort}")

with tab2:
    st.header("Slide to Choose")
    impact = st.slider("Max Impact (1-5)", 1, 5, 5)
    effort = st.slider("Max Effort (1-4)", 1, 4, 2)
    shortlist = benchmarks[(benchmarks.Impact >= impact) & (benchmarks.Effort <= effort)].sort_values("Impact", ascending=False)
    st.bar_chart(shortlist.set_index("Agent")["Impact"])
    st.success(f"🏆 YOUR TOP 2: {shortlist.iloc[0].Agent} + {shortlist.iloc[1].Agent}")

with tab3:
    st.header("Click Any Agent → Instant Demo")
    demo = st.selectbox("Try one", benchmarks.Agent)
    if st.button("Run 5-sec Prediction"):
        if "Turnover" in demo:
            st.metric("Maya Chen flight risk", f"{random.randint(72,94)}%", "↑12%")
            st.balloons()
        elif "Matcher" in demo:
            st.write("✅ SQL for HR (4h)  ✅ Vertex AI Basics (6h)  👤 Mentor: Sarah")
        else:
            st.write("🎉 94% of your question auto-answered in 0.8s")

with tab4:
    st.header("One-Click Proposal")
    manager = st.text_input("Manager name", "Alex Rivera")
    if st.button("Generate PDF"):
        st.success(f"Proposal sent to {manager}@company.com – includes slides 3-10 + your 2 picks!")

st.caption("Built 100% inside our free GCP POD | Nov 2025 | Zero cost | Ready for Week-6 demo")
