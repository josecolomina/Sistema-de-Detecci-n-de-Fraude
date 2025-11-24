import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# Create dummy data
# 0: Normal, 1: Fraud (though IsolationForest is unsupervised, we simulate normal data for training)
# Features: amount, userId (hashed?), merchantId (hashed?) -> let's keep it simple: amount
# In reality, we would need more features.

print("Generating dummy data...")
n_samples = 1000
rng = np.random.RandomState(42)

# Normal transactions: amount around 50 with some variance
X_normal = 50 + 10 * rng.randn(n_samples, 1)

# Fraud transactions: amount around 500 or very small
X_outliers = np.concatenate([
    500 + 50 * rng.randn(50, 1),
    1000 + 100 * rng.randn(10, 1)
])

X_train = np.concatenate([X_normal, X_outliers])

# Train Isolation Forest
print("Training Isolation Forest model...")
clf = IsolationForest(random_state=42, contamination=0.06)
clf.fit(X_train)

# Save model
model_path = 'fraud_model.pkl'
joblib.dump(clf, model_path)
print(f"Model saved to {model_path}")

# Test
test_normal = [[55]]
test_fraud = [[600]]
print(f"Prediction for 55 (Normal): {clf.predict(test_normal)[0]}") # Should be 1 (normal)
print(f"Prediction for 600 (Fraud): {clf.predict(test_fraud)[0]}") # Should be -1 (anomaly)
