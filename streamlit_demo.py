
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='HR Agents Demo', layout='wide')

st.title('HR Agents — Interactive Prototype (Demo Data)')

st.sidebar.header('Select Agent')
agent = st.sidebar.selectbox('Agent', ['Attrition Prediction', 'Sentiment Monitor', 'Time Analytics'])

# Dummy dataset
@st.cache_data
def load_dummy_employees(n=200):
    np.random.seed(42)
    df = pd.DataFrame({{
        'employee_id': range(1, n+1),
        'tenure_months': np.random.poisson(36, n),
        'performance_score': np.random.choice([1,2,3,4,5], n),
        'engagement_score': np.random.normal(3.5, 0.7, n).clip(1,5),
        'weekly_hours': np.random.normal(40,5,n).clip(20,80)
    }})
    # dummy attrition risk
    df['attrition_risk'] = (0.3*(df['tenure_months']<12) + 0.2*(df['performance_score']<3) + 0.1*(df['engagement_score']<3)).round(2)
    return df

df = load_dummy_employees(250)

if agent == 'Attrition Prediction':
    st.header('Attrition Prediction (Demo)')
    st.write('This simulates risk scoring using demo data.')
    top = st.slider('Show top N highest-risk employees', 5, 50, 10)
    st.dataframe(df.sort_values('attrition_risk', ascending=False).head(top))
    st.bar_chart(df['attrition_risk'].value_counts().sort_index())

elif agent == 'Sentiment Monitor':
    st.header('Sentiment & Engagement Monitor (Demo)')
    st.write('Demo engagement distribution and sample topics.')
    st.metric('Average engagement score', round(df['engagement_score'].mean(),2))
    st.line_chart(df['engagement_score'].rolling(20).mean())

elif agent == 'Time Analytics':
    st.header('Time & Workforce Analytics (Demo)')
    st.write('Show overtime and weekly hours distribution.')
    st.metric('Avg weekly hours', round(df['weekly_hours'].mean(),2))
    st.hist_chart(df['weekly_hours'])

st.markdown('---')
st.info('This is a demo skeleton. Replace demo data with BigQuery connectors and Vertex AI endpoints for a live POC.')
