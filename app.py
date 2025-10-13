from flask import Flask, request, render_template, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_email(name, email, message):
    """Send email via SendGrid API"""
    try:
        msg = Mail(
            from_email=MAIL_USERNAME,
            to_emails=MAIL_RECEIVER,
            subject="New Contact Form Submission",
            html_content=f"""
            <h3>You have a new message from your portfolio contact form:</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong> {message}</p>
            """
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(msg)
        print(f"Email sent, status code: {response.status_code}")

    except Exception as e:
        print(f"Error sending email: {e}")
        raise e

@app.route("/")
def home():
    status = request.args.get("status")
    return render_template("index.html", status=status)

@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            return redirect(url_for("home", status="error"))

        send_email(name, email, message)
        return redirect(url_for("home", status="success"))

    except Exception as e:
        return redirect(url_for("home", status="error"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
