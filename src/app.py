import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# 1. Initialize Session State for Carousel
if 'task_index' not in st.session_state:
    st.session_state.task_index = 0
if 'current_job' not in st.session_state:
    st.session_state.current_job = None

# 2. Load Data and Precompute Categories
@st.cache_data
def load_data():
    with open('../data/processed/automation_assessments.json', 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    
    occ_scores = df.groupby('job_title')['occ_automation_score'].first().reset_index()
    
    def assign_category(score):
        if score >= 70: return "High"
        elif score >= 40: return "Medium"
        else: return "Low"
        
    occ_scores['risk_category'] = occ_scores['occ_automation_score'].apply(assign_category)
    df = df.merge(occ_scores[['job_title', 'risk_category']], on='job_title', how='left')
    return df, occ_scores

df, occ_scores = load_data()
dimensions = [
    'task_predictability', 'interaction_medium', 'social_requirement',
    'environmental_stability', 'consequence_of_failure',
    'regulatory_barrier', 'economic_arbitrage'
]

# 3. Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a view:", ["Landing Page", "Job Analysis Tool", "Insights Dashboard"])

# 4. Landing Page / Explainer View
if page == "Landing Page":
    st.title("AI Job Displacement Analysis Tool")
    
    st.markdown("""
    Welcome to the AI Job Displacement Analysis Tool. This platform evaluates the susceptibility of various occupations to artificial intelligence and robotic automation by breaking down jobs into their foundational tasks.
    """)
    
    st.write("**How it Works:**")
    st.write("Each occupation is assessed across seven framework dimensions (e.g., Task Predictability, Social Requirement, Consequence of Failure). These dimensions calculate a task-level automation score, which rolls up into the occupation's overall displacement likelihood.")
    
    st.info("**Dimension Scale:** 1 = Very difficult to automate (Human advantage) | 5 = Highly automatable (AI advantage)")
    
    st.write("**Risk Category Thresholds:**")
    st.markdown("""
    * **High Risk (70% - 100%):** The vast majority of core tasks are highly susceptible to automation. Roles in this category are likely to face significant displacement.
    * **Medium Risk (40% - 69.9%):** Occupations facing task augmentation. AI will likely change the daily workflow significantly, but human oversight remains necessary.
    * **Low Risk (0% - 39.9%):** Occupations heavily reliant on complex human interaction, unpredictable physical environments, or high-stakes accountability.
    """)

# 5. Job Analysis Tool View
elif page == "Job Analysis Tool":
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
        
        # Categorize tasks into risk buckets
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

# 6. Insights Dashboard View
elif page == "Insights Dashboard":
    st.title("Insights & Trends")
    
    st.write("**Summary Statistics**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Occupations Analyzed", len(occ_scores))
    with col2:
        st.metric("Average Automation Risk", f"{occ_scores['occ_automation_score'].mean():.2f}%")
    with col3:
        st.metric("Total Tasks Evaluated", len(df))

    st.write("---")
    st.write("**Occupation Comparison**")
    
    bar_data = occ_scores.sort_values(by='occ_automation_score', ascending=False)
    fig_bar = px.bar(
        bar_data, 
        x='job_title', 
        y='occ_automation_score', 
        color='risk_category',
        color_discrete_map={'Low': 'green', 'Medium': 'goldenrod', 'High': 'red'},
        labels={'job_title': 'Occupation', 'occ_automation_score': 'Automation Likelihood (%)'},
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.write("---")
    st.write("**Dimension Averages**")
    
    dim_cols = [f"dimension_assessments.{d}.score" for d in dimensions]
    overall_dim_avg = df[dim_cols].mean().reset_index()
    overall_dim_avg.columns = ['Dimension', 'Average Score']
    overall_dim_avg['Dimension'] = [d.replace('_', ' ').title() for d in dimensions]
    
    fig_dim_avg = px.bar(
        overall_dim_avg, 
        x='Dimension', 
        y='Average Score',
        color='Average Score',
        color_continuous_scale='RdYlGn_r',
        labels={'Dimension': 'Dimension', 'Average Score': 'Average Score (1-5)'}
    )
    fig_dim_avg.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_dim_avg, use_container_width=True)
        
    st.write("---")
    st.write("**Dimension Heatmap**")
    
    heatmap_data = df.groupby('job_title')[dim_cols].mean()
    heatmap_data.columns = [d.replace('_', ' ').title() for d in dimensions]
    
    fig_heat = px.imshow(
        heatmap_data, 
        text_auto=".1f", 
        aspect="auto",
        color_continuous_scale='RdYlGn_r',
        labels=dict(x="Dimension", y="Occupation", color="Avg Score (1-5)")
    )
    fig_heat.update_yaxes(dtick=1)
    fig_heat.update_layout(height=max(600, len(heatmap_data) * 35))
    st.plotly_chart(fig_heat, use_container_width=True)