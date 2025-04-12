# blog_generator.py

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

class GeminiBlogGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    def generate_blog(self, vibe, obj, theme, tone, word_count=150):
        prompt = (
            f"You are a social media content creator. Based on an image that gives off a {vibe.lower()} vibe and "
            f"features {obj.lower()}, write a blog-style paragraph (around {word_count} words). "
            f"The theme is {theme.lower()} and the tone should feel {tone.lower()}. "
            f"Make the writing feel natural and human—avoid robotic phrasing. Use vivid descriptions, sensory details, and a conversational style. "
            f"Include subtle emotions, personal reflections, or observations. Avoid hashtags, emojis, or bullet points."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating blog post: {e}"
