package com.example.transaction_ingestion.controller;

import com.example.transaction_ingestion.model.Transaction;
import com.example.transaction_ingestion.service.TransactionProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * REST Controller for handling incoming transaction requests.
 */
@RestController
@RequestMapping("/api/transactions")
public class TransactionController {

    @Autowired
    private TransactionProducer transactionProducer;

    /**
     * Endpoint to receive a new transaction.
     * Validates the input and publishes the event to Kafka.
     *
     * @param transaction The transaction details.
     * @return ResponseEntity with status.
     */
    @PostMapping
    public ResponseEntity<String> createTransaction(@RequestBody Transaction transaction) {
        // Simple validation
        if (transaction.getAmount() == null || transaction.getUserId() == null) {
            return ResponseEntity.badRequest().body("Invalid transaction data");
        }

        // Send to Kafka
        transactionProducer.sendTransaction(transaction);

        return ResponseEntity.ok("Transaction received and processing");
    }
}
