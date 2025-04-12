# backend/routes/product_success_text_route.py

from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
from backend.ml.product_success_text import train_text_model, predict_text_success

router = APIRouter()
TEXT_DATA_DIR = "backend/ml/datasets/user_data_text"
os.makedirs(TEXT_DATA_DIR, exist_ok=True)

@router.post("/train-text-model")
def train_model_route(csv_file: UploadFile = File(...)):
    csv_path = os.path.join(TEXT_DATA_DIR, csv_file.filename)
    with open(csv_path, "wb") as f:
        shutil.copyfileobj(csv_file.file, f)

    try:
        message = train_text_model(csv_path)
        return {"message": message}
    except Exception as e:
        return {"error": str(e)}

@router.post("/predict-text-success")
def predict_route(description: str = Form(...)):
    try:
        result, confidence = predict_text_success(description)
        return {
            "success_prediction": result,
            "confidence": confidence
        }
    except Exception as e:
        return {"error": str(e)}