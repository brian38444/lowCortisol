# https://www.kaggle.com/datasets/uetchy/vtuber-livechat-elements
# https://www.kaggle.com/datasets/maliqr/vtuber-like-views-and-subscriber-data

from flask import *
import pandas as pd
import sqlite3

import argparse
import subprocess
import json
import os
import shutil
import sys
import time
import urllib.request
import zipfile
import kagglehub
from kagglehub import KaggleDatasetAdapter
from pathlib import Path

ROOT = Path(__file__).parent
URL = [
    "uetchy/vtuber-livechat-elements",
    "maliqr/vtuber-like-views-and-subscriber-data"
]
#
# def download(url: str, destination: Path) -> Path:
#     if destination.exists():
#         print("Dataset already downloaded")
#         return destination
#
#     try:
#         urllib.request.urlretrieve(url, str(destination)) # Maybe add reporthook= for progress if time (maybe don't even add if folder is small)
#     except Exception as e:
#         if destination.exists():
#             destination.unlink()
#         print(e)
#         print("\nTry runnning download_datasets.py again")
#         sys.exit(1)
#
#     return destination
#
def csv_to_db(csv_path: str, db_path: str, table_name: str) -> None:
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
#
# def extract(zip_path: Path, destination: Path) -> Path:
#     if destination.exists():
#         print("Dataset already extracted")
#         return destination
#
#     with zipfile.ZipFile(zip_path, "r") as zf:
#         zf.extractall(destination)
#
#     zip_path.unlink()
#     return destination

def kaggle_download() -> None:
    for i in range(len(URL)):
        kagglehub.dataset_download(URL[i], path='datasets')

if __name__ == "__main__":
    for i in range(len(URL)):
        # download(URL[i], ROOT / "datasets" / "data.zip")
        # extract(ROOT / "datasets" / "data.zip", ROOT / "datasets" / "extracted") # Subsequently deletes ZIP File
        kaggle_download()
        csv_to_db(ROOT / "datasets", ROOT / "app" / "tables" / f"db{i}", f"data{i}") # Lwk redundant or smth someone can optimize
