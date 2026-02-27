import os
import requests
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Config
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def send_to_discord(title, text):
    payload = {
        "embeds": [{
            "title": title,
            "description": text,
            "color": 5814783 # AI Blue
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def get_ai_report(task_type):
    # Context for 2026
    context = "Date: Feb 2026. User: CS/Neuro student, 148 IQ."
    
    prompts = {
        "morning": f"{context} Analysis: Trump removal odds/timeline + LA weather at 5am.",
        "neuro": f"{context} Research: 1 breakthrough in Dopamine/BPD/ASPD bonding from 2025-26.",
        "cs": f"{context} CS: 3 high-level updates in AI architecture or Python performance.",
        "psych": f"{context} Psych: A data-heavy fact on high-cognitive empathy vs low-affective empathy.",
        "market": f"{context} Markets: 2026 status of BTC and S&P 500."
    }
    
    prompt = prompts.get(task_type, "Provide a general 2026 intelligence update.")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

@app.route('/trigger')
def trigger():
    # This fires whenever a ping hits this URL
    task = request.args.get('type', 'morning')
    
    # 1. Immediate "System Online" message
    # (Optional: remove this if it's too spammy)
    # send_to_discord("System Alert", f"Worker initialized for task: {task}")

    # 2. Fetch the specific AI data
    report = get_ai_report(task)
    
    # 3. Send the final report
    send_to_discord(f"Intelligence Update: {task.upper()}", report)
    
    return jsonify({"status": "complete", "task": task})

@app.route('/')
def home():
    # Simple startup check
    return "Worker is awake."

if __name__ == "__main__":
    # Every time Render starts the app, it runs this.
    # We can send a "Startup" message here if desired.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def run_test():
    print("--- Starting Connection Test ---")
    
    # Validate Env Vars exist
    if not GEMINI_KEY or not DISCORD_URL:
        print("ERROR: Missing Environment Variables. Check Render Dashboard.")
        return

    try:
        # 2. Test Gemini Connection
        client = genai.Client(api_key=GEMINI_KEY)
        print("Connecting to Gemini...")
        ai_response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="State 'Gemini is Online' and give a 1-sentence 2026 political headline."
        )
        report = ai_response.text
        print(f"Gemini Response: {report}")

        # 3. Test Discord Connection
        print("Sending to Discord...")
        payload = {"content": f"**[Test Successful]**\n{report}"}
        db_res = requests.post(DISCORD_URL, json=payload)
        
        if db_res.status_code == 204:
            print("SUCCESS: Message delivered to Discord.")
        else:
            print(f"FAILED: Discord returned status {db_res.status_code}")

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    run_test()