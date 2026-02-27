import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure API Keys (Set these in Render Dashboard -> Environment)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_report(report_type):
    # Prompt logic changes based on the request type
    prompts = {
        "morning": "Daily Report Feb 2026: 1. Likelihood of Trump being removed from office & timeline. 2. Weather in Hollister, CA and Bastrop, TX at 5am. 3. Top headline.",
        "neuro": "Provide 3 recent breakthroughs in Neuroscience or Psychology (specifically BPD/ASPD research) from 2025-2026.",
        "tech": "Give me 5 critical updates in Computer Science and AI for today.",
        "random": "Give me 5 interesting facts or world news events happening right now."
    }
    
    selected_prompt = prompts.get(report_type, prompts["random"])
    response = model.generate_content(selected_prompt)
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