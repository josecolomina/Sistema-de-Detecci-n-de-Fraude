package com.example.transaction_ingestion.model;

import lombok.Data;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Transaction {
    private String id;
    private Double amount;
    private String userId;
    private String merchantId;
    private Long timestamp;
}
