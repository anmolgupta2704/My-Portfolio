from flask import Flask, request, render_template, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp-relay.brevo.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


def send_email(name, email, message):
    if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_RECEIVER:
        raise ValueError("Missing required environment variables.")

    msg = MIMEMultipart()
    msg['From'] = MAIL_USERNAME
    msg['To'] = MAIL_RECEIVER
    msg['Subject'] = "📩 New Contact Form Submission"

    body = f"""
    <h3>New Contact Message</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong><br>{message}</p>
    """
    msg.attach(MIMEText(body, 'html'))

    # Send using Brevo SMTP (Safe for Render)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, MAIL_RECEIVER, msg.as_string())


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
    except Exception as e:
        print("Error:", e)
        return redirect(url_for("home", status="error"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
