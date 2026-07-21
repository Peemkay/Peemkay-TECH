"""Minimal SQLite storage for contact-form submissions.

Uses the stdlib sqlite3 module only, so there is nothing extra to install
or configure on PythonAnywhere beyond a writable instance/ folder.
"""
import os
import sqlite3
from datetime import datetime, timezone


def get_connection(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    conn = get_connection(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                project_type TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_message(db_path, name, email, project_type, message):
    conn = get_connection(db_path)
    try:
        conn.execute(
            "INSERT INTO messages (name, email, project_type, message, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, email, project_type, message, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()
