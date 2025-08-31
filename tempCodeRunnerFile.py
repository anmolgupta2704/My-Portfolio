from flask import Flask, request, render_template, redirect
import sqlite3
import os

app = Flask(__name__)

# Database ka path instance folder me
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "contact.db")

# Ensure instance folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Database setup (ek baar chalega)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Home route (portfolio ka index.html render hoga)
@app.route("/")
def home():
    return render_template("index.html")  # tumhara portfolio ka main page

# Contact Form submission
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Save into database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", 
                (name, email, message))
    conn.commit()
    conn.close()

    return redirect("/")  # submit hone ke baad wapas home page par bhej do

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
