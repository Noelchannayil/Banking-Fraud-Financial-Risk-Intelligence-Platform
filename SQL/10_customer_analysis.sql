-- ==========================================
-- Query 1: Top 10 Customers by Total Transactions
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_transactions,
    cf.total_sent_transactions,
    cf.total_received_transactions
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_transactions DESC
LIMIT 10;

-- ==========================================
-- Query 2: Top 10 Customers by Amount Received
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_received_transactions,
    ROUND(cf.total_amount_received, 2) AS total_amount_received
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_amount_received DESC
LIMIT 10;

-- ==========================================
-- Query 3: Top Customers by Average Transaction Amount
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    ROUND(cf.average_amount_sent, 2) AS average_amount_sent,
    ROUND(cf.average_amount_received, 2) AS average_amount_received
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.average_amount_sent DESC
LIMIT 10;

-- ==========================================
-- Query 4: Customers with Multiple Accounts
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_accounts
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_accounts DESC,
         c.entity_name
LIMIT 10;

-- ==========================================
-- Query 5: Top Customers by Average Amount Received
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    ROUND(cf.average_amount_received,2) AS average_amount_received,
    cf.total_received_transactions
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.average_amount_received DESC
LIMIT 10;

-- ==========================================
-- Query 6: Top Customers by Total Amount Sent
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    ROUND(cf.total_amount_sent, 2) AS total_amount_sent,
    cf.total_sent_transactions
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_amount_sent DESC
LIMIT 10;

-- ==========================================
-- Query 7: Top Customers by Received Transactions
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_received_transactions,
    ROUND(cf.total_amount_received, 2) AS total_amount_received
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY cf.total_received_transactions DESC
LIMIT 10;

-- ==========================================
-- Query 8: Sent-to-Received Transaction Ratio
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_sent_transactions,
    cf.total_received_transactions,
    ROUND(
        cf.total_sent_transactions /
        NULLIF(cf.total_received_transactions, 0),
        2
    ) AS sent_received_ratio
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
WHERE cf.total_received_transactions > 0
ORDER BY sent_received_ratio DESC
LIMIT 10;

-- ==========================================
-- Query 9: Customers with Balanced Activity
-- ==========================================

SELECT
    cf.customer_id,
    c.entity_name,
    cf.total_sent_transactions,
    cf.total_received_transactions,
    ABS(cf.total_sent_transactions - cf.total_received_transactions) AS transaction_difference
FROM customer_features cf
JOIN customers c
    ON cf.customer_id = c.customer_id
ORDER BY transaction_difference ASC
LIMIT 10;

-- ==========================================
-- Query 10: Customer Activity Summary
-- ==========================================

SELECT
    COUNT(*) AS total_customers,
    ROUND(AVG(total_accounts), 2) AS avg_accounts_per_customer,
    ROUND(AVG(total_transactions), 2) AS avg_transactions_per_customer,
    ROUND(AVG(total_amount_sent), 2) AS avg_amount_sent,
    ROUND(AVG(total_amount_received), 2) AS avg_amount_received,
    ROUND(AVG(average_amount_sent), 2) AS avg_transaction_sent,
    ROUND(AVG(average_amount_received), 2) AS avg_transaction_received
FROM customer_features;