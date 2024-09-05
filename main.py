import streamlit as st
import pandas as pd

# Define the projects and their scores for each variable
projects = {
    'Project A': {'variable1': 70, 'variable2': 80, 'variable3': 60, 'variable4': 90, 'variable5': 50},
    'Project B': {'variable1': 60, 'variable2': 70, 'variable3': 80, 'variable4': 60, 'variable5': 70},
    'Project C': {'variable1': 90, 'variable2': 85, 'variable3': 70, 'variable4': 80, 'variable5': 90},
    'Project D': {'variable1': 75, 'variable2': 65, 'variable3': 75, 'variable4': 85, 'variable5': 80},
    'Project E': {'variable1': 80, 'variable2': 75, 'variable3': 90, 'variable4': 70, 'variable5': 60},
    'Project F': {'variable1': 85, 'variable2': 95, 'variable3': 85, 'variable4': 95, 'variable5': 85},
    'Project G': {'variable1': 65, 'variable2': 60, 'variable3': 65, 'variable4': 75, 'variable5': 70},
    'Project H': {'variable1': 70, 'variable2': 80, 'variable3': 85, 'variable4': 60, 'variable5': 75},
    'Project I': {'variable1': 95, 'variable2': 90, 'variable3': 95, 'variable4': 85, 'variable5': 90},
    'Project J': {'variable1': 55, 'variable2': 65, 'variable3': 60, 'variable4': 70, 'variable5': 75},
}

# Function to calculate project scores based on input variables and weights
def calculate_project_scores(projects, input_variables):
    scores = {}
    for project, variables in projects.items():
        score = sum(variables[var] * weight for var, weight in input_variables.items())
        scores[project] = score
    return scores

# Streamlit app
st.title("Project Score Calculator")

# Input sliders for weights
st.sidebar.header("Adjust Input Variables Weights")
input_variables = {
    'variable1': st.sidebar.slider('Weight for Variable 1', 0.0, 1.0, 0.2),
    'variable2': st.sidebar.slider('Weight for Variable 2', 0.0, 1.0, 0.3),
    'variable3': st.sidebar.slider('Weight for Variable 3', 0.0, 1.0, 0.1),
    'variable4': st.sidebar.slider('Weight for Variable 4', 0.0, 1.0, 0.25),
    'variable5': st.sidebar.slider('Weight for Variable 5', 0.0, 1.0, 0.15)
}

# Calculate scores for each project and convert to DF
project_scores = calculate_project_scores(projects, input_variables)
project_scores_df = pd.DataFrame.from_dict(project_scores, orient='index', columns=['Score'])

#Sort the DF
sorted_scores_df = project_scores_df.sort_values(by='Score', ascending = False)

#Define function to apply the style
def highlight_top5(s):
    colour = ['rgba(0,255,0,1.0)', 'rgba(0,255,0,0.9)', 'rgba(0,255,0,0.8)', 'rgba(0,255,0,0.7)','rgba(0,255,0,0.6)']
    return ['background-color: {}'.format(colour[i]) if i < 5 else '' for i in range(len(s))]

# Apply the stype to the Sorted DF
styled_scores_df = sorted_scores_df.style.apply(highlight_top5, subset=['Score'])

# Display scores
st.header("Project Scores")
st.dataframe(styled_scores_df)

# st.write(project_scores)

# Compare with previous weights
original_input_variables = {
    'variable1': 0.2,
    'variable2': 0.3,
    'variable3': 0.1,
    'variable4': 0.25,
    'variable5': 0.15
}

original_scores = calculate_project_scores(projects, original_input_variables)


#Create Comparison DF
comparison = {project: {'Original': original_scores[project], 'New': project_scores[project]} for project in projects}
comparison_df = pd.DataFrame.from_dict(comparison, orient='index')

# Add columns (Rank) to Comparison DF
comparison_df['Original Rank'] = comparison_df['Original'].rank(ascending=False).astype(int)
comparison_df['New Rank'] = comparison_df['New'].rank(ascending=False).astype(int)

# Display Comparison DF
st.header("Comparison with Original Weights")
st.dataframe(comparison_df)