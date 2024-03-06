import streamlit as st
import pandas as pd
import plotly.express as px

# Use st.cache_data to cache the data loading function
@st.cache_data
def load_data():
    return pd.read_csv('genelist_all_version5March.csv')

df = load_data()

# Page Setup
st.title('Newborn screening gene selector')
st.sidebar.header('Filters')

# Capture user selections for filtering
# RUSP Status
rusp_status_options = df['rusp'].unique().tolist()
rusp_status_selection = st.sidebar.multiselect('RUSP Status', rusp_status_options, key='rusp')

# Inheritance Pattern
inheritance_options = df['inheritance_babyseq2'].unique().tolist()
inheritance_selection = st.sidebar.multiselect('Inheritance Pattern', inheritance_options, key='inheritance_babyseq2')

# Orthogonal Test
orthogonal_test_options = df['orthogonal_test'].unique().tolist()
orthogonal_test_selection = st.sidebar.multiselect('Orthogonal Test', orthogonal_test_options, key='orthogonal_test')

# Age of Onset
age_onset_options = df['age_onset_asqm_standard'].unique().tolist()
age_onset_selection = st.sidebar.multiselect('Age of Onset', age_onset_options, key='age_onset')

# Severity of Disease
severity_options = df['severity'].unique().tolist()
severity_selection = st.sidebar.multiselect('Severity of Disease', severity_options, key='severity')

# Efficacy of Treatment
efficacy_options = df['efficacy'].unique().tolist()
efficacy_selection = st.sidebar.multiselect('Efficacy of Treatment', efficacy_options, key='efficacy')

# Apply filters to the dataframe
filtered_df = df.copy()

if rusp_status_selection:
    filtered_df = filtered_df[filtered_df['rusp'].isin(rusp_status_selection)]

if inheritance_selection:
    filtered_df = filtered_df[filtered_df['inheritance_babyseq2'].isin(inheritance_selection)]

if orthogonal_test_selection:
    filtered_df = filtered_df[filtered_df['orthogonal_test'].isin(orthogonal_test_selection)]

if age_onset_selection:
    filtered_df = filtered_df[filtered_df['age_onset_asqm_standard'].isin(age_onset_selection)]

if severity_selection:
    filtered_df = filtered_df[filtered_df['severity'].isin(severity_selection)]

if efficacy_selection:
    filtered_df = filtered_df[filtered_df['efficacy'].isin(efficacy_selection)]

# Function to generate and display bar graphs for filtered data
def display_bar_graphs(df, column, title):
    fig = px.bar(df[column].value_counts().reset_index(), x='index', y=column,
                 title=title, labels={'index': column, column: 'Count'})
    fig.update_layout(xaxis_title=column, yaxis_title='Count', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)

# Display bar graphs for each category based on user selections
display_bar_graphs(filtered_df, 'rusp', 'Distribution of Genes by RUSP Status')
display_bar_graphs(filtered_df, 'inheritance_babyseq2', 'Distribution of Genes by Inheritance Pattern')
display_bar_graphs(filtered_df, 'orthogonal_test', 'Distribution of Genes by Orthogonal Test')
display_bar_graphs(filtered_df, 'age_onset_asqm_standard', 'Distribution of Genes by Age of Onset')
display_bar_graphs(filtered_df, 'severity', 'Distribution of Genes by Severity of Disease')
display_bar_graphs(filtered_df, 'efficacy', 'Distribution of Genes by Efficacy of Treatment')