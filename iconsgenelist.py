import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Use st.cache_data to cache the data loading function
@st.cache_data
def load_data():
    return pd.read_csv('genelist_all_version5March.csv')



df = load_data()

st.title('Newborn screening gene selector')

# Define checkboxes in the sidebar before using them
st.sidebar.header('US RUSP status')
rusp_core = st.sidebar.checkbox('Core', value=False, key='rusp_core_key')
rusp_secondary = st.sidebar.checkbox('Secondary', value=False, key='rusp_secondary_key')
rusp_not_on_rusp = st.sidebar.checkbox('Not on RUSP', value=False, key='rusp_not_on_rusp_key')

# Initialize df_filtered with the full DataFrame as default
df_filtered = df.copy()

# Now that checkboxes are defined, you can use them in your logic
query_conditions = []
if rusp_core:
    query_conditions.append("rusp == 'Core'")
if rusp_secondary:
    query_conditions.append("rusp == 'Secondary'")
if rusp_not_on_rusp:
    # For rows where 'rusp' is NaN, pandas query method does not directly support isna(), use Python's filtering instead
    df_not_on_rusp = df[df['rusp'].isna()]

# Combine 'Core' and 'Secondary' conditions with "or" and filter df accordingly
if query_conditions:
    df_filtered = df.query(" or ".join(query_conditions))

# If 'Not on RUSP' was selected and we have additional conditions, we concatenate the dataframes
if rusp_not_on_rusp and query_conditions:
    df_filtered = pd.concat([df_filtered, df_not_on_rusp]).drop_duplicates()
elif rusp_not_on_rusp:
    df_filtered = df_not_on_rusp

# Slider for number of screening programs
num_programs = st.sidebar.slider('Number of screening programs that include gene', 1, 26, 1, key='num_programs_key')

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
inheritance_xlr = st.sidebar.checkbox('XLR', value=False, key='inheritance_xlr_key')
inheritance_xld = st.sidebar.checkbox('XLD', value=False, key='inheritance_xld_key')
inheritance_missing = st.sidebar.checkbox('Missing', value=False, key='inheritance_missing_key')

# Apply Inheritance filter
inheritance_conditions = []
if inheritance_ar:
    inheritance_conditions.append("inheritance_babyseq2 == 'AR'")
if inheritance_ad:
    inheritance_conditions.append("inheritance_babyseq2 == 'AD'")
if inheritance_xlr:
    inheritance_conditions.append("inheritance_babyseq2 == 'XLR'")
if inheritance_xld:
    inheritance_conditions.append("inheritance_babyseq2 == 'XL'")
if inheritance_missing:
    inheritance_conditions.append("inheritance_babyseq2.isna()")

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
    penetrance_conditions.append("penetrance_babyseq2 == 'HIGH (A)'")
if penetrance_moderate:
    penetrance_conditions.append("penetrance_babyseq2 == 'MODERATE (A)'")
if penetrance_missing:
    penetrance_conditions.append("penetrance_babyseq2.isna()")

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
    orthogonal_conditions.append("orthogonal_test_goldetaldet == 'Y'")
if orthogonal_no:
    orthogonal_conditions.append("orthogonal_test_goldetaldet == 'N'")
if orthogonal_missing:
    orthogonal_conditions.append("orthogonal_test_goldetaldet == 'missing'")

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
st.sidebar.header('Severity of Disease (ASQM)')

# Checkboxes for Severity with unique keys
severity_severe = st.sidebar.checkbox('Severe', value=False, key='severity_severe_key')
severity_moderate = st.sidebar.checkbox('Moderate', value=False, key='severity_moderate_key')
severity_mild = st.sidebar.checkbox('Mild', value=False, key='severity_mild_key')
severity_missing = st.sidebar.checkbox('Missing', value=False, key='severity_missing_key')

# Apply Severity filter
severity_conditions = []
if severity_severe:
    severity_conditions.append("severity_asqm == 3")
if severity_moderate:
    severity_conditions.append("severity_asqm == 2")
if severity_mild:
    severity_conditions.append("severity_asqm == 1")
if severity_missing:
    severity_conditions.append("severity_asqm == 0")

df_filtered = df_filtered.query(" or ".join(severity_conditions)) if severity_conditions else df_filtered

# Title for Efficacy of Treatment checkboxes
st.sidebar.header('Efficacy of Treatment')

