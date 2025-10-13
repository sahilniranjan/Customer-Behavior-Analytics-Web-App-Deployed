"""
Streamlit dashboard for visualizing analytics.
"""
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

BASE_URL = 'http://localhost:5000'

st.title('Customer Behavior Dashboard')

# Fetch trends
if 'trends' not in st.session_state:
    res = requests.get(f'{BASE_URL}/api/analytics/trends')
    st.session_state['trends'] = res.json().get('trends', {})

trends = st.session_state['trends']

dates = list(trends.keys())
counts = list(trends.values())

df = pd.DataFrame({'date':dates,'count':counts})
fig = px.line(df, x='date', y='count', title='Daily Interactions')
st.plotly_chart(fig)

# Fetch patterns
if 'patterns' not in st.session_state:
    res = requests.get(f'{BASE_URL}/api/analytics/patterns')
    st.session_state['patterns'] = res.json().get('patterns', [])

patterns = st.session_state['patterns']
st.subheader('Detected Patterns')
for p in patterns:
    st.write(p)
