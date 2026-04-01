import requests
import json
import random
import urllib.request
import sqlite3, os
from typing import List, Dict, Optional

DB_FILE = "oshi.db"

# Build Databse

db = sqlite3.connect(DB_FILE)
cursor = db.cursor()


cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
    );
    """
)
