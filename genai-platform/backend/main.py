# backend/main.py

from fastapi import FastAPI, File, UploadFile, Form
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from backend.ml.image_caption_gen import VibeClassifier, GeminiCaptionGenerator  # Import your ML classes
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, genai_tools, chat, themes, voice, personal_brand
from backend.routes import themes
from backend.routes import summarizer
from backend.routes import product_success_text_route
from backend.routes import product_routes 
from backend.routes import prediction, update_model
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = FastAPI(title="GenAI-as-a-Service Platform")
app.include_router(themes.router, prefix="/themes")
# CORS config (adjust domains as needed)
origins = ["http://localhost:3000", "http://127.0.0.1:8000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(auth.router, prefix="/auth")
# app.include_router(genai_tools.router, prefix="/tools")
# app.include_router(chat.router, prefix="/chat")
# app.include_router(themes.router, prefix="/themes")
# app.include_router(voice.router, prefix="/voice")
# app.include_router(personal_brand.router, prefix="/brand")
# app.include_router(chat.router)
app.include_router(genai_tools.router, prefix="/genai-tools")
# app.include_router(genai_tools.router, prefix="/genai-tools")
app.include_router(summarizer.router, prefix="/genai-tools")  # Summarizer tools
app.include_router(product_success_text_route.router, prefix="/genai-tools")  # Text predict
# app.include_router(product_routes.router, prefix="/product")
app.include_router(prediction.router, prefix="/product")
app.include_router(update_model.router, prefix="/product")
@app.get("/")
def root():
    return {"message": "Welcome to GenAI platform 🚀"}

@app.post("/genai-tools/genai-tools/image-caption")
async def generate_caption(
    file: UploadFile = File(...),  # File parameter for image
    theme: str = Form(...),        # Theme parameter from the form
    tone: str = Form(...)          # Tone parameter from the form
):
    try:
        # Read the image data from the uploaded file
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))  # Open the image using PIL

        # Get the vibe and object classification for the image
        vibe, vibe_confidence = vibe_classifier.classify(image, mode="vibe")
        obj, obj_confidence = vibe_classifier.classify(image, mode="object")

        # Generate the caption using the vibe, object, theme, and tone
        caption = caption_generator.generate_caption(vibe, obj, theme, tone)

        return {"caption": caption}  # Return the generated caption

    except Exception as e:
        return {"error": str(e)}  # Handle errors gracefully