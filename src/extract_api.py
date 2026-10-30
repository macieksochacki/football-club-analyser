import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FOOTBALL_DATA_API_KEY")
print(api_key is not None)

url = "https://api.football-data.org/v4/competitions/PL/standings"
headers = {"X-Auth-Token": api_key}
response = requests.get(url, headers=headers)
print(response.status_code)

data = response.json()


area = data["area"]
standings = data["standings"]
first = standings[0]
table = first["table"]
print(len(table))
#table = data["standings"][0]["table"]

df = pd.json_normalize(table)
print(df.shape)
print(df.columns.tolist())