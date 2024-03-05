import streamlit as st
import pandas as pd

# Load the data
@st.cache
def load_data():
    return pd.read_csv('/mnt/data/genelist_all_version15Feb.csv')

df = load_data()

# Set page title
st.title('Newborn Screening Gene Selector')

# Sidebar
st.sidebar.header('Filters')

# Checkboxes for RUSP status
rusp_core = st.sidebar.checkbox('Core', value=False)
rusp_secondary = st.sidebar.checkbox('Secondary', value=False)
rusp_not_on_rusp = st.sidebar.checkbox('Not on RUSP', value=False)

# Apply RUSP status filter
rusp_conditions = []
if rusp_core:
    rusp_conditions.append(df['rusp'] == 'Core')
if rusp_secondary:
    rusp_conditions.append(df['rusp'] == 'Secondary')
if rusp_not_on_rusp:
    rusp_conditions.append(df['rusp'].isna())

# Apply the filters if any RUSP conditions are selected, otherwise use unfiltered data
df_filtered = df[any(rusp_conditions)] if rusp_conditions else df.copy()

# Slider for number of screening programs
num_programs = st.sidebar.slider('Number of screening programs that include gene', 1, 25, 1)

# Filter data based on number of programs (applying it on the already RUSP-filtered data)
df_filtered = df_filtered[df_filtered['scr_sum'] >= num_programs]

# Multiselector for screening programs
screening_programs = [col[4:].capitalize() for col in df.columns if col.startswith('scr_') and col not in ['scr_sum', 'rusp']]
selected_programs = st.sidebar.multiselect('Screening Programs', screening_programs)

# Filter data based on selected screening programs
if selected_programs:
    program_conditions = [df_filtered[f'scr_{program.lower()}'] == 1 for program in selected_programs]
    df_filtered = df_filtered[any(program_conditions)]

# Checkboxes for Inheritance
inheritance_ar = st.sidebar.checkbox('AR', value=False)
inheritance_ad = st.sidebar.checkbox('AD', value=False)
inheritance_xl = st.sidebar.checkbox('XL', value=False)
inheritance_missing = st.sidebar.checkbox('Missing', value=False)

# Apply Inheritance filter
inheritance_conditions = []
if inheritance_ar:
    inheritance_conditions.append(df_filtered['inheritance'] == 'AR')
if inheritance_ad:
    inheritance_conditions.append(df_filtered['inheritance'] == 'AD')
if inheritance_xl:
    inheritance_conditions.append(df_filtered['inheritance'] == 'XLR')
if inheritance_missing:
    inheritance_conditions.append(df_filtered['inheritance'].isna())

# Apply the filters if any inheritance conditions are selected, otherwise use unfiltered data
if inheritance_conditions:
    df_filtered = df_filtered[any(inheritance_conditions)]

# Checkboxes for Penetrance
penetrance_high = st.sidebar.checkbox('High', value=False)
penetrance_moderate = st.sidebar.checkbox('Moderate', value=False)
penetrance_missing = st.sidebar.checkbox('Missing', value=False)

# Apply Penetrance filter
penetrance_conditions = []
if penetrance_high:
    penetrance_conditions.append(df_filtered['penetrance'] == 'HIGH (A)')
if penetrance_moderate:
    penetrance_conditions.append(df_filtered['penetrance'] == 'MODERATE(A)')
if penetrance_missing:
    penetrance_conditions.append(df_filtered['penetrance'].isna())

# Apply the filters if any penetrance conditions are selected, otherwise use unfiltered data
if penetrance_conditions:
    df_filtered = df_filtered[any(penetrance_conditions)]

# Checkboxes for Age of Onset (ASQM)
age_onset_birth = st.sidebar.checkbox('Birth', value=False)
age_onset_neonatal = st.sidebar.checkbox('Neonatal', value=False)
age_onset_infant = st.sidebar.checkbox('Infant', value=False)
age_onset_childhood = st.sidebar.checkbox('Childhood', value=False)
age_onset_adolescent_adult = st.sidebar.checkbox('Adolescent/Adult', value=False)
age_onset_variable = st.sidebar.checkbox('Variable', value=False)
age_onset_missing = st.sidebar.checkbox('Missing', value=False)

# Apply Age of Onset (ASQM) filter
age_onset_conditions = []
if age_onset_birth:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'] == 'Birth')
if age_onset_neonatal:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'] == 'Neonatal')
if age_onset_infant:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'] == 'Infant')
if age_onset_childhood:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'] == 'Childhood')
if age_onset_adolescent_adult:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'] == 'Adolescent/Adult')
if age_onset_variable:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'] == 'Variable')
if age_onset_missing:
    age_onset_conditions.append(df_filtered['age_onset_asqm_standard'].isna())

# Apply the filters if any age of onset conditions are selected, otherwise use unfiltered data
if age_onset_conditions:
    df_filtered = df_filtered[any(age_onset_conditions)]

# Checkboxes for Severity
severity_severe = st.sidebar.checkbox('Severe', value=False)
severity_moderate = st.sidebar.checkbox('Moderate', value=False)
severity_mild = st.sidebar.checkbox('Mild', value=False)
severity_no_symptoms = st.sidebar.checkbox('No symptoms', value=False)
severity_missing = st.sidebar.checkbox('Missing', value=False)

# Apply Severity filter
severity_conditions = []
if severity_severe:
    severity_conditions.append(df_filtered['severity'] == 3)
if severity_moderate:
    severity_conditions.append(df_filtered['severity'] == 2)
if severity_mild:
    severity_conditions.append(df_filtered['severity'] == 1)
if severity_no_symptoms:
    severity_conditions.append(df_filtered['severity'] == 0)
if severity_missing:
    severity_conditions.append(df_filtered['severity'].isna())

if severity_conditions:
    df_filtered = df_filtered[any(severity_conditions)]

# Checkboxes for Efficacy of Treatment
efficacy_high = st.sidebar.checkbox('High efficacy', value=False)
efficacy_moderate = st.sidebar.checkbox('Moderate efficacy', value=False)
efficacy_minimal = st.sidebar.checkbox('Minimal efficacy', value=False)
efficacy_no_treatment = st.sidebar.checkbox('No treatment', value=False)
efficacy_missing = st.sidebar.checkbox('Missing', value=False)

# Apply Efficacy of Treatment filter
efficacy_conditions = []
if efficacy_high:
    efficacy_conditions.append(df_filtered['efficacy'] == 3)
if efficacy_moderate:
    efficacy_conditions.append(df_filtered['efficacy'] == 2)
if efficacy_minimal:
    efficacy_conditions.append(df_filtered['efficacy'] == 1)
if efficacy_no_treatment:
    efficacy_conditions.append(df_filtered['efficacy'] == 0)
if efficacy_missing:
    efficacy_conditions.append(df_filtered['efficacy'].isna())

if efficacy_conditions:
    df_filtered = df_filtered[any(efficacy_conditions)]

# Main section
st.write(f"Genes matching selected criteria:")
st.write(df_filtered['gene_official'].tolist())
