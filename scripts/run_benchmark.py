import psycopg2
import time
import pandas as pd

QUERIES = {
    "raw_query_1": "scripts/query_optimization/01_raw_queries.sql",
    "indexed_query_1": "scripts/query_optimization/02_indexed_queries.sql",
    "temp_table_query_1": "scripts/query_optimization/03_temp_table_queries.sql"
}

def run_and_time_query(conn, sql_file):
    with open(sql_file, 'r') as f:
        query = f.read()
    with conn.cursor() as cur:
        start = time.time()
        cur.execute(query)
        try:
            _ = cur.fetchall()
        except:
            pass
        end = time.time()
    return round(end - start, 4)

if __name__ == "__main__":
    conn = psycopg2.connect(dbname="spotify_db", user="postgres", password="admin")

    results = []
    for label, path in QUERIES.items():
        exec_time = run_and_time_query(conn, path)
        print(f"{label} ran in {exec_time} sec")
        results.append({"query": label, "exec_time_sec": exec_time})

    df = pd.DataFrame(results)
    df.to_csv("scripts/query_optimization/query_summary.csv", index=False)
    print("Benchmark results saved to query_summary.csv")