import os
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

# Load .env file automatically (so you don’t need to set env vars manually each time)
load_dotenv()

# IMPORTANT: KEEP THIS COMMENT
# Follow these instructions when using this blueprint:
# - Note that the newest Gemini model series is "gemini-2.5-flash" or gemini-2.5-pro"
#   - do not change this unless explicitly requested by the user
# - Sometimes the google genai SDK has occasional type errors. You might need to run to validate, at time.  
# The SDK was recently renamed from google-generativeai to google-genai. This file reflects the new name and the new APIs.

# This API key is from Gemini Developer API Key, not Vertex AI API Key
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Missing GEMINI_API_KEY. Please add it to your .env file or environment variables.")

client = genai.Client(api_key=api_key)

def get_pet_advice(question: str) -> str:
    """
    Get pet care advice from Gemini AI.
    This function is specifically designed for pet care questions and guidance.
    """
    try:
        system_prompt = (
            "You are a knowledgeable pet care assistant. Your role is to provide helpful, "
            "accurate advice about pet care, health, nutrition, behavior, and general pet ownership. "
            "You should be warm, friendly, and informative. Always emphasize that for serious "
            "health concerns, the pet owner should consult with a veterinarian. "
            "Keep responses concise but informative. Focus only on pet-related topics."
        )

        full_prompt = f"{system_prompt}\n\nPet owner question: {question}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=500,
            )
        )

        return response.text.strip() if response.text else (
            "I'm sorry, I couldn't generate a response right now. Please try rephrasing your question."
        )

    except Exception as e:
        print(f"⚠️ Error in get_pet_advice: {e}")
        return "I'm currently experiencing technical difficulties. Please try again later or consult with a veterinarian for urgent pet care questions."
