import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "links.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            click_count INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def create_link(original_url: str, short_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO links (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code)
    )
    conn.commit()
    conn.close()


def get_link_by_code(short_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM links WHERE short_code = ?",
        (short_code,)
    )
    row = cur.fetchone()
    conn.close()
    return row


def increment_click(short_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE links SET click_count = click_count + 1 WHERE short_code = ?",
        (short_code,)
    )
    conn.commit()
    conn.close()


def get_all_links():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT original_url, short_code, click_count, created_at
        FROM links
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows