# https://www.kaggle.com/datasets/uetchy/vtuber-livechat-elements
# https://www.kaggle.com/datasets/maliqr/vtuber-like-views-and-subscriber-data

from flask import *
# import pandas as pd
import sqlite3
import kagglehub
from kagglehub import *
from pathlib import Path

ROOT = Path(__file__).parent
URL = [
   "uetchy/vtuber-livechat-elements",
   "maliqr/vtuber-like-views-and-subscriber-data"
]
PATH = [
    "?select=channels.csv",
    "?select=chat_stats.csv"
]

def downloadDataset() -> str:
    return kagglehub.dataset_download("uetchy/vtuber-livechat-elements")

def downloadDatasetWPath() -> str:
    return kagglehub.dataset_download("uetchy/vtuber-livechat-elements", "channels.csv")


# def csv_to_db(csv_path: Path, db_path: Path, table_name: str) -> None:
#     df = pd.read_csv(csv_path)
#     conn = sqlite3.connect(db_path)
#     df.to_sql(table_name, conn, if_exists="replace", index=False)
#     conn.close()

if __name__ == "__main__":
    tables_dir = ROOT / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    downloadDataset()

    # csv_to_db(csv_path, db_path, f"data{i}")
