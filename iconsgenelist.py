import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Use st.cache_data to cache the data loading function
@st.cache_data
def load_data():
    return pd.read_csv('genelist_all_version15Feb.csv')

df = load_data()

# Set page title
st.title('Newborn Screening Gene Selector')

# Sidebar
st.sidebar.header('Filters')

# Title for RUSP status checkboxes
st.sidebar.header('US RUSP Status')

# Checkboxes for RUSP status with unique keys
rusp_core = st.sidebar.checkbox('Core', value=False, key='rusp_core_key')
rusp_secondary = st.sidebar.checkbox('Secondary', value=False, key='rusp_secondary_key')
rusp_not_on_rusp = st.sidebar.checkbox('Not on RUSP', value=False, key='rusp_not_on_rusp_key')

# Apply RUSP status filter using DataFrame.query method to avoid ambiguity
query_string = []
if rusp_core:
    query_string.append("rusp == 'Core'")
if rusp_secondary:
    query_string.append("rusp == 'Secondary'")
if rusp_not_on_rusp:
    query_string.append("rusp.isna()", engine='python')

df_filtered = df.query(" or ".join(query_string)) if query_string else df.copy()

# Slider for number of screening programs
num_programs = st.sidebar.slider('Number of screening programs that include gene', 1, 25, 1, key='num_programs_key')

# Further filter data based on number of programs
df_filtered = df_filtered[df_filtered['scr_sum'] >= num_programs]

# Multiselector for screening programs
st.sidebar.header('Screening Programs')
screening_programs = [col[4:].capitalize() for col in df.columns if col.startswith('scr_') and col not in ['scr_sum', 'rusp']]
selected_programs = st.sidebar.multiselect('Select Programs', screening_programs, key='selected_programs_key')

# Applying filter based on selected screening programs
if selected_programs:
    program_filter = " or ".join([f"`scr_{program.lower()}` == 1" for program in selected_programs])
    df_filtered = df_filtered.query(program_filter)

# Title for Inheritance checkboxes
st.sidebar.header('Inheritance')

# Checkboxes for Inheritance with unique keys
inheritance_ar = st.sidebar.checkbox('AR', value=False, key='inheritance_ar_key')
inheritance_ad = st.sidebar.checkbox('AD', value=False, key='inheritance_ad_key')
inheritance_xl = st.sidebar.checkbox('XL', value=False, key='inheritance_xl_key')
inheritance_missing = st.sidebar.checkbox('Missing', value=False, key='inheritance_missing_key')

# Apply Inheritance filter
inheritance_conditions = []
if inheritance_ar:
    inheritance_conditions.append("inheritance == 'AR'")
if inheritance_ad:
    inheritance_conditions.append("inheritance == 'AD'")
if inheritance_xl:
    inheritance_conditions.append("inheritance == 'XLR'")
if inheritance_missing:
    inheritance_conditions.append("inheritance.isna()")

df_filtered = df_filtered.query(" or ".join(inheritance_conditions)) if inheritance_conditions else df_filtered

# Title for Penetrance checkboxes
st.sidebar.header('Penetrance')

# Checkboxes for Penetrance with unique keys
penetrance_high = st.sidebar.checkbox('High', value=False, key='penetrance_high_key')
penetrance_moderate = st.sidebar.checkbox('Moderate', value=False, key='penetrance_moderate_key')
penetrance_missing = st.sidebar.checkbox('Missing', value=False, key='penetrance_missing_key')

# Apply Penetrance filter
penetrance_conditions = []
if penetrance_high:
    penetrance_conditions.append("penetrance == 'HIGH (A)'")
if penetrance_moderate:
    penetrance_conditions.append("penetrance == 'MODERATE(A)'")
if penetrance_missing:
    penetrance_conditions.append("penetrance.isna()")

df_filtered = df_filtered.query(" or ".join(penetrance_conditions)) if penetrance_conditions else df_filtered

# Title for Orthogonal test checkboxes
st.sidebar.header('Orthogonal Test')

# Checkboxes for Orthogonal test with unique keys
orthogonal_yes = st.sidebar.checkbox('Yes', value=False, key='orthogonal_yes_key')
orthogonal_no = st.sidebar.checkbox('No', value=False, key='orthogonal_no_key')
orthogonal_missing = st.sidebar.checkbox('Missing', value=False, key='orthogonal_missing_key')

# Apply Orthogonal test filter
orthogonal_conditions = []
if orthogonal_yes:
    orthogonal_conditions.append("orthogonal_test == 'Y'")
if orthogonal_no:
    orthogonal_conditions.append("orthogonal_test == 'N'")
if orthogonal_missing:
    orthogonal_conditions.append("orthogonal_test.isna()")

df_filtered = df_filtered.query(" or ".join(orthogonal_conditions)) if orthogonal_conditions else df_filtered

# Title for Age of Onset (ASQM) checkboxes
st.sidebar.header('Age of Onset (ASQM)')

# Checkboxes for Age of Onset (ASQM) with unique keys
age_onset_birth = st.sidebar.checkbox('Birth', value=False, key='age_onset_birth_key')
age_onset_neonatal = st.sidebar.checkbox('Neonatal', value=False, key='age_onset_neonatal_key')
age_onset_infant = st.sidebar.checkbox('Infant', value=False, key='age_onset_infant_key')
age_onset_childhood = st.sidebar.checkbox('Childhood', value=False, key='age_onset_childhood_key')
age_onset_adolescent_adult = st.sidebar.checkbox('Adolescent/Adult', value=False, key='age_onset_adolescent_adult_key')
age_onset_variable = st.sidebar.checkbox('Variable', value=False, key='age_onset_variable_key')
age_onset_missing = st.sidebar.checkbox('Missing', value=False, key='age_onset_missing_key')

