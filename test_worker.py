import os
import requests
from google import genai

# 1. Grab credentials from your Render Environment Variables
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK")

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