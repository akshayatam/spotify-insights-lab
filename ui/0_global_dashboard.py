import streamlit as st
import pandas as pd
import plotly.express as px
import os 
import time 

st.set_page_config(page_title="🌍 Global Dashboard", layout="wide")
st.title("🌍 Global Music Insights Dashboard")

# Load Data
@st.cache_data
def load_data(): 
    start = time.perf_counter() 
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    df = pd.read_csv(os.path.join(project_root, "data", "spotify_tracks_cleaned.csv")) 
    load_time = time.perf_counter() - start 
    return df, load_time 

df, load_time = load_data()

# --- Hero Metrics
st.subheader("📊 At a Glance")
st.success(f"✅ Loaded {len(df):,} rows in **{load_time:.2f} seconds**") 
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tracks", f"{len(df):,}")
col2.metric("% Explicit", f"{(df['explicit'].mean()*100):.2f}%")
col3.metric("Avg Duration", f"{df['duration_min'].mean():.2f} min")
if "promoted" in df.columns:
    col4.metric("% Promoted", f"{df['promoted'].mean()*100:.2f}%")
else:
    col4.metric("Promoted", "N/A")

# --- Trends: Split into 3 Charts
st.markdown("### 📈 Trends Over Time (Separated by Feature)")
yearly = df.groupby("year")[["tempo", "valence", "energy"]].mean().reset_index()

col1, col2, col3 = st.columns(3)

with col1:
    fig_tempo = px.line(yearly, x="year", y="tempo", markers=True, title="🎵 Avg Tempo by Year")
    fig_tempo.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig_tempo, use_container_width=True)

with col2:
    fig_valence = px.line(yearly, x="year", y="valence", markers=True, title="😊 Avg Valence by Year")
    fig_valence.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig_valence, use_container_width=True)

with col3:
    fig_energy = px.line(yearly, x="year", y="energy", markers=True, title="⚡ Avg Energy by Year")
    fig_energy.update_layout(template="plotly_dark", height=300)
    st.plotly_chart(fig_energy, use_container_width=True)

# --- Audio Distributions
st.markdown("### 🎵 Audio Feature Distributions")
features = ["danceability", "energy", "valence"]
for feat in features:
    fig = px.histogram(df, x=feat, nbins=30, title=f"{feat.title()} Distribution")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- Top Artists & Albums
st.markdown("### 🧑‍🎤 Most Common Artists & Albums")
top_artists = df['artists'].value_counts().nlargest(10)
fig1 = px.bar(top_artists, title="Top 10 Artists")
fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

top_albums = df['album'].value_counts().nlargest(10)
fig2 = px.bar(top_albums, title="Top 10 Albums")
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# --- Promotion Heatmap (if available)
if "promoted" in df.columns:
    st.markdown("### 🎯 Promotion Hotspots (Valence vs Energy)")
    fig3 = px.scatter(
        df, x="valence", y="energy", color=df["promoted"].map({1: "Promoted", 0: "Not Promoted"}),
        opacity=0.5, title="Promoted Track Clusters"
    )
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

# --- Download Section
st.markdown("### 📥 Download Full Dataset")
st.download_button("Download CSV", df.to_csv(index=False), "spotify_cleaned.csv")