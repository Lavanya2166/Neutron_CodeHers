import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

MODEL_PATH = "backend/trained_model.pkl"
DATA_PATH = "backend/product_prize_updated.csv"

def train_model_from_csv(csv_file) -> list:
    df = pd.read_csv(csv_file)
    X = pd.get_dummies(df.drop("sales_success", axis=1))
    y = df["sales_success"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    joblib.dump(model, MODEL_PATH)
    df.to_csv(DATA_PATH, index=False)
    return list(X.columns), acc


def predict_product(model_input_df: pd.DataFrame) -> list:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained. Please upload a training CSV to /train first.")


    model = joblib.load(MODEL_PATH)
    existing_df = pd.read_csv(DATA_PATH)
    X = pd.get_dummies(existing_df.drop("sales_success", axis=1))

    new_data_encoded = pd.get_dummies(model_input_df)
    new_data_encoded = new_data_encoded.reindex(columns=X.columns, fill_value=0)

    predictions = model.predict(new_data_encoded)

    results = []
    for i, pred in enumerate(predictions):
        item = model_input_df.iloc[i]
        reasons = []

        if item["ad_effectiveness"] < 5:
            reasons.append("Advertisement effectiveness is low.")
        if item["price_range"] == "High":
            reasons.append("Product is in a high price range.")
        if item["target_gender"] == "Unisex":
            reasons.append("Unisex products may have broader but less targeted appeal.")

        results.append({
            "product_index": i,
            "success": bool(pred),
            "reasons": reasons
        })

    return results
