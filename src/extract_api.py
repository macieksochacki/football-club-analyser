import os
import requests
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import duckdb

load_dotenv()
api_key = os.getenv("FOOTBALL_DATA_API_KEY")

url = "https://api.football-data.org/v4/competitions/PL/standings"
headers = {"X-Auth-Token": api_key}
response = requests.get(url, headers=headers)
print(response.status_code)

data = response.json()

standings = data["standings"]
first = standings[0]
table = first["table"]

df = pd.json_normalize(table)
df.columns = df.columns.str.replace(".", "_", regex=False)
print(df.shape)
print(df.columns.tolist())

Path("data").mkdir(exist_ok=True)

DB_PATH = Path("data/football.duckdb")

with duckdb.connect(str(DB_PATH)) as con:
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    con.execute("CREATE OR REPLACE TABLE raw.api_standings AS SELECT * FROM df")
    rows = con.execute("SELECT COUNT(*) FROM raw.api_standings").fetchone()[0]
    
print(f"raw.api_standings: {rows:,} rows")