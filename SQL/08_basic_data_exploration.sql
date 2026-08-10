-- ==========================================
-- BASIC DATA EXPLORATION
-- ==========================================

-- Query 1: Total Records in Every Table

SELECT 'banks' AS table_name, COUNT(*) AS total_records
FROM banks

UNION ALL

SELECT 'customers', COUNT(*)
FROM customers

UNION ALL

SELECT 'accounts', COUNT(*)
FROM accounts

UNION ALL

SELECT 'transactions', COUNT(*)
FROM transactions

UNION ALL

SELECT 'aml_patterns', COUNT(*)
FROM aml_patterns

UNION ALL

SELECT 'transaction_features', COUNT(*)
FROM transaction_features

UNION ALL

SELECT 'account_features', COUNT(*)
FROM account_features

UNION ALL

SELECT 'customer_features', COUNT(*)
FROM customer_features

UNION ALL

SELECT 'network_features', COUNT(*)
FROM network_features

UNION ALL

SELECT 'analytical_dataset', COUNT(*)
FROM analytical_dataset;

-- ==========================================
-- Query 2: Total Number of Banks
-- ==========================================

SELECT
    COUNT(*) AS total_banks
FROM banks;

-- ==========================================
-- Query 3: Total Number of Customers
-- ==========================================

SELECT
    COUNT(*) AS total_customers
FROM customers;

-- ==========================================
-- Query 4: Total Number of Accounts
-- ==========================================

SELECT
    COUNT(*) AS total_accounts
FROM accounts;

-- ==========================================
-- Query 5: Total Number of Transactions
-- ==========================================

SELECT
    COUNT(*) AS total_transactions
FROM transactions;