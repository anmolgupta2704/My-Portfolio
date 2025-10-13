from flask import Flask, request, render_template, redirect, url_for
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")  
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")  

app = Flask(__name__)

def send_email(name, email, message):
    """Send email via Gmail SMTP"""
    try:
        subject = "New Contact Form Submission"
        body = f"""
You have a new message from your portfolio contact form:

Name: {name}
Email: {email}
Message: {message}
        """

        msg = MIMEMultipart()
        msg["From"] = MAIL_USERNAME
        msg["To"] = MAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Gmail SMTP SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, MAIL_RECEIVER, msg.as_string())

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
