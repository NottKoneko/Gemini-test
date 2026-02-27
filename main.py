import os
import requests
from flask import Flask, request, jsonify
from google import genai  # Newer 2026 library

app = Flask(__name__)

# The client automatically looks for GEMINI_API_KEY in your Env Vars
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def get_intelligence(report_type):
    # Context optimized for your profile
    base_context = "Current Date: Feb 2026. Student: IQ 148, ASU, CS/Neuroscience."
    
    prompts = {
        "morning": f"{base_context} Analyze 2026 politics: Trump removal probability/timeline. LA weather at 5 AM.",
        "neuro": f"{base_context} Latest research on dopamine-storm bonding or ASPD/BPD neurology.",
        "tech": f"{base_context} 3 critical AI/CS updates for a senior-level student.",
        "random": "5 high-impact data points: Global markets and cognitive performance hacks."
    }
    
    prompt_text = prompts.get(report_type, prompts["random"])
    
    # Using the latest 3-Flash model
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt_text
    )
    return response.text

@app.route('/trigger')
def trigger():
    report_type = request.args.get('type', 'morning')
    content = get_intelligence(report_type)
    
    # Send to Discord
    requests.post(DISCORD_WEBHOOK_URL, json={"content": f"**[2026 Intelligence Report]**\n{content}"})
    return jsonify({"status": "delivered", "type": report_type})

@app.route('/')
def health():
    return "Worker is Online."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))