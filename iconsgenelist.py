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

# Radio button for RUSP status
rusp_status = st.sidebar.radio(
    "RUSP status",
    ['Core', 'Secondary', 'Not on RUSP']
)

# Apply RUSP status filter
if rusp_status == 'Not on RUSP':
    df_filtered = df[df['rusp'].isna()]
else:
    df_filtered = df[df['rusp'] == rusp_status]

# Slider for number of screening programs
num_programs = st.sidebar.slider('Number of screening programs that include gene', 1, 25, 1)

# Filter data based on number of programs (applying it on the already RUSP-filtered data)
df_filtered = df_filtered[df_filtered['scr_sum'] >= num_programs]

# Multiselector for screening programs
screening_programs = [col[4:].capitalize() for col in df.columns if col.startswith('scr_') and col not in ['scr_sum', 'rusp']]
selected_programs = st.sidebar.multiselect('Screening Programs', screening_programs)

# Filter data based on selected screening programs
for program in selected_programs:
    program_col = 'scr_' + program.lower()
    df_filtered = df_filtered[df_filtered[program_col] == 1]

# Main section
st.write(f"Genes matching selected criteria:")
st.write(df_filtered['gene_official'].tolist())
