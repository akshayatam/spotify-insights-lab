# 📊 Query Optimization Case Study (PostgreSQL `EXPLAIN ANALYZE`)

This section compares how PostgreSQL executes a complex query using:

- ❌ No optimization (raw query)
- ✅ Multicolumn index
- ✅ TEMP TABLE reuse

---

## 🧠 Query 

> *Find the top 5 years with the most high-energy, highly danceable explicit songs, and compute the average tempo and valence per year.*

```sql
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
``` 

--- 

## 🧪 Execution Time Summary 

| Query Type | Execution Time | Access Method | Notes | 
| :---: | :---: | :---: | :---: | 
| Raw | 89.5 ms | Parallel Sequence Scan | Full table scan on 1.2M+ rows | 
| Indexed | 2.75 ms | Index Scan | ~32x faster; index used for filtering | 
| Temp Table | 0.58 ms | Sequence Scan (temp) | Fastest; operates only on filtered subset | 

--- 

## 📌 Plan Highlights 

### 1. Raw Query 

``` 
"QUERY PLAN"
"Limit  (cost=41352.63..41352.65 rows=5 width=76) (actual time=84.238..89.437 rows=5 loops=1)"
"  ->  Sort  (cost=41352.63..41352.87 rows=93 width=76) (actual time=84.237..89.436 rows=5 loops=1)"
"        Sort Key: (count(*)) DESC"
"        Sort Method: top-N heapsort  Memory: 25kB"
"        ->  Finalize GroupAggregate  (cost=41315.94..41351.09 rows=93 width=76) (actual time=83.954..89.427 rows=34 loops=1)"
"              Group Key: year"
"              ->  Gather Merge  (cost=41315.94..41346.90 rows=186 width=76) (actual time=83.941..89.346 rows=94 loops=1)"
"                    Workers Planned: 2"
"                    Workers Launched: 2"
"                    ->  Partial GroupAggregate  (cost=40315.92..40325.41 rows=93 width=76) (actual time=58.221..58.357 rows=31 loops=3)"
"                          Group Key: year"
"                          ->  Sort  (cost=40315.92..40317.63 rows=685 width=20) (actual time=58.215..58.260 rows=1115 loops=3)"
"                                Sort Key: year"
"                                Sort Method: quicksort  Memory: 108kB"
"                                Worker 0:  Sort Method: quicksort  Memory: 54kB"
"                                Worker 1:  Sort Method: quicksort  Memory: 90kB"
"                                ->  Parallel Seq Scan on spotify_tracks  (cost=0.00..40283.66 rows=685 width=20) (actual time=0.340..57.947 rows=1115 loops=3)"
"                                      Filter: (explicit AND (energy > '0.8'::double precision) AND (danceability > '0.75'::double precision))"
"                                      Rows Removed by Filter: 399294"
"Planning Time: 0.166 ms"
"Execution Time: 89.501 ms"
``` 

- PostgreSQL scans the entire table with 2 workers. 
- Efficient for one-off queries, but not reusable. 
- Sorting done with **top-N heapsort**. 

### 2. Indexed Query 

``` 
"QUERY PLAN"
"Limit  (cost=4015.14..4015.15 rows=5 width=76) (actual time=2.729..2.730 rows=5 loops=1)"
"  ->  Sort  (cost=4015.14..4015.37 rows=93 width=76) (actual time=2.729..2.729 rows=5 loops=1)"
"        Sort Key: (count(*)) DESC"
"        Sort Method: top-N heapsort  Memory: 25kB"
"        ->  HashAggregate  (cost=4011.27..4013.60 rows=93 width=76) (actual time=2.683..2.720 rows=34 loops=1)"
"              Group Key: year"
"              Batches: 1  Memory Usage: 32kB"
"              ->  Index Scan using idx_explicit_energy_dance on spotify_tracks  (cost=0.43..3994.82 rows=1645 width=20) (actual time=0.023..2.085 rows=3344 loops=1)"
"                    Index Cond: ((explicit = true) AND (energy > '0.8'::double precision) AND (danceability > '0.75'::double precision))"
"Planning Time: 0.110 ms"
"Execution Time: 2.757 ms"
``` 

- Index used effectively for multi-column filter. 
- Reduces I/O directly. 
- Ideal when filters are **selective** and sorting is minimal. 

### 3. `TEMP TABLE` Query 

``` 
"QUERY PLAN"
"Limit  (cost=149.12..149.13 rows=5 width=76) (actual time=0.559..0.560 rows=5 loops=1)"
"  ->  Sort  (cost=149.12..149.62 rows=200 width=76) (actual time=0.559..0.559 rows=5 loops=1)"
"        Sort Key: (count(*)) DESC"
"        Sort Method: top-N heapsort  Memory: 25kB"
"        ->  HashAggregate  (cost=140.80..145.80 rows=200 width=76) (actual time=0.505..0.545 rows=34 loops=1)"
"              Group Key: year"
"              Batches: 1  Memory Usage: 48kB"
"              ->  Seq Scan on temp_explicit_energy_dance  (cost=0.00..86.40 rows=5440 width=20) (actual time=0.015..0.146 rows=3344 loops=1)"
"Planning Time: 0.063 ms"
"Execution Time: 0.586 ms"
``` 

- Operates only on pre-filtered rows in `TEMP TABLE`. 
- Best performance for modular dashboards or repeated use. 
- Planning time is very low. 

--- 

## Conclusion 

| Insight | Explanation | 
| --- | --- | 
| Indexing reduced execution time by ~32x | 89.5 ms → 2.75 ms | 
| `TEMP TABLE` improved further by 5x | 2.75 ms → 0.58 ms | 
| Sequential scan isn't always worse | Raw query performs well when not reused | 
| Index is best for **targeted filtering** | `TEMP TABLE`s are better for **repeatable filters** | 
