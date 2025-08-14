import streamlit as st

st.set_page_config(page_title="💬 About")
st.title("💬 About This Project")

st.markdown("""
### 👋 Hello there!

Welcome to **Spotify Insights Lab** — a personal yet production-grade project that explores:
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
