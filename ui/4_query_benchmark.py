# File: dashboard/pages/4_⚡_Query_Benchmark.py

import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="⚡ SQL Benchmarks")
st.title("⚡ SQL Query Optimization: Benchmark Study")

# 🧠 Introduction
st.markdown("""
Optimizing SQL queries can significantly reduce processing time, especially when working with large datasets like Spotify's 1.2M track dataset.

Here, we tested one **complex query** under three conditions:
- Without indexing
- With multi-column indexing
- With a temporary pre-filtered table

We compare performance and inspect PostgreSQL's execution plans.
""")

# 📄 SQL Query
st.subheader("📄 Query Used for Benchmarking")
st.markdown("""
> Find the top 5 years with the most high-energy, highly danceable explicit songs, and compute the average tempo and valence per year.
""")
query_code = """
SELECT year,
       COUNT(*) AS track_count,
       ROUND(AVG(tempo)::NUMERIC, 2) AS avg_tempo,
       ROUND(AVG(valence)::NUMERIC, 2) AS avg_valence
FROM spotify_tracks
WHERE explicit = true
  AND energy > 0.8
  AND danceability > 0.75
GROUP BY year
ORDER BY track_count DESC
LIMIT 5;
"""
st.code(query_code, language="sql")

# 🧾 Full Query Plans (Text)
st.subheader("🧾 PostgreSQL EXPLAIN ANALYZE Output")

with st.expander("📉 Raw Query Plan (Execution Time: ~89.5 ms)"):
    st.code("""
Limit  (cost=41352.63..41352.65 rows=5 width=76) (actual time=84.238..89.437 rows=5 loops=1)
  ->  Sort  (cost=41352.63..41352.87 rows=93 width=76) (actual time=84.237..89.436 rows=5 loops=1)
        Sort Key: (count(*)) DESC
        Sort Method: top-N heapsort  Memory: 25kB
        ->  Finalize GroupAggregate  (cost=41315.94..41351.09 rows=93 width=76) (actual time=83.954..89.427 rows=34 loops=1)
              Group Key: year
              ->  Gather Merge  (cost=41315.94..41346.90 rows=186 width=76) (actual time=83.941..89.346 rows=94 loops=1)
                    Workers Planned: 2
                    Workers Launched: 2
                    ->  Partial GroupAggregate  (cost=40315.92..40325.41 rows=93 width=76) (actual time=58.221..58.357 rows=31 loops=3)
                          Group Key: year
                          ->  Sort  (cost=40315.92..40317.63 rows=685 width=20) (actual time=58.215..58.260 rows=1115 loops=3)
                                Sort Key: year
                                Sort Method: quicksort  Memory: 108kB
                                Worker 0:  Sort Method: quicksort  Memory: 54kB
                                Worker 1:  Sort Method: quicksort  Memory: 90kB
                                ->  Parallel Seq Scan on spotify_tracks  (cost=0.00..40283.66 rows=685 width=20) (actual time=0.340..57.947 rows=1115 loops=3)
                                      Filter: (explicit AND (energy > '0.8'::double precision) AND (danceability > '0.75'::double precision))
                                      Rows Removed by Filter: 399294
Planning Time: 0.166 ms
Execution Time: 89.501 ms
""", language="sql")

with st.expander("⚙️ Indexed Query Plan (Execution Time: ~2.75 ms)"):
    st.code("""
Limit  (cost=4015.14..4015.15 rows=5 width=76) (actual time=2.729..2.730 rows=5 loops=1)
  ->  Sort  (cost=4015.14..4015.37 rows=93 width=76) (actual time=2.729..2.729 rows=5 loops=1)
        Sort Key: (count(*)) DESC
        Sort Method: top-N heapsort  Memory: 25kB
        ->  HashAggregate  (cost=4011.27..4013.60 rows=93 width=76) (actual time=2.683..2.720 rows=34 loops=1)
              Group Key: year
              Batches: 1  Memory Usage: 32kB
              ->  Index Scan using idx_explicit_energy_dance on spotify_tracks  (cost=0.43..3994.82 rows=1645 width=20) (actual time=0.023..2.085 rows=3344 loops=1)
                    Index Cond: ((explicit = true) AND (energy > '0.8'::double precision) AND (danceability > '0.75'::double precision))
Planning Time: 0.110 ms
Execution Time: 2.757 ms
""", language="sql")

with st.expander("📦 Temp Table Query Plan (Execution Time: ~0.59 ms)"):
    st.code("""
Limit  (cost=149.12..149.13 rows=5 width=76) (actual time=0.559..0.560 rows=5 loops=1)
  ->  Sort  (cost=149.12..149.62 rows=200 width=76) (actual time=0.559..0.559 rows=5 loops=1)
        Sort Key: (count(*)) DESC
        Sort Method: top-N heapsort  Memory: 25kB
        ->  HashAggregate  (cost=140.80..145.80 rows=200 width=76) (actual time=0.505..0.545 rows=34 loops=1)
              Group Key: year
              Batches: 1  Memory Usage: 48kB
              ->  Seq Scan on temp_explicit_energy_dance  (cost=0.00..86.40 rows=5440 width=20) (actual time=0.015..0.146 rows=3344 loops=1)
Planning Time: 0.063 ms
Execution Time: 0.586 ms
""", language="sql")

# 🔍 Visualizing PostgreSQL EXPLAIN Plans
st.subheader("🧠 Query Execution Flow (PostgreSQL EXPLAIN)")

assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets"))

with st.expander("📉 Raw Query Plan (Execution Time: 89.5 ms)"):
    st.image(Image.open(os.path.join(assets_dir, "explain_plan_unoptimized.png")), use_container_width=True)
    st.caption("Raw query without indexing or temp tables.")

with st.expander("⚙️ Indexed Query Plan (Execution Time: 2.75 ms)"):
    st.image(Image.open(os.path.join(assets_dir, "explain_plan_after_indexing.png")), use_container_width=True)
    st.caption("Indexed on explicit, energy, and danceability.")

with st.expander("📦 Temp Table Query Plan (Execution Time: 0.59 ms)"):
    st.image(Image.open(os.path.join(assets_dir, "explain_plan_after_temp_table.png")), use_container_width=True)
    st.caption("Pre-filtered temp table reduced overhead dramatically.")

# ✅ Conclusion
st.markdown("---")
st.subheader("📌 Key Takeaways")
st.markdown("""
- 🔎 **Indexing** significantly reduced query time from ~89ms to ~2.7ms.
- 📦 **Temp tables** offered further optimization (~0.5ms), ideal when filtering logic is reused.
- 🧠 PostgreSQL’s EXPLAIN plans provide insights into why optimizations work.

This benchmark showcases the **real-world performance gains** of applying thoughtful database design.
""")
