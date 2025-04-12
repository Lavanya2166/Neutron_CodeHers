import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

import os
from dotenv import load_dotenv
from pathlib import Path

# Correct path to .env file in the 'neutron_codehers/genai-platform' directory
env_path = Path(__file__).resolve().parents[2] / ".env"  # Goes up 2 levels to reach 'genai-platform'
load_dotenv(dotenv_path=env_path)

# Verify that the GOOGLE_API_KEY is loaded correctly
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
else:
    print("GOOGLE_API_KEY Key loaded")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")


# --- Vibe Classifier ---

class VibeClassifier:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        self.vibes = [
            "a calm photo", "a vibrant picture", "a vintage image", "a moody photo",
            "a dreamy scene", "an aesthetic vibe", "a minimalistic image", "a grungy look"
        ]
        self.objects = [
            "a cup of cold coffee", "a girl", "a boy", "a dog", "a cat", "a car", "a building",
            "a sunset", "a mountain", "a flower", "a cityscape", "a painting", "a fashion model"
        ]

    def classify(self, image_path, mode="vibe"):
        image = Image.open(image_path).convert("RGB")
        prompts = self.vibes if mode == "vibe" else self.objects

        inputs = self.processor(text=prompts, images=image, return_tensors="pt", padding=True).to(self.device)
        outputs = self.model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)

        top_idx = probs.argmax().item()
        label = prompts[top_idx].replace("a ", "").strip().capitalize()

        return label, probs[0][top_idx].item()

# --- Gemini Blog Generator ---
class GeminiCaptionGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    def generate_blog(self, vibe, obj, theme, tone, word_count=150):
        prompt = (
            f"You are a social media content creator. Based on an image that gives off a {vibe.lower()} vibe and "
            f"features {obj.lower()}, write a blog-style paragraph (around {word_count} words). "
            f"The theme is {theme.lower()} and the tone should feel {tone.lower()}. "
            f"Make the writing feel natural and human—avoid robotic phrasing. Use vivid descriptions, sensory details, and a conversational style. "
            f"Include subtle emotions, personal reflections, or observations. Avoid hashtags, emojis, or bullet points. This should feel like a slice of real life."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f" Error generating blog text: {e}")
            return "Error generating blog post."

# --- Main Execution ---
if __name__ == "__main__":
    image_path = "C:\\Users\\garga\\OneDrive\\Desktop\\cc.jpg"  # Update this path as needed

    if not os.path.exists(image_path):
        print(f" Image not found at {image_path}")
    else:
        classifier = VibeClassifier()
        caption_gen = GeminiCaptionGenerator(api_key)

        # Run classification
        vibe, vibe_conf = classifier.classify(image_path, mode="vibe")
        obj, obj_conf = classifier.classify(image_path, mode="object")

        # Set default theme and tone
        theme = "Mindfulness"
        tone = "Poetic"

        # Get user input for word count
        try:
            word_count = int(input("How many words would you like for the blog post? "))
        except ValueError:
            print("Invalid input. Using default word count of 150.")
            word_count = 600

        # Generate blog post
        blog_post = caption_gen.generate_blog(vibe, obj, theme, tone, word_count)

        # Output
        print(" Image Classification Results:")
        print(f" Object: {obj} ({obj_conf:.2f})")
        print(f" Theme: {theme}")
        print(f" Tone: {tone}")
        print(f" Blog Post ({word_count} words):\n")
        print(blog_post)
