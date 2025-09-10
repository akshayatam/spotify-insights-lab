import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

csv_path = "./data/spotify_tracks_cleaned.csv"
parquet_path = "./data/spotify_tracks_cleaned.parquet"

# dtype hints help reduce size & speed IO (optional but recommended)
dtype = {
    # "explicit": "boolean",  # if 0/1, convert after read
    # put known small ints/cats here later…
}

df = pd.read_csv(csv_path, dtype=dtype)
# Example compacting:
if "explicit" in df.columns and df["explicit"].dtype != "bool":
    df["explicit"] = df["explicit"].astype("bool")
for col in df.select_dtypes(include="object").columns:
    # Often safe to categorical-ize (review high-cardinality columns later)
    if df[col].nunique() / len(df) < 0.9:
        df[col] = df[col].astype("category")

table = pa.Table.from_pandas(df, preserve_index=False)
pq.write_table(table, parquet_path, compression="zstd", use_dictionary=True)
