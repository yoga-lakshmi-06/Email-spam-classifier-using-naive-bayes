import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / "database.db"

def get_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def register_user(username: str, password: str):
    username = username.strip()
    if not username or not password:
        return False, "Username and password required."
    conn = get_conn()
    c = conn.cursor()
    try:
        pw_hash = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)", (username, pw_hash, datetime.utcnow().isoformat()))
        conn.commit()
        return True, "Registered."
    except Exception as e:
        return False, "Username already exists."
    finally:
        conn.close()

def authenticate_user(username: str, password: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    if check_password_hash(row["password_hash"], password):
        return dict(row)
    return None

def get_user_by_username(username: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
