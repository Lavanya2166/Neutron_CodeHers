# backend/ml/product_success_text.py

import os
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Corrected __file__ variable
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/text_success_model.pkl")

def train_text_model(csv_path):
    df = pd.read_csv(csv_path)

    if len(df) < 20:
        raise ValueError("At least 20 items required to train the model.")

    X = df['description']
    y = df['success']

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ])

    pipeline.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    return "Model trained successfully."

def predict_text_success(description):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained yet.")

    model = joblib.load(MODEL_PATH)
    prediction = model.predict([description])[0]
    confidence = model.predict_proba([description])[0].max()

    return bool(prediction), round(confidence, 2)
