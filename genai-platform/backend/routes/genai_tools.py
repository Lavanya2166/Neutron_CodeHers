# backend/routes/genai_tools.py

from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
import os
from dotenv import load_dotenv
from backend.ml.image_caption_gen import VibeClassifier, GeminiCaptionGenerator
from fastapi import Depends
from backend.database import get_database
router = APIRouter(prefix="/genai-tools", tags=["GenAI Tools"])

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

vibe_classifier = VibeClassifier()
caption_generator = GeminiCaptionGenerator(api_key)

async def get_current_user():
    return {"_id": "demo_user"}

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

# @router.get("/saved-captions")
# async def get_user_captions(user: dict = Depends(get_current_user), db=Depends(get_database)):
#     try:
#         user_id = user["user_id"]
#         captions = await db["captions"].find({"user_id": user_id}).to_list(length=100)
#         return {"captions": captions}
#     except Exception as e:
#         print(f"Error fetching captions: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
