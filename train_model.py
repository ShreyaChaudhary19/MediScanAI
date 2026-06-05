import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("disease_dataset.csv")

# Features and target
X = data.drop("disease", axis=1)
y = data["disease"]

# Create model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

# Train model
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")