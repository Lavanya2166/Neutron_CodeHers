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

# --- Gemini Hashtag Generator ---
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
            return response.text.strip().splitlines()
        except Exception as e:
            print(f" Error generating hashtags: {e}")
            return ["#error_generating_hashtags"]

# --- Main Execution ---
if __name__ == "__main__":
    image_path = "C:\\Users\\garga\\OneDrive\\Desktop\\cc.jpg"
    if not os.path.exists(image_path):
        print(f" Image not found at {image_path}")
    else:
        classifier = VibeClassifier()
        hashtag_gen = GeminiHashtagGenerator(api_key)

        vibe, vibe_conf = classifier.classify(image_path, mode="vibe")
        obj, obj_conf = classifier.classify(image_path, mode="object")

        theme = "Minimalist"
        tone = "Friendly"

        hashtags = hashtag_gen.generate_hashtags(vibe, obj, theme, tone)

        print("\n--- Image Classification ---")
        print(f" Vibe: {vibe} ({vibe_conf:.2f})")
        print(f" Object: {obj} ({obj_conf:.2f})")
        print(f" Theme: {theme}")
        print(f" Tone: {tone}")

        print("\n--- Suggested Hashtags ---\n")
        for tag in hashtags:
            print(f"#{tag.strip()}")