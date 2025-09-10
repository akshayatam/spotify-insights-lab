import streamlit as st
from PIL import Image 
from pathlib import Path

# Page name
st.set_page_config(
    page_title="Spotify Insights Lab",
    page_icon="🎧",
    # layout="wide",
)

# Header and Intro
st.title("🎧 Spotify Insights Lab") 

image = Image.open("assets/spotify_logo.png")
st.image(image, width="stretch")

st.markdown("""
### 👋 Hello there!
Welcome to **Spotify Insights Lab** — a project that blends machine learning, SQL tuning, and data storytelling to explore what makes music tick.

Built using over **1.2 million tracks**, this app lets you:
- 🎵 Explore songs by danceability, energy, and vibe
- 🔍 Discover mood-based clusters using audio features
- 📈 Predict which songs might get promoted
- ⚡ Benchmark SQL query performance like a Spotify data engineer

---

### Features 
- 🎵 Music clustering using ML (KMeans + t-SNE)
- 📈 Promotion prediction using XGBoost
- ⚡ SQL query optimization experiments

---

### 🧑‍💻 Why I Built This
Spotify has been more than just a music app to me — it shaped my taste, habits, and even my understanding of what data can do. This project is a tribute to that journey, while also being a technical playground:

- ✅ For **ML/DS roles**: I demonstrate modeling, clustering, feature analysis, SHAP, and pipelines
- ✅ For **Data Engineer / Analyst**: I optimize SQL queries, benchmark performance, and clean 1.2M+ rows
- ✅ For **Product / Portfolio**: The Streamlit dashboard provides story + insight + functionality

---

### 🚀 Stack Used
- Python (Pandas, Scikit-learn, XGBoost)
- Streamlit for the dashboard
- Plotly for charts
- PostgreSQL for SQL optimization

---

### ❤️ Thank You for Visiting
If you're from Spotify or just a music + data nerd like me — thanks for being here!
""")

# Personal Note 
st.markdown("""
> 💬 _“Spotify has always felt personal to me — long before it launched in India. This project is my way of paying tribute to the platform that changed how I listen, and showcasing the skills I bring to the table as an ML engineer.”_

Explore the pages from the sidebar to dive into the insights.
""")