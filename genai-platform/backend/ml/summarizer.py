import os
import fitz  # PyMuPDF for PDF
from docx import Document  # python-docx for Word
import google.generativeai as genai
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from pathlib import Path

# Correct path to .env file in the 'neutron_codehers' directory
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

# Step 2: Load CLIP for object classification
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def classify_object(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = clip_processor(
        text=["a photo", "document", "presentation", "screenshot"],
        images=image,
        return_tensors="pt",
        padding=True
    )
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    labels = ["a photo", "document", "presentation", "screenshot"]
    return labels[probs.argmax()]

def generate_summary(text, word_limit, vibe, tone, theme, obj_class):
    prompt = f"""
Summarize the following content into approximately {word_limit} words.
The summary should have a {vibe} vibe, a {tone} tone, and reflect the theme of {theme}.
The content type is classified as: {obj_class}.

Content:
{text}
"""
    response = model.generate_content(prompt)
    return response.text

def main():
    print(" Welcome to the Smart Summarizer\n")
    file_type = input("Enter file type (pdf/docx/text): ").strip().lower()

    if file_type == "pdf":
        file_path = input("Enter PDF file path (absolute or relative): ").strip().strip('"')
        text = extract_text_from_pdf(file_path)
    elif file_type == "docx":
        file_path = input("Enter DOCX file path (absolute or relative): ").strip().strip('"')
        text = extract_text_from_docx(file_path)
    elif file_type == "text":
        print("Enter your text (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)
    else:
        print(" Unsupported file type")
        return

    word_limit = input("Enter desired word count for the summary: ").strip()
    try:
        word_limit = int(word_limit)
    except ValueError:
        print(" Please enter a valid number.")
        return

    # Hardcoded for now
    vibe = "professional"
    tone = "informative"
    theme = "education"

    # Optional image for classification
    image_path = input("Enter image path for object classification (or press Enter to skip): ").strip().strip('"')
    if image_path:
        obj_class = classify_object(image_path)
        print(f" Object classified as: {obj_class}")
    else:
        obj_class = "text document"

    print(" Generating summary, please wait...")
    summary = generate_summary(text, word_limit, vibe, tone, theme, obj_class)
    print(" Summary:\n")
    print(summary)

#  Corrected main trigger
if __name__ == "__main__":
    main()
