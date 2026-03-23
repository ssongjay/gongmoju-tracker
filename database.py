import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "gongmoju.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ipo_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            stock_name TEXT NOT NULL,
            broker TEXT NOT NULL,
            ipo_price INTEGER NOT NULL,
            allocated INTEGER NOT NULL DEFAULT 0,
            allocated_qty INTEGER NOT NULL DEFAULT 0,
            sell_price INTEGER,
            sell_date TEXT,
            memo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)
    conn.commit()
    conn.close()
