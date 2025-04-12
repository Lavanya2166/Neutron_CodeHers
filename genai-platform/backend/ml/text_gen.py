import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()  # <- Use ".env" (not "try.env") if that's the correct file

# ✅ Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(" GEMINI_API_KEY not found in .env")
    exit()
else:
    print(" GEMINI API Key loaded successfully")

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


# --- Gemini Caption Generator ---
# --- Gemini Caption Generator ---
class GeminiCaptionGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")  # ✅ Correct model name

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
            print(f" Error generating caption: {e}")
            return "Error generating caption."



# --- Main Execution ---
if __name__ == "__main__":
    image_path = "C:\\Users\\garga\\OneDrive\\Desktop\\cc.jpg"  # 🔁 Update with your actual image path

    if not os.path.exists(image_path):
        print(f" Image not found at {image_path}")
    else:
        classifier = VibeClassifier()
        caption_gen = GeminiCaptionGenerator(api_key)

        # Run classification
        vibe, vibe_conf = classifier.classify(image_path, mode="vibe")
        obj, obj_conf = classifier.classify(image_path, mode="object")

        # Customize theme and tone
        theme = "Minimalist"
        tone = "Friendly"

        # Generate caption
        caption = caption_gen.generate_caption(vibe, obj, theme, tone)

        # Output
        print(f" Object: {obj} ({obj_conf:.2f})")
        print(f" Vibe: {vibe} ({vibe_conf:.2f})")
        print(f"Theme: {theme}")
        print(f" Tone: {tone}")
        print(f" Instagram Caption:\n{caption}")