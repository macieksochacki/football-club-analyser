# Football Club Analyser

An ETL pipeline that automates club squad and transfer analysis on Transfermarkt data, built with Python, SQL and DuckDB.

**Status: in progress.** Extract and load steps work; SQL transformations, data validation and reporting are next.

## Why

During my internship as a scouting and data analyst I analysed clubs by hand: squad age structure, minutes distribution, foreign players and transfer activity. One club took hours of copying numbers from Transfermarkt into spreadsheets. This project turns that manual procedure into a reproducible pipeline that can analyse any club, or a whole league, in one run.

## Pipeline

```
download.py  ->  data/raw/*.csv  ->  load.py  ->  DuckDB (raw)  ->  SQL: staging  ->  SQL: marts  ->  report
   Extract                            Load                          Transform
```

| Step | What it does | Status |
|---|---|---|
| Extract | `src/download.py` downloads the public transfermarkt-datasets package and unpacks the raw CSV files | Done |
| Load | `src/load.py` loads every raw table into a local DuckDB database (`raw` schema) | Done |
| Explore | `notebooks/explore.ipynb`: profiling tables, row counts, coverage checks in SQL | In progress |
| Transform | Layered SQL models: `staging` (cleaned, typed) and `marts` (club level metrics) | Next |
| Validate | Data quality checks: missing birth dates, duplicates, more than 90 minutes per player per match | Planned |
| Report | `report.py`: league and season in, comparison table (CSV) and charts out | Planned |

## Data

Source: [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets) by dcaribou (public, no API key needed).

Loaded so far: 1.89M player appearances, 89k games, 796 clubs, 65 competitions, plus players, transfers and market valuations.

Known limitations, found while exploring:

* Updates of the source are paused; data ends in July 2026, so the 2025/26 season is the latest complete one.
* Average of about 21 recorded appearances per game, below the 26 to 28 players who usually take part, which suggests incomplete lineups for some games (likely cup and lower league matches). This will be covered by the validation step.
* Coverage is limited to selected leagues, not every competition.

## Planned metrics (marts)

* Share of minutes played by U23 and 30+ players per club and season
* Number and origin of foreign players
* Incoming and outgoing transfers by age bracket, with fees and market values

## How to run

```bash
git clone https://github.com/macieksochacki/football-club-analyser.git
cd football-club-analyser
pip install duckdb pandas matplotlib
python src/download.py   # Extract: downloads and unpacks the data (a few hundred MB)
python src/load.py       # Load: builds data/football.duckdb
```

Raw data and the database are not stored in the repo (see `.gitignore`); the scripts recreate them.

## Tech

Python, pandas, DuckDB, SQL, Jupyter, Git
