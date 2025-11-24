from kafka import KafkaConsumer
import json
import joblib
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
KAFKA_TOPIC = 'transactions'
KAFKA_BROKER = 'localhost:9092'
MODEL_PATH = 'fraud_model.pkl'

def load_model():
    """
    Loads the pre-trained Isolation Forest model from disk.
    
    Returns:
        model: The loaded Scikit-learn model or None if not found.
    """
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file {MODEL_PATH} not found. Please run train_model.py first.")
        return None
    logger.info(f"Model loaded successfully from {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict_fraud(model, transaction):
    """
    Predicts if a transaction is fraudulent using the loaded model.
    
    Args:
        model: The trained Isolation Forest model.
        transaction (dict): The transaction data containing 'amount'.
    """
    # Extract features (must match training)
    amount = transaction.get('amount')
    
    if amount is None:
        logger.warning("Invalid transaction: missing amount")
        return
    
    # Reshape for prediction
    features = np.array([[amount]])
    
    # Predict
    # IsolationForest returns 1 for normal, -1 for anomaly
    prediction = model.predict(features)[0]
    
    if prediction == -1:
        logger.warning(f"🚨 FRAUD DETECTED! Transaction ID: {transaction.get('id')}, Amount: {amount}, User: {transaction.get('userId')}")
        # In a real production system, we would trigger a block action, send an email, or push to a 'fraud-alerts' topic.
    else:
        logger.info(f"✅ Transaction OK. ID: {transaction.get('id')}, Amount: {amount}")

def main():
    """
    Main function to start the Kafka Consumer.
    """
    logger.info("Starting Fraud Detector Consumer...")
    
    model = load_model()
    if not model:
        return

    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='fraud-detection-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        logger.info(f"Listening on topic '{KAFKA_TOPIC}'...")

        for message in consumer:
            transaction = message.value
            predict_fraud(model, transaction)
            
    except Exception as e:
        logger.error(f"Error in consumer: {e}")

if __name__ == "__main__":
    main()
