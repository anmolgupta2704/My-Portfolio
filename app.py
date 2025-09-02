from flask import Flask, request, render_template, redirect
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Database setup (ek baar chalega)
def init_db():
    os.makedirs("instance", exist_ok=True)   # folder 
    conn = sqlite3.connect("instance/contact.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()


# Email bhejne ka function
def send_email(name, email, message):
    sender = "anmolgupta2704@gmail.com"       
    receiver = "anmolgupta2704@gmail.com"        
    password = "loil bvzv yros vozx"           

    subject = f"New Contact from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print(" Email sent successfully")
    except Exception as e:
        print(" Email error:", e)


# Home route 
@app.route("/")
def home():
    return render_template("index.html")  #  main page


# Contact Form submission
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Save into database
    conn = sqlite3.connect("instance/contact.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", 
                (name, email, message))
    conn.commit()
    conn.close()

    # Email bhejna
    send_email(name, email, message)

    return redirect("/")  # submit 


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
