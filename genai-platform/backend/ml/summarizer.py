import os
import fitz
from docx import Document
import google.generativeai as genai
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from dotenv import load_dotenv
from pathlib import Path
from io import BytesIO

# Load env vars
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# CLIP model setup (though we are removing image classification)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_text_from_pdf_file(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx_file(file_bytes):
    document = Document(BytesIO(file_bytes))  # Correcting the input to BytesIO
    return "\n".join([para.text for para in document.paragraphs])

# Removing image classification (not needed now)
def generate_summary(text, vibe, tone, theme, obj_class):
    prompt = f"""
Summarize the following content in a concise manner.
The summary should have a {vibe} vibe, a {tone} tone, and reflect the theme of {theme}.
The content type is classified as: {obj_class}.

Content:
{text}
"""
    response = model.generate_content(prompt)
    return response.text

# Updated function to handle file and text input correctly
async def process_and_summarize(text, file, vibe, tone, theme):
    final_text = ""
    
    if file:
        content = await file.read()
        if file.filename.endswith(".pdf"):
            final_text = extract_text_from_pdf_file(content)
        elif file.filename.endswith(".docx"):
            final_text = extract_text_from_docx_file(content)
        else:
            raise ValueError("Unsupported file type. Please upload PDF or DOCX.")
    else:
        final_text = text  # If no file is uploaded, use the text input

    obj_class = "text"  # We are not using image classification anymore

    # Generate summary based on the text content
    summary = generate_summary(final_text, vibe, tone, theme, obj_class)
    return summary
