from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# Database setup (ek baar chalega)
def init_db():
    conn = sqlite3.connect("contact.db")
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
    conn = sqlite3.connect("contact.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", 
                (name, email, message))
    conn.commit()
    conn.close()

    return redirect("/")  # submit hone ke baad wapas home page par bhej do

if __name__ == "__main__":
    init_db()
    app.run(debug=True)     