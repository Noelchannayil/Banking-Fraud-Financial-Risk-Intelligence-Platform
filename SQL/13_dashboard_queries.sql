-- ==========================================
-- Dashboard Query 1: KPI Summary
-- ==========================================

SELECT
    (SELECT COUNT(*) FROM banks) AS total_banks,
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM accounts) AS total_accounts,
    (SELECT COUNT(*) FROM transactions) AS total_transactions,
    (SELECT COUNT(*) FROM transactions
        WHERE is_laundering = 1) AS laundering_transactions,
    (
        SELECT ROUND(SUM(amount_paid),2)
        FROM transactions
    ) AS total_transaction_amount;

    -- ==========================================
-- Dashboard Query 2: Transaction Trend
-- ==========================================

SELECT
    DATE(timestamp) AS transaction_date,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_paid), 2) AS total_amount
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY transaction_date;

-- ==========================================
-- Dashboard Query 3: Payment Method Distribution
-- ==========================================

SELECT
    payment_format,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_paid), 2) AS total_amount
FROM transactions
GROUP BY payment_format
ORDER BY total_transactions DESC;

-- ==========================================
-- Dashboard Query 4: Payment Currency Distribution
-- ==========================================

SELECT
    payment_currency,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_paid), 2) AS total_amount
FROM transactions
GROUP BY payment_currency
ORDER BY total_transactions DESC;

-- ==========================================
-- Dashboard Query 5: Top 10 Banks by Transaction Volume
-- ==========================================

SELECT
    b.bank_name,
    SUM(af.total_transactions) AS total_transactions
FROM banks b
JOIN account_features af
    ON b.bank_id = af.bank_id
GROUP BY
    b.bank_name
ORDER BY total_transactions DESC
LIMIT 10;

-- ==========================================
-- Dashboard Query 6: Top 10 Customers
-- ==========================================

SELECT
    c.customer_id,
    c.entity_name,
    cf.total_transactions
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_transactions DESC
LIMIT 10;

-- ==========================================
-- Dashboard Query 7: Top 10 Accounts by Total Amount Sent
-- ==========================================

SELECT
    af.account_id,
    af.customer_id,
    b.bank_name,
    ROUND(af.total_amount_sent, 2) AS total_amount_sent
FROM account_features af
JOIN banks b
    ON af.bank_id = b.bank_id
ORDER BY af.total_amount_sent DESC
LIMIT 10;

-- ==========================================
-- Dashboard Query 8: Fraud vs Normal Transactions
-- ==========================================

SELECT
    CASE
        WHEN is_laundering = 1 THEN 'Laundering'
        ELSE 'Normal'
    END AS transaction_status,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_paid), 2) AS total_amount
FROM transactions
GROUP BY transaction_status
ORDER BY total_transactions DESC;

-- ==========================================
-- Dashboard Query 9: Cross-Bank vs Same-Bank Transactions
-- ==========================================

SELECT
    CASE
        WHEN from_bank_id = to_bank_id THEN 'Same Bank'
        ELSE 'Cross Bank'
    END AS transaction_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_paid), 2) AS total_amount
FROM transactions
GROUP BY transaction_type
ORDER BY total_transactions DESC;

-- ==========================================
-- Dashboard Query 10: Overall Dashboard Summary
-- ==========================================

SELECT
    COUNT(DISTINCT bank_id) AS total_banks,
    COUNT(account_id) AS total_accounts,
    ROUND(AVG(total_transactions), 2) AS avg_transactions_per_account,
    ROUND(AVG(total_amount_sent), 2) AS avg_amount_sent,
    ROUND(AVG(total_amount_received), 2) AS avg_amount_received,
    ROUND(AVG(average_amount_sent), 2) AS avg_transaction_sent,
    ROUND(AVG(average_amount_received), 2) AS avg_transaction_received,
    ROUND(
        SUM(total_amount_sent) / SUM(total_transactions),
        2
    ) AS overall_avg_transaction_value
FROM account_features;