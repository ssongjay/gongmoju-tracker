import sqlite3
import sys
import os


def _get_db_path():
    if getattr(sys, 'frozen', False):
        # 앱 번들일 때: 사용자 홈 폴더에 저장 (데이터 유지)
        data_dir = os.path.join(os.path.expanduser("~"), ".gongmoju-tracker")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, "gongmoju.db")
    return os.path.join(os.path.dirname(__file__), "gongmoju.db")


DB_PATH = _get_db_path()


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
