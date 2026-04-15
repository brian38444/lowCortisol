import sqlite3
import csv
import os

DB_FILE = "oshi.db"

def load(filename):
    with open(filename, newline="") as f:
        return list(csv.DictReader(f))


db = sqlite3.connect(DB_FILE)
c = db.cursor()

channels = load("chatStats/channels.csv")
c.executemany(
    """
    INSERT OR IGNORE INTO vtubers
        (channel_id, channel_name, profile_image_url, agency,
            total_subscriber_count, total_videos)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    [
        (
            r["channelId"],
            r["englishName"] or r["name"],
            r["photo"],
            r["affiliation"],
            int(r["subscriptionCount"] ),
            int(r["videoCount"] ),
        )
        for r in channels
    ],
)

master = load("chatStats/masterData.csv")
for r in master:
    c.execute(
        """
        UPDATE vtubers SET
            channel_url = ?,
            total_views = ?,
            total_likes = ?,
            total_comments = ?,
            avg_views = ?,
            avg_likes = ?,
            total_subscriber_count = ?,
            total_videos = ?
        WHERE channel_id = ?
        """,
        (
            f"https://youtube.com/{r['customUrl']}",
            int(float(r["total_views"])),
            int(float(r["total_likes"])),
            int(float(r["total_comment"])),
            int(float(r["avg_views"])),
            int(float(r["avg_likes"])),
            int(float(r["total_subs"])),
            int(float(r["total_video"])),
            r["id"],
        ),
    )


chats = load("chatStats/chat_stats.csv")
# only insert rows where the channel exists in vtubers for continuity 
c.executemany(
    """
    INSERT OR REPLACE INTO chats
        (channel_id, period, chats, member_chats, unique_chatters,
            banned_chatters, deleted_chats)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    [
        (
            r["channelId"],
            r["period"],
            int(r["chats"]),
            int(r["memberChats"]),
            int(r["uniqueChatters"]),
            int(r["bannedChatters"]),
            int(r["deletedChats"]),
        )
        for r in chats
        if c.execute(
            "SELECT 1 FROM vtubers WHERE channel_id=?", (r["channelId"],)
        ).fetchone()
    ],
)

scs = load("chatStats/superchat_stats.csv")
# only insert rows where the channel exists in vtubers for continuity 
c.executemany(
    """
    INSERT OR REPLACE INTO superchats
        (channel_id, period, super_chats, unique_super_chatters,
            total_sc, average_sc, total_message_length, average_message_length,
            most_frequent_currency, most_frequent_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    [
        (
            r["channelId"],
            r["period"],
            int(r["superChats"]),
            int(r["uniqueSuperChatters"]),
            int(float(r["totalSC"])),
            int(float(r["averageSC"])),
            int(r["totalMessageLength"]),
            int(float(r["averageMessageLength"])),
            r["mostFrequentCurrency"],
            r["mostFrequentColor"],
        )
        for r in scs
        if c.execute(
            "SELECT 1 FROM vtubers WHERE channel_id=?", (r["channelId"],)
        ).fetchone()
    ],
)

db.commit()
db.close()

