"""Load step: load raw CSV files into DuckDB (raw layer)."""
from pathlib import Path
import duckdb

RAW_DIR = Path("data/raw")
DB_PATH = Path("data/football.duckdb")
TABLES = ["players", "clubs", "competitions", "games", "appearances", "transfers"]


def load_tables(con: duckdb.DuckDBPyConnection, tables: list[str]) -> None:
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    for table in tables:
        csv_path = RAW_DIR / f"{table}.csv.gz"
        con.execute(
            f"CREATE OR REPLACE TABLE raw.{table} AS "
            f"SELECT * FROM read_csv_auto('{csv_path}')"
        )
        rows = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
        print(f"raw.{table}: {rows:,} rows")


if __name__ == "__main__":
    with duckdb.connect(str(DB_PATH)) as con:
        load_tables(con, TABLES)