# Checkboxes for Efficacy of Treatment with unique keys
efficacy_high = st.sidebar.checkbox('High efficacy', value=False, key='efficacy_high_key')
efficacy_moderate = st.sidebar.checkbox('Moderate efficacy', value=False, key='efficacy_moderate_key')
efficacy_minimal = st.sidebar.checkbox('Minimal efficacy', value=False, key='efficacy_minimal_key')
efficacy_missing = st.sidebar.checkbox('No treatment', value=False, key='efficacy_missing_key')

# Apply Efficacy of Treatment filter
efficacy_conditions = []
if efficacy_high:
    efficacy_conditions.append("efficacy_asqm == 3")
if efficacy_moderate:
    efficacy_conditions.append("efficacy_asqm == 2")
if efficacy_minimal:
    efficacy_conditions.append("efficacy_asqm == 1")
if efficacy_missing:
    efficacy_conditions.append("efficacy_asqm == 0")

df_filtered = df_filtered.query(" or ".join(efficacy_conditions)) if efficacy_conditions else df_filtered

# Display the filtered results

filtered_genes_diseases = df_filtered[['gene', 'name_disease']]

# Rename columns for display
filtered_genes_diseases.columns = ['Gene', 'Disease']

# Reset index to start numbering at 1 for the table display
filtered_genes_diseases.index = range(1, len(filtered_genes_diseases) + 1)

# Display as a table in Streamlit, now with updated index and column names
st.write("Filtered genes and corresponding diseases", filtered_genes_diseases)

categories = [
    'rusp',                             # RUSP status
    'inheritance_babyseq2',             # Inheritance pattern
    'orthogonal_test_goldetaldet',      # Orthogonal test
    'age_onset_asqm_standard',          # Age of onset
    'severity_asqm',                    # Severity of disease
    'efficacy_asqm'                     # Efficacy of treatment
]

# Custom titles for the plots
custom_titles = {
    'rusp': 'US RUSP status',
    'inheritance_babyseq2': 'Inheritance',
    'orthogonal_test_goldetaldet': 'Orthogonal test',
    'age_onset_asqm_standard': 'Age of onset (ASQM)',
    'severity_asqm': 'Severity (ASQM)',
    'efficacy_asqm': 'Efficacy (ASQM)'
}

# Custom titles for the plots
custom_titles = {
    'rusp': 'US RUSP status',
    'inheritance_babyseq2': 'Inheritance',
    'orthogonal_test_goldetaldet': 'Orthogonal test',
    'age_onset_asqm_standard': 'Age of onset (ASQM)',
    'severity_asqm': 'Severity (ASQM)',
    'efficacy_asqm': 'Efficacy (ASQM)'
}

def preprocess_for_missing_data(df, columns):
    """
    Adjust specified columns in the DataFrame to include 'Missing' as a category
    for NaN (empty) cells.
    """
    for column in columns:
        df[column] = df[column].fillna('Missing')
    return df

def generate_individual_plots(df, category, title, show_yaxis_label):
    if category in ['rusp', 'inheritance_babyseq2', 'orthogonal_test_goldetaldet', 'age_onset_asqm_standard']:
        # Ensure 'Missing' is recognized for each category and treated accordingly
        df[category] = df[category].fillna('Missing')

        if category == 'rusp':
            df['rusp'] = df['rusp'].replace({'Missing': 'Not on RUSP'})
            order = ['Core', 'Secondary', 'Not on RUSP']
        elif category == 'inheritance_babyseq2':
            order = df[category].unique().tolist()
            if 'Missing' in order:
                order.append(order.pop(order.index('Missing')))
        elif category == 'orthogonal_test_goldetaldet':
            order = ['Y', 'N', 'Missing']
        elif category == 'age_onset_asqm_standard':
            # Adjust the order list based on your actual data categories for age_onset_asqm_standard
            order = df[category].unique().tolist()
            if 'Missing' in order:
                order.remove('Missing')
            order += ['Missing']  # Ensuring 'Missing' is the last category
            df[category] = df[category].replace({'missing': 'Missing', 'Childhood': 'Child', 'Adolescent/Adult': 'Adult', 'Missing': 'Missing'})
        
        df[category] = pd.Categorical(df[category], categories=order, ordered=True)
        gene_counts = df[category].value_counts().reindex(order).fillna(0)
        
        fig = px.bar(gene_counts, x=gene_counts.index, y=gene_counts.values,
                     title=title, labels={'y': 'Number of Genes'})
    else:
        gene_counts = df[category].value_counts().reset_index()
        gene_counts.columns = [category, 'Number of Genes']
        tooltips = df.groupby(category)['gene'].apply(list).reset_index(name='Genes')
        plot_data = pd.merge(gene_counts, tooltips, on=category, how='left')
        fig = px.bar(plot_data, x=category, y='Number of Genes',
                     hover_data=['Genes'],
                     labels={'index': category, 'Number of Genes': 'Number of Genes'},
                     title=title)
    
    fig.update_traces(marker_color='#D3D3D3', hovertemplate="<br>".join([
        "Category: %{x}",
        "Number of Genes: %{y}",
        "Genes: %{customdata[0]}"]))
    fig.update_layout(xaxis_title="", yaxis_title="Number of Genes" if show_yaxis_label else "")
    if category == 'age_onset_asqm_standard':
        fig.update_xaxes(tickangle=45)

    return fig

