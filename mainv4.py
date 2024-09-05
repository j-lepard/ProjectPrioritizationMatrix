import streamlit as st
import pandas as pd

# Define the projects and their scores for each variable
projects = {
    'Project A': {'variable1': 70, 'variable2': 80, 'variable3': 60, 'variable4': 90, 'variable5': 50, 'variable6': 40},
    'Project B': {'variable1': 60, 'variable2': 70, 'variable3': 80, 'variable4': 60, 'variable5': 70, 'variable6': 50},
    'Project C': {'variable1': 90, 'variable2': 85, 'variable3': 70, 'variable4': 80, 'variable5': 90, 'variable6': 60},
    'Project D': {'variable1': 75, 'variable2': 65, 'variable3': 75, 'variable4': 85, 'variable5': 80, 'variable6': 70},
    'Project E': {'variable1': 80, 'variable2': 75, 'variable3': 90, 'variable4': 70, 'variable5': 60, 'variable6': 80},
    'Project F': {'variable1': 85, 'variable2': 95, 'variable3': 85, 'variable4': 95, 'variable5': 85, 'variable6': 90},
    'Project G': {'variable1': 65, 'variable2': 60, 'variable3': 65, 'variable4': 75, 'variable5': 70, 'variable6': 50},
    'Project H': {'variable1': 70, 'variable2': 80, 'variable3': 85, 'variable4': 60, 'variable5': 75, 'variable6': 40},
    'Project I': {'variable1': 95, 'variable2': 90, 'variable3': 95, 'variable4': 85, 'variable5': 90, 'variable6': 60},
    'Project J': {'variable1': 55, 'variable2': 65, 'variable3': 60, 'variable4': 70, 'variable5': 75, 'variable6': 50},
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
variable1 = st.sidebar.slider('Strategic Alignment', 0.0, 1.0, 0.2, step=0.05)
variable2 = st.sidebar.slider('Client Focus and Business Need', 0.0, 1.0, 0.2, step=0.05)
variable3 = st.sidebar.slider('Risk', 0.0, 1.0, 0.2, step=0.05)
variable4 = st.sidebar.slider('Scalability', 0.0, 1.0, 0.15, step=0.05)
variable5 = st.sidebar.slider('Interoperability', 0.0, 1.0, 0.15, step=0.05)
variable6 = st.sidebar.slider('Project Readiness', 0.0, 1.0, 0.10, step=0.05)

# Calculate the total weight
total_weight = variable1 + variable2 + variable3 + variable4 + variable5 + variable6
total_weight= round(total_weight,2)

# Display the total weight
st.sidebar.write(f"Total Weight: {total_weight:.2f}")

# # Form submission button
# with st.sidebar.form(key='weights_form'):
#     submit_button = st.form_submit_button(label='Submit')

# Ensure total weigh <1:
if total_weight != 1.0:
         st.sidebar.error(f"The total weight of all variables must equal 1.0. Its is currently {total_weight} Please adjust the weights.")
#     else:
input_variables = {
'variable1': variable1,
'variable2': variable2,
'variable3': variable3,
'variable4': variable4,
'variable5': variable5,
'variable6': variable6
}

# Calculate scores for each project and convert to DataFrame
project_scores = calculate_project_scores(projects, input_variables)
project_scores_df = pd.DataFrame.from_dict(project_scores, orient='index', columns=['Score'])

# Sort the DataFrame
sorted_scores_df = project_scores_df.sort_values(by='Score', ascending=False)

# Define a function to apply the styles
def highlight_top_5(s):
    color = ['rgba(49, 148, 36, 1.0)','rgba(60, 181,44, 1.0)','rgba(77, 205, 58, 1.0)','rgba(105, 215, 91, 1.0)','rgba(135, 223, 124, 1.0)']
    return ['background-color: {}'.format(color[i]) if i < 5 else '' for i in range(len(s))]

# Apply the styles to the DataFrame
styled_scores_df = (
        sorted_scores_df.style
        .apply(highlight_top_5, subset=['Score'])
        .set_table_styles(
            [{'selector': 'th.col0', 'props': [('min-width', '450px')]},
             {'selector': 'td.col0', 'props': [('min-width', '450px')]}]
        )
    )

# Display scores
st.header("Project Scores")
st.dataframe(styled_scores_df)

# Compare with previous weights
original_input_variables = {
'variable1': 0.2,
'variable2': 0.2,
'variable3': 0.1,
'variable4': 0.25,
'variable5': 0.15,
'variable6': 0.10
}

original_scores = calculate_project_scores(projects, original_input_variables)

def highlight_new_greater(val, original_val):
    color = 'green' if val < original_val else ''
    return f'background-color: {color}'

# Create comparison DataFrame

#Create Comparison DF
comparison = {project: {'Original': original_scores[project], 'New': project_scores[project]} for project in projects}


#Create Comparison DF
comparison = {project: {'Original': original_scores[project], 'New': project_scores[project]} for project in projects}
comparison_df = pd.DataFrame.from_dict(comparison, orient='index')

# Add columns (Rank) to Comparison DF
comparison_df['Original Rank'] = comparison_df['Original'].rank(ascending=False).astype(int)
comparison_df['New Rank'] = comparison_df['New'].rank(ascending=False).astype(int)

# Add a new column 'Change' that shows "Increase" if New > Original, otherwise "No Change" or "Decrease"
comparison_df[' Rank Change'] = comparison_df.apply(
    lambda row: 'Increase' if row['New Rank'] > row['Original Rank'] else ('--' if row['New Rank'] == row['Original Rank'] else 'Decrease'), 
    axis=1
)

# Apply the highlight function correctly
styled_comparison_df = comparison_df



# Display comparison DataFrame
st.header("Comparison with Original Weights")
st.dataframe(styled_comparison_df)