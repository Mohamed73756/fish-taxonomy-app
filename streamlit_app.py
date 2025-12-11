import streamlit as st
import pandas as pd

# --- CONFIGURATION & DATA LOADING ---
# Ensure your CSV file is in the same folder as this script
DATA_FILE = 'fish_data.csv'

# Load the data once and cache it for speed
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Fill down the higher taxonomic ranks if they are blank (common in hierarchical tables)
    df['Class'] = df['Class'].ffill() 
    df['Order'] = df['Order'].ffill()
    df['Family'] = df['Family'].ffill()
    return df

df_fish = load_data(DATA_FILE)

# --- APP LAYOUT ---
st.title("🐟 Interactive Fish Taxonomy Browser")
st.markdown("Explore the **{}** Class of fishes and their lower taxonomic ranks.".format(df_fish['Class'].iloc[0]))
# Use the official count you provided
st.markdown("**:blue[{}]** Total Fish Species Records Indexed".format(len(df_fish)))

# --- INTERACTIVE TAXONOMIC TREE ---

# 1. Select Order (Primary Filter)
st.sidebar.header("Filter by Order")
selected_order = st.sidebar.selectbox(
    "Choose a specific Order:", 
    df_fish['Order'].unique()
)

# Filter the DataFrame based on the selected Order
df_order = df_fish[df_fish['Order'] == selected_order]

st.subheader(f"Order: {selected_order}")

# 2. Iterate through Families within the selected Order
families = df_order['Family'].unique()

for family in families:
    # Use st.expander for a collapsible, interactive effect
    with st.expander(f"**Family: {family}** ({len(df_order[df_order['Family'] == family])} Species)"):
        df_family = df_order[df_order['Family'] == family].copy()
        
        # Clean up the fish name display for the species list
        # We assume the Genus and Species are in the same 'Fish' column after cleaning
        species_list = df_family['Species_Scientific'].tolist()
        
        # Display the list of species
        st.write("**:gray[Species List:]**")
        
        # Create a dictionary to group Species by their Genus (extracted from 'Fish' column)
        genus_groups = df_family.groupby(df_family['Species_Scientific'].str.split().str[0])
        
        for genus, group in genus_groups:
            st.markdown(f"**Genus: {genus}**")
            for index, row in group.iterrows():
                # Display only the species name, assuming the genus is already displayed
                species_only = row['Fish'].split(genus, 1)[-1].strip()
                st.markdown(f"- *{genus} {species_only}*")

# --- OPTIONAL: RAW DATA VIEW ---
if st.checkbox('Show Raw Data Table'):
    st.dataframe(df_fish)

# --- End of Streamlit App ---

