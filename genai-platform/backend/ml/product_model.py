import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATA_PATH = "data/product_prize.csv"
MODEL_PATH = "trained_model.pkl"

def load_data():
    return pd.read_csv(DATA_PATH)

def preprocess_data(df):
    X = pd.get_dummies(df.drop("sales_success", axis=1))
    y = df["sales_success"]
    return X, y

def train_and_save_model(df):
    X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    joblib.dump((model, X.columns.tolist()), MODEL_PATH)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return accuracy

def predict_success(new_data: dict):
    model, columns = joblib.load(MODEL_PATH)
    df = pd.DataFrame([new_data])
    df_encoded = pd.get_dummies(df)
    df_encoded = df_encoded.reindex(columns=columns, fill_value=0)
    prediction = model.predict(df_encoded)[0]
    return prediction

def update_data_and_retrain(new_entries: list):
    df_existing = load_data()
    df_new = pd.DataFrame(new_entries)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(DATA_PATH, index=False)
    accuracy = train_and_save_model(df_combined)
    return accuracy

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
from typing import List
from io import StringIO
from fastapi import UploadFile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../../trained_model.pkl")

def train_model_from_uploaded_csv(file: UploadFile):
    # Read uploaded file content into DataFrame
    content = file.file.read().decode('utf-8')
    df = pd.read_csv(StringIO(content))

    X = pd.get_dummies(df.drop("sales_success", axis=1))
    y = df["sales_success"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump((model, X.columns.tolist()), MODEL_PATH)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy
