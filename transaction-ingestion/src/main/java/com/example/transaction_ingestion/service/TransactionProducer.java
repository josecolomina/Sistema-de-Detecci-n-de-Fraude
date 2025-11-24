package com.example.transaction_ingestion.service;

import com.example.transaction_ingestion.model.Transaction;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

/**
 * Service responsible for producing transaction events to Kafka.
 */
@Service
public class TransactionProducer {

    private static final String TOPIC = "transactions";

    @Autowired
    private KafkaTemplate<String, Transaction> kafkaTemplate;

    /**
     * Sends a transaction object to the configured Kafka topic.
     *
     * @param transaction The transaction data to send.
     */
    public void sendTransaction(Transaction transaction) {
        System.out.println("Sending transaction to Kafka: " + transaction);
        kafkaTemplate.send(TOPIC, transaction);
    }
}
