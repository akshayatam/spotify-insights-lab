import streamlit as st

pg = st.navigation( 
    [ 
        st.Page("home_page.py", title="Home", icon="🏠"),
        st.Page("0_global_dashboard.py", title="Global Dashboard", icon="🌍"), 
        st.Page("1_track_explorer.py", title="Track Explorer", icon="🎵"), 
        st.Page("2_mood_clusters.py", title="Mood Clusters", icon="🔍"), 
        st.Page("3_promotion_model.py", title="Promotion Model", icon="📈"), 
        st.Page("4_query_benchmark.py", title="Query Benchmark", icon="⚡")
    ]
) 
st.set_page_config(
    page_title="Spotifdy Insights Lab",
    page_icon="🎧",
    # layout="wide",
) 
pg.run() 
