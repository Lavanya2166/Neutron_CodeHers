from fastapi import APIRouter, UploadFile, File
import pandas as pd
import os

from backend.model_utils import train_model_from_csv, DATA_PATH

router = APIRouter()

@router.post("/update_model")
async def update_model_route(file: UploadFile = File(...)):
    new_df = pd.read_csv(file.file)
    
    if "sales_success" not in new_df.columns:
        return {"error": "CSV must include the 'sales_success' column."}

    existing_df = pd.read_csv(DATA_PATH)
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    updated_df.to_csv(DATA_PATH, index=False)

    feature_cols, acc = train_model_from_csv(DATA_PATH)
    return {
        "message": "Model updated successfully.",
        "accuracy": acc,
        "features_used": feature_cols
    }
