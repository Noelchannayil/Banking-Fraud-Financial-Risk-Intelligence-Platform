# 📂 Dataset

This folder contains the documentation for the dataset used in the **Banking Fraud & Financial Risk Intelligence Platform**.

The project uses the **IBM Anti-Money Laundering (AML) HI-Small Dataset**, obtained from **Kaggle**, to perform large-scale banking transaction analysis, Anti-Money Laundering (AML) analysis, financial risk analysis and business intelligence reporting.

The original **September 2022** transaction timeline from the source dataset is preserved throughout the project.

---

## 📊 Dataset Overview

The dataset represents a large-scale synthetic banking ecosystem containing relationships between customers, accounts, banks and financial transactions.

| Metric | Value |
|---|---:|
| **Dataset** | IBM HI-Small AML Dataset |
| **Source** | Kaggle |
| **Transaction Records** | **5.08 Million+** |
| **Customers** | **166K** |
| **Accounts** | **519K** |
| **Banks** | **30K** |
| **Transaction Period** | **September 2022** |
| **Laundering Labels** | Normal / Laundering |
| **Payment Methods** | 7 |
| **Currencies** | Multiple |

---

# 📁 Raw Dataset Files

The original dataset consists of three primary files:

| File | Description |
|---|---|
| `HI-Small_Accounts.csv` | Contains account-level information including account identifiers, customer relationships and banking information. |
| `HI-Small_Trans.csv` | Contains transaction-level information including timestamps, sender and receiver accounts, banks, transaction amounts, currencies, payment methods and laundering labels. |
| `HI-Small_Patterns.txt` | Contains structured transaction patterns associated with Anti-Money Laundering (AML) activities. |

---

## 🏦 `HI-Small_Accounts.csv`

The accounts dataset provides entity-level information required to establish relationships between accounts, customers and banks.

### Key Information

- Account identifiers
- Customer relationships
- Bank identifiers
- Entity information
- Account-level attributes

This dataset is used during the Python ETL process to build account and customer-level analytical features.

---

## 💳 `HI-Small_Trans.csv`

The transaction dataset contains the core financial transaction records used throughout the project.

### Key Transaction Attributes

| Attribute | Description |
|---|---|
| **Timestamp** | Date and time of the transaction |
| **From Bank** | Sender bank identifier |
| **Sender Account** | Originating account |
| **To Bank** | Receiver bank identifier |
| **Receiver Account** | Destination account |
| **Amount Paid** | Amount transferred by the sender |
| **Payment Currency** | Currency used for the payment |
| **Amount Received** | Amount received by the beneficiary |
| **Receiving Currency** | Currency received by the beneficiary |
| **Payment Method** | Transaction payment channel |
| **Laundering Label** | Indicates whether the transaction is labeled as laundering |

---

## 📄 `HI-Small_Patterns.txt`

The patterns file contains structured information describing transaction patterns associated with known Anti-Money Laundering (AML) activities.

The pattern information provides additional context for understanding suspicious transaction behavior and supports the project's AML-oriented analytical workflow.

---

# 🔄 Dataset Processing Pipeline

The raw dataset is processed through the project's Python ETL and feature-engineering pipeline.

```text
IBM HI-Small AML Dataset
          │
          ├── HI-Small_Accounts.csv
          ├── HI-Small_Trans.csv
          └── HI-Small_Patterns.txt
                    │
                    ▼
             Python ETL Pipeline
                    │
                    ▼
              Data Cleaning
                    │
                    ▼
              Data Validation
                    │
                    ▼
            Feature Engineering
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
     Transaction  Account   Customer
      Features   Features   Features
                    │
                    ▼
             Network Features
                    │
                    ▼
          Analytical Dataset
                    │
                    ▼
             MySQL Database
                    │
                    ▼
             SQL Analytics
                    │
                    ▼
             Power BI Reports
