# 🎧 Spotify Insights Lab – ML Meets Music

What makes a song *promotable*? Can we predict what tracks deserve the spotlight based on their sound alone?  
**Spotify Insights Lab** is an interactive ML-powered dashboard built to answer exactly that: merging audio science, machine learning, and music love into one powerful app.

---

## 🚀 Overview

This project explores the **vibe, virality, and promotion potential** of over **1.2 million tracks** from Spotify’s dataset. It features:

- 📊 **Global audio trends** over the years
- 🧠 **Track promotion prediction** with a trained XGBoost model
- 🔍 **Feature importance & evaluation metrics**
- 🧪 GPT-ready explanations (via Hugging Face integration)
- 🎛️ Clean, professional **Streamlit UI**
- 🎼 Explorations by album, artist, and genre

All designed to mimic a real-world music marketing workflow — with synthetic uplift-based labels, robust model training, and future plans for SHAP explainability.

---

## 🧠 Why I Built This

Spotify wasn’t even available in India when I first wanted to use it. I remember reading launch rumors, checking for app availability - and waiting.

Years later, I built this project as a personal tribute — not just to Spotify, but to the idea of making music *measurable*. How can we decode the rhythm of a hit? Can we explain what makes people dance?

This project is my way of combining that question with AI.

---

## 📂 Folder Structure

```
spotify-query-lab/
├── dashboard/
│ └── pages/
│ ├── 0_Home.py
│ ├── 1_Global_Dashboard.py
│ ├── 2_Cluster_Graph.py
│ ├── 3_Promotion_Model.py ← 📈 Promotion Likelihood + GPT Insights
├── data/
│ ├── spotify_tracks_cleaned.csv
│ └── spotify_tracks_with_clusters_and_uplift.csv
├── models/
│ └── xgb_promotion_model.pkl
├── scripts/
│ ├── clustering_and_labeling.py
│ └── train_xgb_model.py
├── requirements.txt
└── README.md
```

## ⚙️ Features

### 🌍 Global Dashboard
- Trends over time: Tempo, Energy, Valence
- Distribution histograms of key audio features
- Top artists, albums, and audio metadata

### 📈 Promotion Model
- Predicts probability of a track being promoted
- Built using **XGBoost**, trained on uplift-style labels
- Shows feature importance, AUC, and class metrics
- **GPT integration** (Hugging Face) to explain predictions *(early stage)*

### 🎛️ Clustering & Uplift Labels
- Clusters tracks based on audio feature embeddings
- Assigns synthetic *promotion likelihood* via valence/energy/danceability
- Preprocessing, modeling, and visualization scripts included

---

## 📉 Model Performance

| Metric          | Score  |
|-----------------|--------|
| ROC AUC         | 0.9188 |
| F1 Score (1)    | 0.90   |
| Precision (1)   | 0.95   |
| Recall (1)      | 0.85   |

✅ **High confidence predictions** with room to explore interpretability via SHAP and causal methods.

---

## 🔮 Coming Soon

- SHAP-based local + global explainability
- Cohort/genre-wise segment analysis
- Spotify API integration
- Streamlit Cloud live deployment
- PDF insight reports for each track

---

## 🛠️ Tech Stack

| Layer        | Tools Used |
|--------------|------------|
| Language     | Python 3.12 |
| ML Modeling  | scikit-learn, XGBoost |
| Dashboard    | Streamlit, Plotly |
| LLM Integration | Hugging Face Transformers |
| Data Size    | ~1.2 million rows |
