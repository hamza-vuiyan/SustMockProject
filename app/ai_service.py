import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

# 1. Initialize the NEW Google GenAI client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment!")
    
client = genai.Client(api_key=api_key)

async def classify_ticket(message: str) -> dict:
    """
    Sends the customer message to Gemini and returns a parsed JSON dictionary.
    """
    prompt = f"""
    You are an automated triage assistant for a digital finance company.
    Read the following customer support message and classify it.
    
    You MUST respond with a RAW JSON object containing exactly these 4 keys:
    1. "case_type": Strictly choose one from [wrong_transfer, payment_failed, refund_request, phishing_or_social_engineering, other].
    2. "severity": Strictly choose one from [low, medium, high, critical].
    3. "agent_summary": A 1-2 sentence neutral summary of the issue. NEVER ask the customer to share a PIN, OTP, password, or card number.
    4. "confidence": A float between 0.0 and 1.0 representing your confidence.
    
    Customer Message: "{message}"
    """

    try:
        # 2. Use the new async client (.aio) and the 2.5-flash model
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        # 3. Parse the AI's string response into a Python dictionary
        if not response.text:
            raise ValueError("AI returned an empty response (possible safety block).")

        # 3. Parse the AI's string response into a Python dictionary
        ai_data = json.loads(response.text)
        
        # 4. The Ultimate Safety Filter
        forbidden_words = ["pin", "otp", "password", "card"]
        summary = ai_data.get("agent_summary", "").lower()
        
        if any(word in summary for word in forbidden_words):
             ai_data["agent_summary"] = "Customer reported an issue. (Automated summary redacted for containing sensitive keyword requests)."
             
        return ai_data

    except Exception as e:
        print(f"AI Service Error: {e}")
        return {}