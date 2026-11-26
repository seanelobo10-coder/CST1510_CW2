from pathlib import Path
import pandas as pd
import requests

URL = "https://disease.sh/v3/covid-19/countries"
PARAMS = {}
RECORDS_KEY = None
RENAME = {}
KEEP = ["country", "continent", "cases", "deaths", "recovered", "tests", "population", "active"]
MUST_HAVE = ["cases", "continent"]
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"


def get_data(url, params):
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print("Could not get the data:", e)
        return None


def make_table(data, records_key):
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")


def tidy_data(df):
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df


def save_data(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    data = get_data(URL, PARAMS)
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
        print(table.head())
        save_data(table, RAW_FILE)