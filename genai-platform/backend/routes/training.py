from fastapi import APIRouter, File, UploadFile
import pandas as pd
import tempfile
from backend.model_utils import train_model_from_csv

router = APIRouter()

@router.post("/train")
async def train_model_route(file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        contents = await file.read()
        temp_file.write(contents)
        temp_file.close()

        # Train the model
        columns, acc = train_model_from_csv(temp_file.name)
        return {"message": "Model trained successfully", "accuracy": acc, "features": columns}

    except Exception as e:
        return {"error": str(e)}
