from flask import Flask, request, render_template, redirect
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# --------------------------
# Load env variables (Render dashboard me set karna hoga)
# --------------------------
MAIL_USERNAME = os.getenv("MAIL_USERNAME")   # your gmail
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")   # your 16-digit app password
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")   # jisme receive karna hai

# --------------------------
# Email sender function
# --------------------------
def send_email(name, email, message):
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

        # Gmail SMTP (SSL)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, MAIL_RECEIVER, msg.as_string())

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise e  # taaki Render logs me dikhe


# --------------------------
# Routes
# --------------------------
@app.route("/")
def home():
    return render_template("index.html")   

@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        send_email(name, email, message)
        return redirect("/")   
    except Exception as e:
        return f"Error: {e}", 500


# --------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
