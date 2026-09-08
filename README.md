# AI Job Displacement Analysis Tool

An interactive assessment tool that evaluates how likely different occupations and their component tasks are to be replaced or augmented by AI. The tool combines structured occupational data from O*NET with a custom multi-dimensional framework and LLM-based scoring to produce transparent, task-level automation risk estimates.

This project was developed as the final deliverable for the Magnimind Academy Mentorship Program.

---

## Overview

Rapid advances in large language models and related AI systems have intensified debate about which jobs will be automated and which will be augmented. Rather than treating entire occupations as monolithic, this tool decomposes jobs into their foundational tasks and scores each task across a set of carefully defined dimensions that capture automatability.

The resulting scores roll up into an overall **displacement likelihood (0–100%)** and a clear risk category, giving workers, educators, employers, and policymakers a data-driven starting point for discussion—not a definitive prediction.

---

## How It Works

1. **Occupation selection** – Users choose an occupation from a curated set of diverse roles spanning different industries, skill levels, and work contexts.
2. **Task extraction** – Core tasks for the selected occupation are drawn from the O*NET database.
3. **Multi-dimensional scoring** – Each task is evaluated across **seven framework dimensions** (examples include Task Predictability, Social Requirement, and Consequence of Failure). Scores range from 1 to 5:
   - **1** = Very difficult to automate (strong human advantage)
   - **5** = Highly automatable (strong AI advantage)
4. **Aggregation** – Task-level scores are combined into an overall occupation displacement likelihood (0–100%).
5. **Presentation** – Results are shown with dimension breakdowns, risk categorization, and explanatory context.

---

## Data Sources

- **O\*NET Database** (U.S. Department of Labor) – Comprehensive occupational data including task statements, skills, abilities, work activities, knowledge areas, work context, and tools & technology.
- **U.S. Bureau of Labor Statistics** – Foundational occupational employment and wage statistics used for context and selection of representative occupations.

---

## Risk Category Thresholds

| Category       | Score Range   | Interpretation                                                                 |
|----------------|---------------|--------------------------------------------------------------------------------|
| **High Risk**  | 70% – 100%    | Vast majority of core tasks are highly susceptible to automation. Significant displacement pressure is likely. |
| **Medium Risk**| 40% – 69.9%   | Substantial task augmentation expected. AI will change daily workflows, but human oversight remains essential. |
| **Low Risk**   | 0% – 39.9%    | Heavy reliance on complex human interaction, unpredictable physical environments, or high-stakes accountability. |

---

## Key Project Components

### 1. Automation Assessment Framework
A structured model with 5–8 (in this implementation, seven) dimensions that characterize automatability. Each dimension is defined, justified, weighted, and scored on a consistent 1–5 scale. An overall automation formula aggregates the dimension scores into a 0–100% displacement likelihood.

### 2. O\*NET Data Pipeline
Scripts that download, explore, clean, and structure relevant O\*NET files (Occupation Data, Task Statements, Skills, Abilities, Work Activities, Knowledge, Work Context, Tools and Technology). A diverse set of 20–50 occupations is selected to ensure coverage across industries, skill levels, and work types.

### 3. LLM-Powered Analysis
Prompt-engineered LLM calls that systematically score individual tasks against the framework dimensions. Structured (JSON) output is required for consistency. Temperature is kept low and prompts include clear criteria and examples. Results are validated for face validity and consistency.

### 4. Interactive Web Application
A Streamlit-based interface that lets non-technical users:
- Search or select an occupation
- View overall automation risk score and category
- Inspect dimension-level breakdowns (with visualizations such as radar/bar charts)
- Explore task-level automation likelihoods
- Receive high-level career resilience context

### 5. Visualizations & Insights
Occupation comparison charts, dimension heatmaps/radar plots, task-score distributions, and summary statistics that highlight patterns across the analyzed set of jobs.

---

## Design Decision Documentation

All major design choices are documented, including:

- Selection and weighting of framework dimensions
- Occupation sampling strategy and diversity criteria
- Prompt engineering iterations and consistency measures
- Scoring aggregation formula and risk thresholds
- Technology stack and UI prioritization

---

## Important Limitations & Uncertainty

- **Informed estimates, not predictions.** Scores reflect a specific analytical framework applied to current data and current AI capabilities.
- **Technology evolves rapidly.** What is difficult to automate today may become feasible tomorrow.
- **Expert disagreement exists.** Different researchers weight dimensions differently and reach different conclusions.
- **One perspective only.** This tool is intended to encourage critical thinking and the development of adaptable skills, not to dictate career decisions.

Users should treat the results as a structured starting point for further inquiry rather than absolute truth.

---

## Technical Stack

- **Language:** Python
- **Application framework:** Streamlit
- **Data handling:** Pandas
- **Visualization:** Plotly (and/or Matplotlib/Seaborn)
- **LLM APIs:** OpenAI GPT-4 (or equivalent – Anthropic Claude / Google Gemini)
- **Primary data source:** O\*NET database (Excel / text files or Web Services API)

---

## Getting Started

### Prerequisites
- Python 3.9+
- API key for the chosen LLM provider
- Downloaded O\*NET database files (or API credentials)

### Installation
```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt