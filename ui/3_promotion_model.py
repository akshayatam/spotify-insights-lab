import streamlit as st
import pandas as pd
import os
import plotly.express as px
import joblib
from transformers import pipeline

st.set_page_config(page_title="📈 Promotion Model", layout="wide")
st.title("📈 Promotion Probability Predictor")

# ----------------- Load Data and Model -----------------
@st.cache_data
def load_data():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "spotify_tracks_with_clusters_and_uplift.csv"))
    return pd.read_csv(path)

df = load_data()

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "xgb_promotion_model.pkl"))
model = joblib.load(model_path)

features = [
    'danceability', 
    'energy', 
    'loudness', 
    'speechiness', 
    'acousticness', 
    'instrumentalness', 
    'liveness', 
    'valence', 
    'tempo', 
    'duration_min', 
    'year'
]

# ----------------- Description -----------------
st.markdown("""
🎯 This model estimates the **likelihood of a track being promoted** — mimicking real-world campaign targeting using a combination of **audio features** and **metadata**.

🧪 Since real promotion labels weren't available, I created **synthetic uplift-style labels** using a heuristic formula based on *valence*, *energy*, and *danceability*, with added random noise to simulate real-world messiness.

> 💡 This is just a **proof-of-concept** for how machine learning might be used to assist music promotion teams in filtering tracks based on vibe and virality signals.

---
""")

# ----------------- Track Selection -----------------
st.markdown("### 🎧 Select a Track")
col1, col2 = st.columns(2)

with col1:
    selected_album = st.selectbox("💿 Album", sorted(df["album"].unique()))
with col2:
    tracks_in_album = df[df["album"] == selected_album]["name"].unique()
    target_track = st.selectbox("🎵 Track", sorted(tracks_in_album))

track_row = df[(df["album"] == selected_album) & (df["name"] == target_track)].iloc[0]
input_features = track_row[features].values.reshape(1, -1)

# ----------------- Prediction -----------------
pred_proba = model.predict_proba(input_features)[0, 1]
st.metric("📈 Promotion Likelihood", f"{pred_proba * 100:.2f}%")

# ----------------- Feature Importance -----------------
st.markdown("---")
st.subheader("🧠 Global Feature Importance")

st.markdown("These importances reflect the **overall model behavior**, not specific to the selected track.")

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

fig = px.bar(
    importance_df,
    x="Feature",
    y="Importance",
    title="XGBoost Feature Importances (Global)",
    labels={"Importance": "Importance Score"},
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

# ----------------- LLM Explanation -----------------
st.markdown("---")
st.subheader("🤖 AI Explanation of Promotion Likelihood")

st.markdown("""
This section uses a Hugging Face hosted model to explain why the selected track might be promoted.
If you're seeing an error, make sure you're using a model that doesn't require gated access.
""")

@st.cache_resource
def load_llm():
    return pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-alpha")

llm = load_llm()

prompt = f"""
Explain why the following track might be considered for promotion based on its musical attributes:

Track: {target_track}
Album: {selected_album}

Audio Features:
Danceability: {track_row['danceability']}, Energy: {track_row['energy']}, Loudness: {track_row['loudness']},
Speechiness: {track_row['speechiness']}, Acousticness: {track_row['acousticness']}, Instrumentalness: {track_row['instrumentalness']},
Liveness: {track_row['liveness']}, Valence: {track_row['valence']}, Tempo: {track_row['tempo']} BPM,
Duration: {track_row['duration_min']:.2f} min, Year: {track_row['year']}

Be concise, insightful, and music-aware.
"""

with st.spinner("Generating explanation with LLM..."):
    explanation = llm(prompt, max_new_tokens=120)[0]['generated_text'].split("\n")[-1]

st.markdown(f"> {explanation}")

# ----------------- Evaluation Metrics -----------------
st.markdown("---")
st.subheader("📊 Model Performance")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**📊 Precision / Recall / F1 Score**")

    metrics_data = {
        "Class": ["Not Promoted (0)", "Promoted (1)", "Macro Avg", "Weighted Avg"],
        "Precision": [0.95, 0.95, 0.95, 0.95],
        "Recall":    [0.98, 0.85, 0.92, 0.95],
        "F1 Score":  [0.97, 0.90, 0.93, 0.95]
    }

    metrics_df = pd.DataFrame(metrics_data)
    st.table(metrics_df)

with col2:
    st.markdown("**AUC Score**")
    st.metric(label="ROC AUC", value="0.9188")

# ----------------- Footer -----------------
st.markdown("""
---
🔬 _Note: Feature importances are derived from the trained model and do not change based on the selected track._

🧠 Want deeper insights? Future versions will include **SHAP-based explanations** to show *why* a track received its score.
""")
