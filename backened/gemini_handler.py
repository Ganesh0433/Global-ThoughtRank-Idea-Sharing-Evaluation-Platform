import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
def evaluate_with_gemini(text):
    prompt = f"""
    Analyze this idea for originality (1-10), creativity (1-10), and critical thinking (1-10).
    Respond STRICTLY in JSON format ONLY (no Markdown backticks, no extra text).
    Required format:
    {{
        "originality": score,
        "creativity": score,
        "critical_thinking": score,
        "feedback": "Your feedback here..."
    }}
    Idea: "{text}"
    """
    response = model.generate_content(prompt)
    
    # Remove Markdown backticks if present
    cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
    
    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print("Failed to parse:", cleaned_response)  # Debug
        return {"error": f"Invalid JSON: {str(e)}"}