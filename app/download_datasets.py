# https://www.kaggle.com/datasets/uetchy/vtuber-livechat-elements
# https://www.kaggle.com/datasets/maliqr/vtuber-like-views-and-subscriber-data

from flask import *
# import pandas as pd
import sqlite3
# import kagglehub
import os
from pathlib import Path

ROOT = Path(__file__).parent
chat_dir = ROOT / "chatStats"
chat_dir.mkdir(parents=True, exist_ok=True)


os.system(f"kaggle datasets download uetchy/vtuber-livechat-elements -p {chat_dir} --unzip")

os.system(f"kaggle datasets download maliqr/vtuber-like-views-and-subscriber-data -f masterData.csv -p {chat_dir} --unzip")
