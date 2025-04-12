import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load existing CSV
csv_path = ("C:\\Users\\garga\\Downloads\\StudentSurvey\\1product_prize_updated.csv")
df = pd.read_csv(csv_path)

# Step 1: Ask how many new entries to add
num_entries = int(input("How many new product entries do you want to add? "))

# Step 2: Input new data
new_data = []
for i in range(num_entries):
    print(f"\n--- Enter details for Product {i + 1} ---")
    target_age_group = input("Enter target age group (e.g., 18-24, 25-34): ")
    target_gender = input("Enter target gender (e.g., Male, Female, Unisex): ")
    product_color = input("Enter product color (e.g., Red, Blue, Black): ")
    price_range = input("Enter price range (Low, Medium, High): ")
    ad_effectiveness = float(input("Enter advertisement effectiveness (1 to 10): "))
    sales_success = int(input("Sales success? (1 for Success, 0 for Failure): "))

    new_data.append({
        "target_age_group": target_age_group,
        "target_gender": target_gender,
        "product_color": product_color,
        "price_range": price_range,
        "ad_effectiveness": ad_effectiveness,
        "sales_success": sales_success
    })

# Step 3: Add new data to the DataFrame
df_new = pd.DataFrame(new_data)
df_updated = pd.concat([df, df_new], ignore_index=True)

# Step 4: Save updated data (overwrite CSV)
df_updated.to_csv(csv_path, index=False)
print("\n✅ CSV file updated with new data.")

# Step 5: Retrain model
X = pd.get_dummies(df_updated.drop("sales_success", axis=1))  # One-hot encode categorical variables
y = df_updated["sales_success"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\n📊 Model retrained with updated data.")
print("Accuracy:", accuracy_score(y_test, y_pred))

# Step 6: Save the model
model_path = "C:\\Users\\garga\\Downloads\\StudentSurvey\\trained_model.pkl"
joblib.dump(model, model_path)
print("💾 Trained model saved successfully.")


