# backend/routes/genai_tools.py

from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
import os
from dotenv import load_dotenv
from backend.ml.image_caption_gen import VibeClassifier, GeminiCaptionGenerator

router = APIRouter(prefix="/genai-tools", tags=["GenAI Tools"])

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

vibe_classifier = VibeClassifier()
caption_generator = GeminiCaptionGenerator(api_key)

@router.post("/image-caption")
async def generate_caption_route(
    file: UploadFile = File(...),
    theme: str = Form(...),
    tone: str = Form(...)
):
    try:
        image = Image.open(file.file).convert("RGB")

        vibe, _ = vibe_classifier.classify(image, mode="vibe")
        obj, _ = vibe_classifier.classify(image, mode="object")

        caption = caption_generator.generate_caption(vibe, obj, theme, tone)

        return {
            "object": obj,
            "vibe": vibe,
            "theme": theme,
            "tone": tone,
            "caption": caption
        }

    except Exception as e:
        return {"error": str(e)}
