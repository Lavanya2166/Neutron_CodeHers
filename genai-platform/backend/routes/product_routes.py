from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from backend.ml.product_model import predict_success, update_data_and_retrain

router = APIRouter()

class ProductInput(BaseModel):
    target_age_group: str
    target_gender: str
    product_color: str
    price_range: str
    ad_effectiveness: float

class ProductEntry(ProductInput):
    sales_success: int

@router.post("/product/predict")
def predict_product_success(product: ProductInput):
    prediction = predict_success(product.dict())
    return {"prediction": "✅ Success" if prediction == 1 else "❌ Failure"}

@router.post("/product/update")
def update_product_data(entries: List[ProductEntry]):
    accuracy = update_data_and_retrain([e.dict() for e in entries])
    return {"message": "Data updated and model retrained.", "new_accuracy": round(accuracy, 2)}
