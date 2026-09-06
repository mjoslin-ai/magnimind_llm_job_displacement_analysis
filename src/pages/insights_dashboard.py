import streamlit as st
import plotly.express as px
from utils import load_data, dimensions

df, occ_scores = load_data()

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

bar_data = occ_scores.sort_values(by='occ_automation_score', ascending=True)
fig_bar = px.bar(
    bar_data, 
    x='occ_automation_score', 
    y='job_title', 
    color='risk_category',
    color_discrete_map={'Low': 'green', 'Medium': 'goldenrod', 'High': 'red'},
    labels={'job_title': 'Occupation', 'occ_automation_score': 'Automation Likelihood (%)'},
    orientation='h'
)
fig_bar.update_layout(height=max(500, len(bar_data) * 30))
st.plotly_chart(fig_bar, use_container_width=True)

st.write("---")
st.write("**Dimension Averages**")

dim_cols = [f"dimension_assessments.{d}.score" for d in dimensions]
overall_dim_avg = df[dim_cols].mean().reset_index()
overall_dim_avg.columns = ['Dimension', 'Average Score']
overall_dim_avg['Dimension'] = [d.replace('_', ' ').title() for d in dimensions]
overall_dim_avg = overall_dim_avg.sort_values(by='Average Score', ascending=True)

fig_dim_avg = px.bar(
    overall_dim_avg, 
    x='Average Score', 
    y='Dimension',
    color='Average Score',
    color_continuous_scale='RdYlGn_r',
    labels={'Dimension': 'Dimension', 'Average Score': 'Average Score (1-5)'},
    orientation='h'
)
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