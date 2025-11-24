# Sistema de Detección de Fraude en Tiempo Real

Este proyecto es una prueba de concepto (PoC) de una arquitectura híbrida y escalable para la detección de fraude en transacciones financieras. Combina la robustez y tipado estático de **Java (Spring Boot)** para la ingesta de datos de alto rendimiento, con la flexibilidad y potencia de las librerías de Ciencia de Datos de **Python** para el análisis y predicción en tiempo real.

## 🚀 Arquitectura

El sistema sigue una arquitectura orientada a eventos (Event-Driven Architecture):

1.  **Ingesta (Java/Spring Boot)**:
    -   Expone una API REST (`POST /api/transactions`) para recibir transacciones.
    -   Valida los datos y actúa como *Producer* enviando los eventos a un tópico de Kafka.
    -   Diseñado para manejar alta concurrencia.

2.  **Streaming (Apache Kafka)**:
    -   Actúa como el bus de mensajería central, desacoplando el servicio de ingesta del servicio de análisis.
    -   Garantiza la persistencia y orden de los mensajes.

3.  **Detección (Python/Scikit-learn)**:
    -   Un servicio *Consumer* escucha el tópico de Kafka.
    -   Utiliza un modelo de Machine Learning (`Isolation Forest`) pre-entrenado para evaluar cada transacción.
    -   Clasifica la transacción como legítima o fraudulenta en milisegundos.

## 🛠️ Tecnologías

-   **Backend**: Java 17, Spring Boot 3.x, Spring Kafka.
-   **Data Streaming**: Apache Kafka, Zookeeper.
-   **Machine Learning**: Python 3.9+, Scikit-learn, Pandas, Kafka-Python.
-   **Infraestructura**: Docker, Docker Compose.

## 📋 Prerrequisitos

-   Docker y Docker Compose.
-   Java 17+ (para desarrollo local).
-   Python 3.9+ (para desarrollo local).

## ⚡️ Ejecución Rápida

### 1. Levantar Infraestructura (Kafka)
```bash
docker-compose up -d
```

### 2. Entrenar el Modelo (Python)
Es necesario generar el modelo base antes de iniciar el detector.
```bash
cd fraud-detector
pip install -r requirements.txt
python train_model.py
```
Esto generará un archivo `fraud_model.pkl`.

### 3. Iniciar el Detector de Fraude (Python)
```bash
python detector.py
```
El servicio quedará esperando transacciones...

### 4. Iniciar el Servicio de Ingesta (Java)
En una nueva terminal:
```bash
cd transaction-ingestion
./mvnw spring-boot:run
```

### 5. Probar el Sistema
Envía una transacción normal (Monto ~50):
```bash
curl -X POST http://localhost:8080/api/transactions \
     -H "Content-Type: application/json" \
     -d '{"id":"tx1", "amount": 55.0, "userId": "user123", "merchantId": "m1", "timestamp": 1630000000}'
```
*Resultado esperado en Python*: `✅ Transaction OK.`

Envía una transacción fraudulenta (Monto alto):
```bash
curl -X POST http://localhost:8080/api/transactions \
     -H "Content-Type: application/json" \
     -d '{"id":"tx2", "amount": 600.0, "userId": "user999", "merchantId": "m2", "timestamp": 1630000000}'
```
*Resultado esperado en Python*: `🚨 FRAUD DETECTED!`

## 🧠 Sobre el Modelo
Se utiliza **Isolation Forest**, un algoritmo de aprendizaje no supervisado eficaz para la detección de anomalías. El modelo "aprende" qué constituye una transacción "normal" basándose en el monto (simplificado para esta demo) y detecta desviaciones significativas.

---
Hecho por Jose Colomina Alvarez - 2024
