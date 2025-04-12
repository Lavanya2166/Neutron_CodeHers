import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

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

    def classify(self, image, mode="vibe"):
        image = Image.open(image).convert("RGB")
        prompts = self.vibes if mode == "vibe" else self.objects

        inputs = self.processor(text=prompts, images=image, return_tensors="pt", padding=True).to(self.device)
        outputs = self.model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)

        top_idx = probs.argmax().item()
        label = prompts[top_idx].replace("a ", "").strip().capitalize()

        return label, probs[0][top_idx].item()
