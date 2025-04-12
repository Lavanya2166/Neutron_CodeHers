import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("C:\\Users\\garga\\Downloads\\StudentSurvey\\product_prize_updated.csv")

# Features and label
X = pd.get_dummies(df.drop("sales_success", axis=1))  # One-hot encode categorical variables
y = df["sales_success"]

# Split into training and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# --- Take user input ---
print("\nEnter details for the new product:")
target_age_group = input("Target age group (e.g., 18-24, 25-34): ")
target_gender = input("Target gender (e.g., Male, Female, Unisex): ")
product_color = input("Product color (e.g., Red, Blue, Black): ")
price_range = input("Price range (Low, Medium, High): ")
ad_effectiveness = float(input("Advertisement effectiveness (1 to 10): "))

# Create DataFrame for prediction
new_product = pd.DataFrame([{
    "target_age_group": target_age_group,
    "target_gender": target_gender,
    "product_color": product_color,
    "price_range": price_range,
    "ad_effectiveness": ad_effectiveness
}])

# One-hot encode the new data
new_product_encoded = pd.get_dummies(new_product)

# Align new data with model's expected input format
new_product_encoded = new_product_encoded.reindex(columns=X.columns, fill_value=0)

# Predict and display result
prediction = model.predict(new_product_encoded)
print("\nSuccess Prediction for New Product:", "✅ Success" if prediction[0] == 1 else "❌ Failure")
