from flask import Flask, request, render_template, redirect, url_for
import os
from dotenv import load_dotenv

# Brevo API imports
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

app = Flask(__name__)

# ENV variables
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")     # Verified Sender in Brevo
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")     # Where messages come

def send_email(name, email, message):
    if not BREVO_API_KEY or not MAIL_USERNAME or not MAIL_RECEIVER:
        raise ValueError("Missing required environment variables.")

    # Configure Brevo API
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # Email content
    email_content = sib_api_v3_sdk.SendSmtpEmail(
        sender={"name": "Contact Form", "email": MAIL_USERNAME},
        to=[{"email": MAIL_RECEIVER}],
        subject="📩 New Contact Form Submission",
        html_content=f"""
        <h3>New Contact Message</h3>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong><br>{message}</p>
        """
    )

    # Send email
    try:
        api_instance.send_transac_email(email_content)
    except ApiException as e:
        print("Error sending email: ", e)
        raise


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
