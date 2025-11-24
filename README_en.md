# Real-Time Fraud Detection System

This project is a Proof of Concept (PoC) demonstrating a scalable, hybrid architecture for real-time financial fraud detection. It combines the robustness and static typing of **Java (Spring Boot)** for high-throughput data ingestion with the flexibility and power of **Python**'s data science libraries for real-time analysis and prediction.

## 🚀 Architecture

The system follows an Event-Driven Architecture:

1.  **Ingestion (Java/Spring Boot)**:
    -   Exposes a REST API (`POST /api/transactions`) to receive transactions.
    -   Validates data and acts as a *Producer*, sending events to a Kafka topic.
    -   Designed to handle high concurrency.

2.  **Streaming (Apache Kafka)**:
    -   Acts as the central messaging bus, decoupling the ingestion service from the analysis service.
    -   Ensures message persistence and ordering.

3.  **Detection (Python/Scikit-learn)**:
    -   A *Consumer* service listens to the Kafka topic.
    -   Uses a pre-trained Machine Learning model (`Isolation Forest`) to evaluate each transaction.
    -   Classifies transactions as legitimate or fraudulent in milliseconds.

## 🛠️ Tech Stack

-   **Backend**: Java 17, Spring Boot 3.x, Spring Kafka.
-   **Data Streaming**: Apache Kafka, Zookeeper.
-   **Machine Learning**: Python 3.9+, Scikit-learn, Pandas, Kafka-Python.
-   **Infrastructure**: Docker, Docker Compose.

## 📋 Prerequisites

-   Docker & Docker Compose.
-   Java 17+ (for local dev).
-   Python 3.9+ (for local dev).

## ⚡️ Quick Start

### 1. Start Infrastructure (Kafka)
```bash
docker-compose up -d
```

### 2. Train the Model (Python)
You must generate the base model before starting the detector.
```bash
cd fraud-detector
pip install -r requirements.txt
python train_model.py
```
This will generate a `fraud_model.pkl` file.

### 3. Start Fraud Detector (Python)
```bash
python detector.py
```
The service will start listening for transactions...

### 4. Start Ingestion Service (Java)
In a new terminal:
```bash
cd transaction-ingestion
./mvnw spring-boot:run
```

### 5. Test the System
Send a normal transaction (Amount ~50):
```bash
curl -X POST http://localhost:8080/api/transactions \
     -H "Content-Type: application/json" \
     -d '{"id":"tx1", "amount": 55.0, "userId": "user123", "merchantId": "m1", "timestamp": 1630000000}'
```
*Expected result in Python*: `✅ Transaction OK.`

Send a fraudulent transaction (High amount):
```bash
curl -X POST http://localhost:8080/api/transactions \
     -H "Content-Type: application/json" \
     -d '{"id":"tx2", "amount": 600.0, "userId": "user999", "merchantId": "m2", "timestamp": 1630000000}'
```
*Expected result in Python*: `🚨 FRAUD DETECTED!`

## 🧠 About the Model
We use **Isolation Forest**, an unsupervised learning algorithm effective for anomaly detection. The model "learns" what constitutes a "normal" transaction based on the amount (simplified for this demo) and detects significant deviations.

---
Created by Jose Colomina Alvarez - 2024
