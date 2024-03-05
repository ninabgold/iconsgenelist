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

if rusp_conditions:
    df_filtered = df[any(rusp_conditions)]
else:
    df_filtered = df.copy()

# Slider for number of screening programs
num_programs = st.sidebar.slider('Number of screening programs that include gene', 1, 25, 1)

# Filter data based on number of programs (applying it on the already RUSP-filtered data)
df_filtered = df_filtered[df_filtered['scr_sum'] >= num_programs]

# Multiselector for screening programs
screening_programs = [col[4:].capitalize() for col in df.columns if col.startswith('scr_') and col not in ['scr_sum', 'rusp']]
selected_programs = st.sidebar.multiselect('Screening Programs', screening_programs)

# Filter data based on selected screening programs
if selected_programs:
    df_filtered = df_filtered[df_filtered[[f'scr_{program.lower()}' for program in selected_programs]].any(axis=1)]

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

if inheritance_conditions:
    df_filtered = df_filtered[any(inheritance_conditions)]

# Main section
st.write(f"Genes matching selected criteria:")
st.write(df_filtered['gene_official'].tolist())
