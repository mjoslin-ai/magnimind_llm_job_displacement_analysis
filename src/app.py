import streamlit as st

if 'task_index' not in st.session_state:
    st.session_state.task_index = 0
if 'current_job' not in st.session_state:
    st.session_state.current_job = None

pg = st.navigation([
    st.Page("pages/landing_page.py", title="Landing Page"),
    st.Page("pages/job_analysis.py", title="Job Analysis"),
    st.Page("pages/insights_dashboard.py", title="Insights Dashboard")
])
pg.run()