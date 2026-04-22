# Jun Jie Li (PM), Shafin Kazi, Lucas Zheng, Kyle Liu
# lowCortisol
# SoftDev pd4
# p04
# 2026-04-21

import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.request

DB_FILE = "oshi.db"
URL = "https://holodex.net/api/v2/channels/"
DELAY_SECONDS = 0.3
TIMEOUT = 10

API_KEY = os.environ.get("HOLODEX_API_KEY", "").strip()
if not API_KEY:
    sys.exit("\n  Missing HOLODEX_API_KEY.\n")

def fetch_channel(channel_id):
    req = urllib.request.Request(
        URL + channel_id,
        headers={
            "X-APIKEY": API_KEY,
            "Accept": "application/json",
            "User-Agent": "oshi.me/1.0 (lowCortisol)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        if e.code == 429:
            print("rate limited")
            time.sleep(30)
        else:
            print(f"HTTP {e.code} for {channel_id}")
        return None
    except Exception as e:
        print(f"error for {channel_id}: {e}")
        return None


def main():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()

    rows = cursor.execute(
        "SELECT channel_id, channel_name, profile_image_url FROM vtubers"
    ).fetchall()

    total = len(rows)
    updated = unchanged = not_found = no_photo = 0

    for i, (channel_id, name, current_url) in enumerate(rows, 1):
        label = (name or channel_id)[:42]
        print(f"[{i:>4}/{total}] {label:<44}", end=" ", flush=True)

        data = fetch_channel(channel_id)

        if data is None:
            not_found += 1
            print("not on holodex")
        elif not data.get("photo"):
            no_photo += 1
            print("no photo field")
        elif data["photo"] == current_url:
            unchanged += 1
            print("already current")
        else:
            cursor.execute(
                "UPDATE vtubers SET profile_image_url = ? WHERE channel_id = ?",
                (data["photo"], channel_id),
            )
            db.commit()
            updated += 1
            print("updated")

        time.sleep(DELAY_SECONDS)

    db.close()

    print(
        f"\nDone."
        f"\n  updated:       {updated}"
        f"\n  already good:  {unchanged}"
        f"\n  not on holodex:{not_found}"
        f"\n  no photo:      {no_photo}"
    )


if __name__ == "__main__":
    main()