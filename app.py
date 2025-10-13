from flask import Flask, request, render_template, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Your Gmail/SMTP email
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # App password for Gmail
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")  # Where you want to receive messages

def send_email(name, email, message):
    """Send email using SMTP"""
    try:
        if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_RECEIVER:
            raise ValueError("Environment variables not set correctly!")

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = MAIL_USERNAME
        msg['To'] = MAIL_RECEIVER
        msg['Subject'] = "New Contact Form Submission"
        body = f"""
        <h3>You have a new message from your portfolio contact form:</h3>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong> {message}</p>
        """
        msg.attach(MIMEText(body, 'html'))

        # Connect to SMTP server and send
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, MAIL_RECEIVER, msg.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
        raise e

@app.route("/")
def home():
    status = request.args.get("status")
    return render_template("index.html", status=status)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        return redirect(url_for("home", status="error"))

    try:
        send_email(name, email, message)
        return redirect(url_for("home", status="success"))
    except Exception:
        return redirect(url_for("home", status="error"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
