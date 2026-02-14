import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from app.data.postgres import SessionLocal
from app.data.models import TrainingSample

# Load training data
db = SessionLocal()
data = db.query(TrainingSample).all()
db.close()

if len(data) < 10:
    print("Not enough data to train ML model")
    exit()

# Build DataFrame
df = pd.DataFrame([{
    "base": s.base,
    "rep": s.repetition,
    "behavior": s.behavior,
    "intel": s.intel,
    "y": s.decision
} for s in data])

# Feature engineering
df["risk"] = df["base"] + df["behavior"] + df["intel"] - abs(df["rep"])

# Input features
X = df[["base", "rep", "behavior", "intel", "risk"]]
y = df["y"]

# Train model
model = LogisticRegression(max_iter=500)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("ML Model trained on", len(df), "samples")
