import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="🎵 Track Explorer")
st.title("🎵 Track Explorer")

st.markdown("""
Use the interactive filters below to explore Spotify tracks by **year**, **danceability**, **energy**, and **tempo**.
""")

@st.cache_data
def load_data():
    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(current_file)
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    data_path = os.path.join(project_root, "data", "spotify_tracks_cleaned.csv")
    return pd.read_csv(data_path)

df = load_data()

# Main page filters (not sidebar)
with st.expander("🎚️ Filter Tracks", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        year_range = st.slider("Select Year Range", int(df["year"].min()), int(df["year"].max()), (2010, 2024))
        min_danceability = st.slider("Minimum Danceability", 0.0, 1.0, 0.5, step=0.05)

    with col2:
        min_energy = st.slider("Minimum Energy", 0.0, 1.0, 0.5, step=0.05)
        tempo_range = st.slider("Tempo Range (BPM)", int(df["tempo"].min()), int(df["tempo"].max()), (80, 180))

# Apply filters
filtered = df[
    (df["year"].between(*year_range)) &
    (df["danceability"] >= min_danceability) &
    (df["energy"] >= min_energy) &
    (df["tempo"].between(*tempo_range))
]

st.subheader(f"🎶 Showing {len(filtered)} tracks")
st.dataframe(
    filtered[["name", "artists", "year", "danceability", "energy", "tempo"]],
    use_container_width=True
)

st.markdown("### 📥 Download Filtered Data")
st.download_button("⬇️ Download CSV", filtered.to_csv(index=False), "filtered_tracks.csv")
