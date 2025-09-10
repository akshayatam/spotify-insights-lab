import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="🔍 Mood Clusters")
st.title("🔍 Mood-Based Clustering")

@st.cache_data
def load_data():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "spotify_tracks_with_clusters.csv"))
    return pd.read_csv(path)

df_full = load_data()

# Sample for faster loading (used in plot only)
df_sampled = df_full.sample(frac=0.2, random_state=42)

st.markdown("""
This section clusters Spotify tracks into **mood-based groups** using audio features like *valence*, *energy*, and *danceability*.  
We use **KMeans clustering** and visualize the groups with **t-SNE**, a technique for dimensionality reduction that preserves local structure.

🎯 **Why?**  
To understand how songs naturally group based on mood and energy — uncovering patterns not visible in raw audio metrics.

💡 **Note:**  
To ensure performance, only **20% of tracks are shown** in the visual map below. All filters and summaries work on the full dataset.
""")

# Sidebar cluster selector
cluster = st.sidebar.selectbox("🎨 Select Cluster", sorted(df_full["cluster"].unique()))
st.sidebar.markdown("---")

# Filter full data by cluster
filtered = df_full[df_full["cluster"] == cluster]

st.subheader(f"🌈 Cluster {cluster} — {len(filtered)} tracks")
st.dataframe(filtered[["name", "artists", "valence", "energy", "danceability"]])

# t-SNE Plot using sampled data
st.markdown("---")
st.markdown("### 🗺️ Mood Landscape (t-SNE Projection)")

# Limit width using columns
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    fig = px.scatter(
        df_sampled,
        x="tsne_1",
        y="tsne_2",
        color="cluster",
        hover_data=["name", "artists"],
        title="t-SNE Mood Clusters (sampled view)"
    )
    fig.update_layout(template="plotly_dark", height=500, width=600)
    st.plotly_chart(fig, use_container_width=False)
