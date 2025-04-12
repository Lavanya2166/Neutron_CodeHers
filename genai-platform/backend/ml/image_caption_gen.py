# backend/ml/image_caption_gen.py

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import google.generativeai as genai
import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)


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

    def classify(self, image: Image.Image, mode="vibe"):
        prompts = self.vibes if mode == "vibe" else self.objects
        inputs = self.processor(text=prompts, images=image, return_tensors="pt", padding=True).to(self.device)
        outputs = self.model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)

        top_idx = probs.argmax().item()
        label = prompts[top_idx].replace("a ", "").strip().capitalize()
        return label, probs[0][top_idx].item()


class GeminiCaptionGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

    def generate_caption(self, vibe, obj, theme, tone):
        prompt = (
            f"Generate a short, aesthetic Instagram caption for a photo that has a {vibe.lower()} vibe "
            f"and contains {obj.lower()}. The theme is {theme.lower()} and the tone is {tone.lower()}. "
            f"Make it inspiring, catchy, and suitable for social media, without emojis or special characters."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error generating caption: {e}")
            return "Error generating caption."
