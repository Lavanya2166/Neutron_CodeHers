from fastapi import APIRouter, UploadFile, File
import pandas as pd
from backend.model_utils import predict_product
from backend.model_utils import train_model_from_csv
import tempfile

router = APIRouter()

@router.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    if df.empty:
        return {"error": "Uploaded file is empty or invalid."}

    try:
        result = predict_product(df)
        return result
    except Exception as e:
        return {"error": str(e)}

@router.post("/train")
async def train_model_route(file: UploadFile = File(...)):
    try:
        # Save uploaded CSV to a temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        temp_file.write(await file.read())
        temp_file.close()

        # Train model using that file
        columns, accuracy = train_model_from_csv(temp_file.name)
        return {
            "message": "Model trained successfully",
            "accuracy": accuracy,
            "features": columns
        }

    except Exception as e:
        return {"error": str(e)}
