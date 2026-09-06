import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils import load_data, dimensions

df, occ_scores = load_data()

st.title("Job Automation Analysis")

st.sidebar.header("Filter & Select")
category_filter = st.sidebar.selectbox("Filter by Risk Category:", ["All", "High", "Medium", "Low"])

ranges = {
    "All": "0% - 100%",
    "High": "70% - 100%",
    "Medium": "40% - 69.9%",
    "Low": "0% - 39.9%"
}
st.sidebar.info(f"**Selected Category Range:** {ranges[category_filter]}")

if category_filter == "All":
    filtered_jobs = occ_scores['job_title'].tolist()
else:
    filtered_jobs = occ_scores[occ_scores['risk_category'] == category_filter]['job_title'].tolist()
    
if not filtered_jobs:
    st.warning(f"No jobs found in the {category_filter} risk category.")
else:
    selected_job = st.sidebar.selectbox("Select an occupation:", filtered_jobs)
    
    if st.session_state.current_job != selected_job:
        st.session_state.task_index = 0
        st.session_state.current_job = selected_job
    
    job_df = df[df['job_title'] == selected_job]
    overall_score = job_df['occ_automation_score'].iloc[0]
    risk_category = job_df['risk_category'].iloc[0]
    num_tasks = len(job_df)
    
    st.header(f"Occupation: {selected_job}")
    st.write(f"**Tasks Analyzed:** {num_tasks}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Automation Likelihood", f"{overall_score:.2f}%")
    with col2:
        st.metric("Automation Risk Category", risk_category)
        
    st.write("---")
    st.write("**Framework Dimension Analysis**")
    
    avg_dims = [job_df[f"dimension_assessments.{dim}.score"].mean() for dim in dimensions]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=avg_dims,
        theta=[d.replace('_', ' ').title() for d in dimensions],
        fill='toself',
        name=selected_job
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.write("---")
    st.write("**Task Distribution Analysis**")
    
    task_bins = [0, 40, 70, 100.1]
    task_labels = ['Low Risk', 'Medium Risk', 'High Risk']
    job_df['task_risk_category'] = pd.cut(job_df['task_automation_score'], bins=task_bins, labels=task_labels, right=False)
    task_dist = job_df['task_risk_category'].value_counts().reset_index()
    task_dist.columns = ['Risk Category', 'Count']
    
    fig_pie = px.pie(task_dist, names='Risk Category', values='Count', color='Risk Category',
                     color_discrete_map={'Low Risk':'green', 'Medium Risk':'goldenrod', 'High Risk':'red'},
                     hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.write("---")
    st.write("**Task-Level Automation Analysis**")
    
    task_sorted = job_df.sort_values(by='task_automation_score', ascending=False)
    most_auto = task_sorted.iloc[0]
    least_auto = task_sorted.iloc[-1]
    
    col_most, col_least = st.columns(2)
    with col_most:
        with st.container(border=True):
            st.caption("🔴 MOST AUTOMATABLE TASK")
            st.markdown(f"**{most_auto['task_description']}**")
            st.metric("Automation Score", f"{most_auto['task_automation_score']}%")
            
    with col_least:
        with st.container(border=True):
            st.caption("🟢 LEAST AUTOMATABLE TASK")
            st.markdown(f"**{least_auto['task_description']}**")
            st.metric("Automation Score", f"{least_auto['task_automation_score']}%")
            
    st.write("**All Task Breakdown**")
    total_tasks = len(task_sorted)
    
    def update_task_from_slider():
        st.session_state.task_index = st.session_state.slider_nav - 1

    st.slider(
        "Task Navigation Bar", 
        min_value=1, 
        max_value=total_tasks, 
        value=st.session_state.task_index + 1,
        key="slider_nav",
        on_change=update_task_from_slider
    )
    
    current_task = task_sorted.iloc[st.session_state.task_index]
    
    with st.container(border=True):
        st.caption(f"Task {st.session_state.task_index + 1} of {total_tasks}")
        
        col_desc, col_score = st.columns([3, 1])
        with col_desc:
            st.markdown("**Task Description**")
            st.write(current_task['task_description'])
        with col_score:
            score = current_task['task_automation_score']
            st.metric("Likelihood", f"{score}%")