import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "bot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            service TEXT NOT NULL,
            requirement TEXT NOT NULL,
            contact TEXT NOT NULL,
            telegram_user_id INTEGER,
            telegram_username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    add_lead_status_column()


def save_project_request(
    name,
    service,
    requirement,
    contact,
    telegram_user_id=None,
    telegram_username=None,
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO project_requests (
            name,
            service,
            requirement,
            contact,
            telegram_user_id,
            telegram_username
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            service,
            requirement,
            contact,
            telegram_user_id,
            telegram_username,
        )
    )

    connection.commit()

    request_id = cursor.lastrowid

    connection.close()

    return request_id


def add_lead_status_column():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            ALTER TABLE project_requests
            ADD COLUMN status TEXT DEFAULT 'New'
        """)
        connection.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass

    connection.close()