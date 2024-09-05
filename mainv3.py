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

# Initialize session state for sliders 
if 'variable1' not in st.session_state:
    st.session_state['variable1'] = 0.2
if 'variable2' not in st.session_state:
    st.session_state['variable2'] = 0.2
if 'variable3' not in st.session_state:
    st.session_state['variable3'] = 0.2
if 'variable4' not in st.session_state:
    st.session_state['variable4'] = 0.15
if 'variable5' not in st.session_state:
    st.session_state['variable5'] = 0.15
if 'variable6' not in st.session_state:
    st.session_state['variable6'] = 0.10

# Input sliders for weights
st.sidebar.header("Adjust Input Variables Weights")
with st.sidebar.form(key='weights_form'):
    st.session_state['variable1'] = st.slider('Strategic Alignment', 0.0, 1.0, st.session_state['variable1'], step=0.1)
    st.session_state['variable2'] = st.slider('Client Focus and Business Need', 0.0, 1.0, st.session_state['variable2'], step=0.1)
    st.session_state['variable3'] = st.slider('Risk', 0.0, 1.0, st.session_state['variable3'], step=0.1)
    st.session_state['variable4'] = st.slider('Scalability', 0.0, 1.0, st.session_state['variable4'], step=0.1)
    st.session_state['variable5'] = st.slider('Interoperability', 0.0, 1.0, st.session_state['variable5'], step=0.1)
    st.session_state['variable6'] = st.slider('Project Readiness', 0.0, 1.0, st.session_state['variable6'], step=0.1)
           
    # Calculate the total weight
    total_weight = st.session_state['variable1'] + st.session_state['variable2'] + st.session_state['variable3'] + st.session_state['variable4'] + st.session_state['variable5'] + st.session_state['variable6']
    
    # Display the total weight
    st.sidebar.write(f"Total Weight: {total_weight:.2f}")

    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if total_weight != 0.0:
            st.sidebar.error("The total weight of all variables must not exceed 1.0. Please adjust the weights.")
        else:
            input_variables = {
            'variable1': st.session_state['variable1'],
            'variable2': st.session_state['variable2'],
            'variable3': st.session_state['variable3'],
            'variable4': st.session_state['variable4'],
            'variable5': st.session_state['variable5'],
            'variable6': st.session_state['variable6']
        }

            # Calculate scores for each project
            project_scores = calculate_project_scores(projects, input_variables)

            # Convert project scores to DataFrame
            project_scores_df = pd.DataFrame.from_dict(project_scores, orient='index', columns=['Score'])

            # Sort the scores to find the top 5
            sorted_scores_df = project_scores_df.sort_values(by='Score', ascending=False)

            # Define a function to apply the styles
            def highlight_top_5(s):
                color = ['rgba(0, 255, 0, 1.0)', 'rgba(0, 255, 0, 0.9)', 'rgba(0, 255, 0, 0.8)', 'rgba(0, 255, 0, 0.7)', 'rgba(0, 255, 0, 0.6)']
                return ['background-color: {}'.format(color[i]) if i < 5 else '' for i in range(len(s))]

            # Apply the styles to the DataFrame
            styled_scores_df = sorted_scores_df.style.apply(highlight_top_5, subset=['Score'])

            # Display scores
            st.header("Project Scores")
            st.dataframe(styled_scores_df)

            # Compare with previous weights
            original_input_variables = {
                'variable1': 0.2,
                'variable2': 0.3,
                'variable3': 0.1,
                'variable4': 0.25,
                'variable5': 0.15,
                'variable6': 0.10
            }

            original_scores = calculate_project_scores(projects, original_input_variables)

            # Create comparison DataFrame
            comparison = {project: {'Original': original_scores[project], 'New': project_scores[project]} for project in projects}
            comparison_df = pd.DataFrame.from_dict(comparison, orient='index')

            # Add rank columns
            comparison_df['Original Rank'] = comparison_df['Original'].rank(ascending=False).astype(int)
            comparison_df['New Rank'] = comparison_df['New'].rank(ascending=False).astype(int)

            # Display comparison DataFrame
            st.header("Comparison with Original Weights")
            st.dataframe(comparison_df)


# Form submission button
# with st.sidebar.form(key='weights_form'):
    

