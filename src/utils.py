import pandas as pd
import json
import streamlit as st

@st.cache_data
def load_data():
    with open('../data/processed/automation_checkpoint.json', 'r') as f:
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

dimensions = [
    'task_predictability', 'interaction_medium', 'social_requirement',
    'environmental_stability', 'consequence_of_failure',
    'regulatory_barrier', 'economic_arbitrage'
]