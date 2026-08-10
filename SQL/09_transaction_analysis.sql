-- ==========================================
-- Query 1: Transaction Volume by Payment Method
-- ==========================================

SELECT
    payment_format,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY payment_format
ORDER BY total_transactions DESC;

-- ==========================================
-- Query 2: Total Transaction Amount by Payment Method
-- ==========================================

SELECT
    payment_format,
    ROUND(SUM(amount_paid), 2) AS total_amount_paid
FROM transactions
GROUP BY payment_format
ORDER BY total_amount_paid DESC;

-- ==========================================
-- Query 3: Average Transaction Amount by Payment Method
-- ==========================================

SELECT
    payment_format,
    ROUND(AVG(amount_paid), 2) AS average_transaction_amount
FROM transactions
GROUP BY payment_format
ORDER BY average_transaction_amount DESC;

-- ==========================================
-- Query 4: Transaction Count by Currency
-- ==========================================

SELECT
    payment_currency,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY payment_currency
ORDER BY total_transactions DESC;

-- ==========================================
-- Query 5: Total Transaction Amount by Currency
-- ==========================================

SELECT
    payment_currency,
    ROUND(SUM(amount_paid), 2) AS total_amount_paid
FROM transactions
GROUP BY payment_currency
ORDER BY total_amount_paid DESC;

-- ==========================================
-- Query 6: Cross-Bank vs Same-Bank Transactions
-- ==========================================

SELECT
    CASE
        WHEN from_bank_id = to_bank_id THEN 'Same Bank'
        ELSE 'Cross Bank'
    END AS transaction_type,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY transaction_type
ORDER BY total_transactions DESC;

-- ==========================================
-- Query 7: Laundering vs Normal Transactions
-- ==========================================

SELECT
    CASE
        WHEN is_laundering = 1 THEN 'Laundering'
        ELSE 'Normal'
    END AS transaction_status,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY transaction_status
ORDER BY total_transactions DESC;

-- ==========================================
-- Query 8: Top 10 Highest Value Transactions
-- ==========================================

SELECT
    transaction_id,
    timestamp,
    sender_account_id,
    receiver_account_id,
    payment_currency,
    payment_format,
    amount_paid
FROM transactions
ORDER BY amount_paid DESC
LIMIT 10;

-- ==========================================
-- Query 9: Top Customers by Amount Sent
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_sent_transactions,
    ROUND(cf.total_amount_sent,2) AS total_amount_sent
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_amount_sent DESC
LIMIT 10;

-- ==========================================
-- Query 10: Top 10 Accounts by Amount Sent
-- ==========================================

SELECT
    account_id,
    customer_id,
    bank_id,
    total_transactions,
    ROUND(total_amount_sent, 2) AS total_amount_sent
FROM account_features
ORDER BY total_amount_sent DESC
LIMIT 10;