# Specify columns where you want to account for missing data
columns_to_account_for_missing = ['rusp', 'inheritance_babyseq2', 'severity_asqm', 'efficacy_asqm']

# Preprocess the DataFrame to include 'Missing' as a category for the specified columns
df_filtered = preprocess_for_missing_data(df_filtered, columns_to_account_for_missing)

# Generate and display plots
for i in range(0, len(categories), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        idx = i + j
        if idx < len(categories):
            category = categories[idx]
            title = custom_titles[category]
            show_yaxis_label = (j == 0)  # Only show the y-axis label for the leftmost graph
            fig = generate_individual_plots(df_filtered, category, title, show_yaxis_label)
            col.plotly_chart(fig, use_container_width=True)

# ... (previous code)

# Replace empty cells with 0 for the specified columns
columns_to_fill = [
    'scr_babydetectv2', 'scr_babyscreen', 'scr_babyseq2', 'scr_beginngs', 
    'scr_chenetal', 'scr_earlycheck', 'scr_firststeps', 'scr_generation', 
    'scr_gnstar', 'scr_guardian', 'scr_jianetal', 'scr_leeetal', 
    'scr_luoetal', 'scr_neoexome', 'scr_neoseq', 'scr_nests', 
    'scr_newbornsinsa', 'scr_puglia', 'scr_wangetal', 'scr_foresite', 
    'scr_fulgent', 'scr_igenomix', 'scr_mendelics', 'scr_nurture', 
    'scr_perkinelmer', 'scr_sema'
]

program_columns = [
    'scr_babydetectv2', 'scr_babyscreen', 'scr_babyseq2', 'scr_beginngs',
    'scr_chenetal', 'scr_earlycheck', 'scr_firststeps', 'scr_generation',
    'scr_gnstar', 'scr_guardian', 'scr_jianetal', 'scr_leeetal',
    'scr_luoetal', 'scr_neoexome', 'scr_neoseq', 'scr_nests',
    'scr_newbornsinsa', 'scr_puglia', 'scr_wangetal', 'scr_foresite',
    'scr_fulgent', 'scr_igenomix', 'scr_mendelics', 'scr_nurture',
    'scr_perkinelmer', 'scr_sema'
]

# Replace empty cells with 0 for the specified columns
df_filtered[program_columns] = df_filtered[program_columns].fillna(0)

# Filter the DataFrame to only include the genes that have been selected based on the sidebar selections
selected_genes = df_filtered['gene']

# Prepare data for the heatmap: genes along y-axis and program names along x-axis
heatmap_data = df_filtered.set_index('gene')[program_columns]
heatmap_values = heatmap_data.values

# Create the heatmap using Plotly
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_values,
    x=program_columns,
    y=selected_genes,
    colorscale='Blues',
    showscale=False
))

# Update the layout of the heatmap
fig_heatmap.update_layout(
    title='Gene Program Participation',
    xaxis_title="Programs",
    yaxis_title="Genes",
    xaxis={'tickangle': -45},
    yaxis={'autorange': 'reversed'}  # Optional to have the genes in reverse order
)

# Display the heatmap below the bar graphs
st.plotly_chart(fig_heatmap, use_container_width=True)

