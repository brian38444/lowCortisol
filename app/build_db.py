import sqlite3

DB_FILE = "oshi.db"

db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    );

    CREATE TABLE IF NOT EXISTS vtubers (
        channel_id TEXT PRIMARY KEY,
        channel_name TEXT,
        profile_image_url TEXT,
        channel_url TEXT,
        agency TEXT,
        total_subscriber_count INTEGER DEFAULT 0,
        total_videos INTEGER DEFAULT 0,
        total_views INTEGER DEFAULT 0,
        total_likes INTEGER DEFAULT 0,
        total_comments INTEGER DEFAULT 0,
        avg_views INTEGER DEFAULT 0,
        avg_likes INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS chats (
        channel_id TEXT REFERENCES vtubers(channel_id),
        period KEY,
        chats INTEGER DEFAULT 0,
        member_chats INTEGER DEFAULT 0,
        unique_chatters INTEGER DEFAULT 0,
        banned_chatters INTEGER DEFAULT 0,
        deleted_chats INTEGER DEFAULT 0,
        PRIMARY KEY (channel_id, period)
    );

    CREATE TABLE IF NOT EXISTS superchats (
        channel_id TEXT REFERENCES vtubers(channel_id),
        period KEY,
        super_chats INTEGER DEFAULT 0,
        unique_super_chatters INTEGER DEFAULT 0,
        total_sc INTEGER DEFAULT 0,
        average_sc INTEGER DEFAULT 0,
        total_message_length INTEGER DEFAULT 0,
        average_message_length INTEGER DEFAULT 0,
        most_frequent_currency TEXT,
        most_frequent_color TEXT,
        PRIMARY KEY (channel_id, period)
    );

    CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT REFERENCES vtubers(channel_id),
        username TEXT REFERENCES users(username),
        desc TEXT
    );
    """
)

db.commit()
db.close()