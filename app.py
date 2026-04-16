import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()
app = Flask(__name__)

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")

PORTFOLIO_CONTEXT = """
You are a helpful assistant for Anmol Gupta's developer portfolio website.
Anmol is a B.Tech Computer Science student specializing in Cybersecurity from Kanpur, Uttar Pradesh.
Skills: DSA (90%), Python (85%), Django (80%), SQL (75%), Web Dev (70%), Cybersecurity (60%).
Projects: Resume Detection System, Tomato Leaf AI (CNN/TF), Face Recognition App (OpenCV).
GitHub: github.com/anmolgupta2704 | LinkedIn: linkedin.com/in/anmol-gupta-714933308
Email: anmolgupta2704@gmail.com | Open for: SDE roles, internships, Python/Django, Cybersecurity.
Be friendly and concise. Max 3-4 sentences.
"""

def ai_chatbot_reply(msg, history=None):
    if ANTHROPIC_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
            messages = []
            if history:
                for h in history[-6:]:
                    if h.get("role") in ("user","assistant") and h.get("content"):
                        messages.append({"role":h["role"],"content":h["content"]})
            messages.append({"role":"user","content":msg})
            resp = client.messages.create(model="claude-haiku-4-5-20251001",max_tokens=300,system=PORTFOLIO_CONTEXT,messages=messages)
            return resp.content[0].text
        except Exception as e:
            print(f"[Claude] {e}")
    return _kw(msg)

def _kw(msg):
    m=msg.lower()
    if any(w in m for w in ["hello","hi","hey","namaste"]): return "👋 Hello! I'm Anmol's assistant. Ask about skills, projects, or hiring!"
    if any(w in m for w in ["resume","cv"]): return "📄 Click 'Resume' at the top to download Anmol's resume."
    if any(w in m for w in ["skill","tech","stack"]): return "💻 DSA (90%) · Python (85%) · Django (80%) · SQL (75%) · Cybersecurity (60%)"
    if "project" in m: return "🚀 Resume Detection System, Tomato Leaf AI (CNN), Face Recognition App."
    if any(w in m for w in ["hire","job","intern","work"]): return "🤝 Anmol is actively looking for SDE/Python/Cybersecurity roles!"
    if any(w in m for w in ["contact","email","reach"]): return "📩 anmolgupta2704@gmail.com — or use the Contact form!"
    if "github" in m: return "🐙 github.com/anmolgupta2704"
    if "linkedin" in m: return "💼 linkedin.com/in/anmol-gupta-714933308"
    if "leetcode" in m: return "⚡ leetcode.com/u/2301641720021_A/"
    if any(w in m for w in ["cert","hackerrank","coursera"]): return "🏆 HackerRank (Python, PS, SQL) · Coursera · Google Cloud Hackathon · HTML5"
    if any(w in m for w in ["security","hack","cyber","ctf"]): return "🛡️ Anmol studies Cybersecurity & Ethical Hacking — CTF challenges, network security, vulnerability analysis."
    return "🤔 Ask about skills, projects, certs, or how to hire Anmol!"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json(silent=True) or {}
    msg = data.get("message","").strip()
    hist = data.get("history",[])
    if not msg: return jsonify({"reply":"Please type a message."})
    return jsonify({"reply": ai_chatbot_reply(msg, hist)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)