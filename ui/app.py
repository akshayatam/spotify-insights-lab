import streamlit as st
from PIL import Image 
from st_pages import Page, show_pages, add_page_title
from pathlib import Path

# Page name
st.set_page_config(
    page_title="Spotify Insights Lab",
    page_icon="🎧",
    # layout="wide",
)

# Header and Intro
st.title("🎧 Spotify Insights Lab")
st.markdown("""
Welcome to **Spotify Insights Lab** — a project that blends machine learning, SQL tuning, and data storytelling to explore what makes music tick.

Built using over **1.2 million tracks**, this app lets you:
- 🎵 Explore songs by danceability, energy, and vibe
- 🔍 Discover mood-based clusters using audio features
- 📈 Predict which songs might get promoted
- ⚡ Benchmark SQL query performance like a Spotify data engineer

---
""")

image = Image.open("assets/spotify_logo.png")
st.image(image, use_container_width=True)

# Personal Note 
st.markdown("""
> 💬 _“Spotify has always felt personal to me — long before it launched in India. This project is my way of paying tribute to the platform that changed how I listen, and showcasing the skills I bring to the table as an ML engineer.”_

Explore the pages from the sidebar to dive into the insights.
""")