# Apply Age of Onset (ASQM) filter
age_onset_conditions = []
if age_onset_birth:
    age_onset_conditions.append("age_onset_asqm_standard == 'Birth'")
if age_onset_neonatal:
    age_onset_conditions.append("age_onset_asqm_standard == 'Neonatal'")
if age_onset_infant:
    age_onset_conditions.append("age_onset_asqm_standard == 'Infant'")
if age_onset_childhood:
    age_onset_conditions.append("age_onset_asqm_standard == 'Childhood'")
if age_onset_adolescent_adult:
    age_onset_conditions.append("age_onset_asqm_standard == 'Adolescent/Adult'")
if age_onset_variable:
    age_onset_conditions.append("age_onset_asqm_standard == 'Variable'")
if age_onset_missing:
    age_onset_conditions.append("age_onset_asqm_standard.isna()")

df_filtered = df_filtered.query(" or ".join(age_onset_conditions)) if age_onset_conditions else df_filtered

# Title for Severity of disease checkboxes
st.sidebar.header('Severity of Disease')

# Checkboxes for Severity with unique keys
severity_severe = st.sidebar.checkbox('Severe', value=False, key='severity_severe_key')
severity_moderate = st.sidebar.checkbox('Moderate', value=False, key='severity_moderate_key')
severity_mild = st.sidebar.checkbox('Mild', value=False, key='severity_mild_key')
severity_no_symptoms = st.sidebar.checkbox('No symptoms', value=False, key='severity_no_symptoms_key')
severity_missing = st.sidebar.checkbox('Missing', value=False, key='severity_missing_key')

# Apply Severity filter
severity_conditions = []
if severity_severe:
    severity_conditions.append("severity == 3")
if severity_moderate:
    severity_conditions.append("severity == 2")
if severity_mild:
    severity_conditions.append("severity == 1")
if severity_no_symptoms:
    severity_conditions.append("severity == 0")
if severity_missing:
    severity_conditions.append("severity.isna()")

df_filtered = df_filtered.query(" or ".join(severity_conditions)) if severity_conditions else df_filtered

# Title for Efficacy of Treatment checkboxes
st.sidebar.header('Efficacy of Treatment')

# Checkboxes for Efficacy of Treatment with unique keys
efficacy_high = st.sidebar.checkbox('High efficacy', value=False, key='efficacy_high_key')
efficacy_moderate = st.sidebar.checkbox('Moderate efficacy', value=False, key='efficacy_moderate_key')
efficacy_minimal = st.sidebar.checkbox('Minimal efficacy', value=False, key='efficacy_minimal_key')
efficacy_no_treatment = st.sidebar.checkbox('No treatment', value=False, key='efficacy_no_treatment_key')
efficacy_missing = st.sidebar.checkbox('Missing', value=False, key='efficacy_missing_key')

# Apply Efficacy of Treatment filter
efficacy_conditions = []
if efficacy_high:
    efficacy_conditions.append("efficacy == 3")
if efficacy_moderate:
    efficacy_conditions.append("efficacy == 2")
if efficacy_minimal:
    efficacy_conditions.append("efficacy == 1")
if efficacy_no_treatment:
    efficacy_conditions.append("efficacy == 0")
if efficacy_missing:
    efficacy_conditions.append("efficacy.isna()")

df_filtered = df_filtered.query(" or ".join(efficacy_conditions)) if efficacy_conditions else df_filtered

# Display the filtered results
genes_list = df_filtered['gene_official'].tolist()
genes_html = "<div style='font-family: Arial; font-size: 11px; color: black;'>"
for gene in genes_list:
    genes_html += f"{gene}<br>"
genes_html += "</div>"

st.markdown(genes_html, unsafe_allow_html=True)

# Assuming df_filtered is your DataFrame filtered according to the user's selections.

categories = [
    'rusp',                # RUSP status
    'inheritance',         # Inheritance pattern
    'orthogonal_test',     # Orthogonal test
    'age_onset_asqm_standard', # Age of onset
    'severity',            # Severity of disease
    'efficacy'             # Efficacy of treatment
]

# Function to generate and display bar graphs for each category
def generate_and_display_bar_graphs(df, categories):
    for category in categories:
        # Prepare data for plotting
        gene_counts = df[category].value_counts().reset_index()
        gene_counts.columns = [category, 'Number of Genes']
        
        # For tooltips, we aggregate genes into lists grouped by the category
        tooltips = df.groupby(category)['gene_official'].apply(list).reset_index(name='Genes')
        plot_data = pd.merge(gene_counts, tooltips, on=category, how='left')
        
        # Plot
        fig = px.bar(plot_data, x=category, y='Number of Genes',
                     hover_data=['Genes'],
                     labels={'Genes': 'Included Genes'},
                     title=f'Number of Genes by {category.replace("_", " ").title()}')
        fig.update_traces(marker_color='navy', hovertemplate="<br>".join([
            "Category: %{x}",
            "Number of Genes: %{y}",
            "Genes: %{customdata[0]}"]))
        fig.update_layout(xaxis_title=category.replace("_", " ").title(), yaxis_title="Number of Genes")
        
        # Display the figure
        st.plotly_chart(fig, use_container_width=True)

# Assuming df_filtered is already defined and filtered based on the user's selections
generate_and_display_bar_graphs(df_filtered, categories)