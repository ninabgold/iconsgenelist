import streamlit as st
import pandas as pd

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
num_programs = st.sidebar.slider('Number of screening programs that include gene', 1, 25, 1, key='num_programs_key')

# Filter data based on number of programs (applying it on the already RUSP-filtered data)
df_filtered = df_filtered[df_filtered['scr_sum'] >= num_programs]

# Multiselector for screening programs with unique key
screening_programs = [col[4:].capitalize() for col in df.columns if col.startswith('scr_') and col not in ['scr_sum', 'rusp']]
selected_programs = st.sidebar.multiselect('Screening Programs', screening_programs, key='selected_programs_key')

# Filter data based on selected screening programs
if selected_programs:
    program_conditions = [df_filtered[f'scr_{program.lower()}'] == 1 for program in selected_programs]
    df_filtered = df_filtered[any(program_conditions)]

# Checkboxes for Inheritance with unique keys
inheritance_ar = st.sidebar.checkbox('AR', value=False, key='inheritance_ar_key')
inheritance_ad = st.sidebar.checkbox('AD', value=False, key='inheritance_ad_key')
inheritance_xl = st.sidebar.checkbox('XL', value=False, key='inheritance_xl_key')
inheritance_missing = st.sidebar.checkbox('Missing', value=False, key='inheritance_missing_key')

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

if inheritance_conditions:
    df_filtered = df_filtered[any(inheritance_conditions)]

# Checkboxes for Penetrance with unique keys
penetrance_high = st.sidebar.checkbox('High', value=False, key='penetrance_high_key')
penetrance_moderate = st.sidebar.checkbox('Moderate', value=False, key='penetrance_moderate_key')
penetrance_missing = st.sidebar.checkbox('Missing', value=False, key='penetrance_missing_key')

# Apply Penetrance filter
penetrance_conditions = []
if penetrance_high:
    penetrance_conditions.append(df_filtered['penetrance'] == 'HIGH (A)')
if penetrance_moderate:
    penetrance_conditions.append(df_filtered['penetrance'] == 'MODERATE(A)')
if penetrance_missing:
    penetrance_conditions.append(df_filtered['penetrance'].isna())

if penetrance_conditions:
    df_filtered = df_filtered[any(penetrance_conditions)]

# Checkboxes for Orthogonal test with unique keys
orthogonal_yes = st.sidebar.checkbox('Yes', value=False, key='orthogonal_yes_key')
orthogonal_no = st.sidebar.checkbox('No', value=False, key='orthogonal_no_key')
orthogonal_missing = st.sidebar.checkbox('Missing', value=False, key='orthogonal_missing_key')

# Apply Orthogonal test filter
orthogonal_conditions = []
if orthogonal_yes:
    orthogonal_conditions.append(df_filtered['orthogonal_test'] == 'Y')
if orthogonal_no:
    orthogonal_conditions.append(df_filtered['orthogonal_test'] == 'N')
if orthogonal_missing:
    orthogonal_conditions.append(df_filtered['orthogonal_test'].isna())

if orthogonal_conditions:
    df_filtered = df_filtered[any(orthogonal_conditions)]

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

if age_onset_conditions:
    df_filtered = df_filtered[any(age_onset_conditions)]

# Skipping severity and efficacy for brevity, but ensure to add unique keys as shown above for these sections too

# Main section
st.write(f"Genes matching selected criteria:")
st.write(df_filtered['gene_official'].tolist())
