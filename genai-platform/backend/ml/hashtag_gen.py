import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)

class GeminiHashtagGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    def generate_hashtags(self, vibe, obj, theme, tone):
        prompt = (
            f"Generate 10 relevant, aesthetic Instagram hashtags (without # symbols) for a photo that has a {vibe.lower()} vibe, "
            f"contains {obj.lower()}, and follows the theme of {theme.lower()} with a {tone.lower()} tone. "
            f"Make them trendy, specific, and without spaces or emojis."
        )
        try:
            response = self.model.generate_content(prompt)
            return [tag.strip().replace("#", "") for tag in response.text.strip().splitlines()]
        except Exception as e:
            print(f"Error generating hashtags: {e}")
            return ["error_generating_hashtags"]
