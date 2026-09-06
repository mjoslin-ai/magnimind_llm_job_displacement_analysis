import streamlit as st

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