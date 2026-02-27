import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure API Keys (Set these in Render Dashboard -> Environment)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_intelligence_report(report_type):
    # Context for 2026 
    base_context = "Current Date: February 2026. User Profile: IQ 148, CS/Neuro/Psych student at ASU."
    
    prompts = {
        "morning": f"{base_context} Analyze 2026 political landscape: Trump removal likelihood/timeline. Provide LA weather at 5 AM. Focus on hard data and probability.",
        "neuro": f"{base_context} Summarize one high-impact paper on dopamine-mediated bonding or BPD/ASPD neurological markers published in late 2025/2026.",
        "tech": f"{base_context} Identify 3 critical shifts in AI systems architecture or low-level Python optimizations relevant to CS students today.",
        "random": "Provide 5 distinct global 'alpha' data points: Markets, Geopolitics, and high-performance cognitive hacks."
    }
    
    prompt = prompts.get(report_type, prompts["random"])
    response = model.generate_content(prompt)
    return response.text

def send_to_discord(content):
    payload = {"content": f"**[System Update]**\n{content}"}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

@app.route('/trigger')
def trigger():
    # Usage: https://your-app.onrender.com/trigger?type=morning
    report_type = request.args.get('type', 'random')
    report_content = get_report(report_type)
    send_to_discord(report_content)
    return jsonify({"status": "success", "type": report_type})

@app.route('/')
def home():
    return "Worker Active."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))