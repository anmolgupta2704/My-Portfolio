import os
import json
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, jsonify

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import anthropic

load_dotenv()

app = Flask(__name__)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

PORTFOLIO_CONTEXT = """
You are a helpful assistant for Anmol Gupta's developer portfolio website.
Anmol is a B.Tech Computer Science student specializing in Cybersecurity from Kanpur, Uttar Pradesh.

Key facts about Anmol:
- Skills: DSA (90%), Python (85%), Django (80%), SQL (75%), Web Development (70%), Cybersecurity & Ethical Hacking (60%)
- Projects: Resume Detection System (GitHub: anmolgupta2704/PROJECT-RESUME-DETECTION), Tomato Leaf AI (deep learning disease detection), Face Recognition Application (AI-based)
- Certifications: Python (HackerRank), Problem Solving (HackerRank), SQL/DBMS (HackerRank), Google Cloud Hack2Skill Agentic Day Hackathon, Coursera Python Data Structures, HTML5
- Contact: anmolgupta2704@gmail.com | +91 790XXXXXXX | Kanpur, UP
- LinkedIn: linkedin.com/in/anmol-gupta-714933308
- GitHub: github.com/anmolgupta2704
- LeetCode: leetcode.com/u/2301641720021_A/
- Open for: SDE roles, Software Engineering internships, Backend Development, Python/Django roles
- Interests: Cybersecurity, ethical hacking, competitive programming, open source

Be friendly, concise, and helpful. Answer questions about Anmol's portfolio, skills, projects, and experience.
If asked about hiring, express that Anmol is actively looking for opportunities.
Keep responses under 3-4 sentences unless more detail is requested.
"""

def send_email(name, email, message):
    if not BREVO_API_KEY or not MAIL_USERNAME or not MAIL_RECEIVER:
        raise ValueError("Missing required environment variables.")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email_content = sib_api_v3_sdk.SendSmtpEmail(
        sender={"name": "Portfolio Contact", "email": MAIL_USERNAME},
        to=[{"email": MAIL_RECEIVER}],
        reply_to={"email": email, "name": name},
        subject=f"📩 New message from {name}",
        html_content=f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f9f9f9;padding:20px;border-radius:10px;">
          <h2 style="color:#5b8cff;">New Portfolio Contact</h2>
          <table style="width:100%;background:#fff;padding:20px;border-radius:8px;border:1px solid #eee;">
            <tr><td style="padding:8px;color:#666;width:100px;"><b>Name</b></td><td style="padding:8px;">{name}</td></tr>
            <tr><td style="padding:8px;color:#666;"><b>Email</b></td><td style="padding:8px;"><a href="mailto:{email}">{email}</a></td></tr>
            <tr><td style="padding:8px;color:#666;vertical-align:top;"><b>Message</b></td><td style="padding:8px;">{message}</td></tr>
          </table>
          <p style="color:#999;font-size:12px;margin-top:16px;">Sent via Anmol Gupta's Portfolio</p>
        </div>
        """
    )
    try:
        api_instance.send_transac_email(email_content)
    except ApiException as e:
        print("Brevo error:", e)
        raise


def ai_chatbot_reply(msg, history=None):
    """Use Claude AI for intelligent responses about the portfolio."""
    if not ANTHROPIC_API_KEY:
        return fallback_chatbot_reply(msg)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        messages = []
        if history:
            for h in history[-6:]:  # last 3 exchanges
                messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": msg})

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=PORTFOLIO_CONTEXT,
            messages=messages
        )
        return response.content[0].text
    except Exception as e:
        print("AI chatbot error:", e)
        return fallback_chatbot_reply(msg)


def fallback_chatbot_reply(msg):
    msg = msg.lower()
    if any(w in msg for w in ["hello", "hi", "hey", "namaste"]):
        return "👋 Hello! I'm Anmol's portfolio assistant. Ask me about his skills, projects, or how to hire him!"
    elif "resume" in msg or "cv" in msg:
        return "📄 You can download Anmol's resume from the 'See My Resume' button on the homepage."
    elif "skill" in msg:
        return "💻 Anmol's top skills: DSA (90%), Python (85%), Django (80%), SQL (75%), Web Dev (70%), and Cybersecurity (60%)."
    elif "project" in msg:
        return "🚀 Anmol has built: Resume Detection System, Tomato Leaf AI (deep learning), and a Face Recognition App. Check the Projects section!"
    elif any(w in msg for w in ["contact", "email", "reach"]):
        return "📩 Email: anmolgupta2704@gmail.com | Use the contact form below to send a message directly!"
    elif any(w in msg for w in ["hire", "job", "internship", "opportunity"]):
        return "🤝 Anmol is actively looking for SDE roles and Python/Django opportunities. Use the contact form or email directly!"
    elif "college" in msg or "education" in msg or "study" in msg:
        return "🎓 Anmol is pursuing B.Tech in Computer Science with a specialization in Cybersecurity from Kanpur, UP."
    elif "github" in msg:
        return "🐙 GitHub: github.com/anmolgupta2704 — check out his repositories!"
    elif "linkedin" in msg:
        return "💼 LinkedIn: linkedin.com/in/anmol-gupta-714933308"
    elif "certif" in msg:
        return "🏆 Certifications: HackerRank Python, Problem Solving, SQL; Google Cloud Hackathon; Coursera Python Data Structures; HTML5."
    else:
        return "🤔 I can tell you about Anmol's skills, projects, certifications, or how to contact/hire him. What would you like to know?"


@app.route("/")
def home():
    status = request.args.get("status")
    return render_template("index.html", status=status)


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return redirect(url_for("home", status="error"))

    try:
        send_email(name, email, message)
        return redirect(url_for("home", status="success"))
    except Exception as e:
        print("Contact error:", e)
        return redirect(url_for("home", status="error"))


@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    reply = ai_chatbot_reply(user_msg, history)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)