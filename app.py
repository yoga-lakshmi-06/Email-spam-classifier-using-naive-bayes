from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
import pickle
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
from auth import register_user, authenticate_user, get_user_by_username
from pathlib import Path

BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
EXPORT_FOLDER = BASE_DIR / "exports"
DATABASE = BASE_DIR / "database.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"  # change this in production
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

# load model + vectorizer
with open(BASE_DIR / "spam_model.pkl", "rb") as f:
    model = pickle.load(f)

with open(BASE_DIR / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ensure db tables
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        created_at TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email_text TEXT,
        prediction TEXT,
        score REAL,
        created_at TEXT,
        filename TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Please fill in both fields.", "danger")
            return redirect(url_for("register"))
        ok, msg = register_user(username, password)
        if ok:
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash(msg, "danger")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = authenticate_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Logged in successfully.", "success")
            nxt = request.args.get("next") or url_for("dashboard")
            return redirect(nxt)
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    result = None
    score = None
    email_text = ""
    filename = None

    if request.method == "POST":
        # either a textarea or an uploaded file
        email_text = request.form.get("email_text", "").strip()

        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            fname = secure_filename(uploaded.filename)
            save_path = UPLOAD_FOLDER / fname
            uploaded.save(save_path)
            filename = fname
            # try to read text from .txt
            if fname.lower().endswith(".txt"):
                with open(save_path, "r", encoding="utf-8", errors="ignore") as fh:
                    email_text = fh.read()
            # .docx basic support (optional)
            elif fname.lower().endswith(".docx"):
                try:
                    import docx
                    doc = docx.Document(save_path)
                    email_text = "\n".join(p.text for p in doc.paragraphs)
                except Exception:
                    # fallback
                    email_text = ""
        if not email_text:
            flash("No email content provided.", "warning")
            return redirect(url_for("dashboard"))

        # vectorize + predict probability
        X = vectorizer.transform([email_text])
        probs = model.predict_proba(X)[0]
        # assume classes: [ham, spam] or similar. We'll attempt to find spam index.
        classes = getattr(model, "classes_", None)
        spam_index = None
        if classes is not None:
            # try to map label "spam" (case-insensitive) or label 1
            for i, cls in enumerate(classes):
                if str(cls).lower() in ("spam", "1", "true", "yes"):
                    spam_index = i
                    break
        if spam_index is None:
            # fallback: assume second column is spam if binary
            spam_index = 1 if probs.shape[0] >= 2 else 0

        spam_prob = float(probs[spam_index]) * 100.0
        score = round(spam_prob, 2)
        result = "Spam" if spam_prob >= 50 else "Ham"

        # store log
        conn = get_db_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO logs (user_id, email_text, prediction, score, created_at, filename) VALUES (?, ?, ?, ?, ?, ?)",
            (session["user_id"], email_text[:2000], result, score, datetime.utcnow().isoformat(), filename)
        )
        conn.commit()
        conn.close()

    return render_template("dashboard.html", result=result, score=score, email_text=email_text)

@app.route("/logs")
@login_required
def logs():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT logs.*, users.username FROM logs LEFT JOIN users ON logs.user_id = users.id WHERE users.id = ? ORDER BY logs.created_at DESC", (session["user_id"],))
    rows = c.fetchall()
    conn.close()
    return render_template("logs.html", logs=rows)

@app.route("/download/<filename>")
@login_required
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
