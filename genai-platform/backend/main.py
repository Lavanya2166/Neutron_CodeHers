# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, genai_tools, chat, themes, voice, personal_brand
from backend.routes import themes
import os
from dotenv import load_dotenv
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
app.include_router(genai_tools.router)

@app.get("/")
def root():
    return {"message": "Welcome to GenAI platform 🚀"}
