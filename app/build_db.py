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
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT
    );
    """
)
