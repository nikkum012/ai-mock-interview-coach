from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Optimized for fast, conversational AI apps
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_response(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print("FULL ERROR:", str(e))
        return f"ERROR: {str(e)}"