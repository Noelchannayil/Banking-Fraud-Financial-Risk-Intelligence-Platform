-- ==========================================
-- Query 1: Top Banks by Customer Count
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    COUNT(DISTINCT a.customer_id) AS total_customers
FROM banks b
JOIN accounts a
    ON b.bank_id = a.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY total_customers DESC
LIMIT 10;

-- ==========================================
-- Query 2: Top Banks by Number of Accounts
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    COUNT(a.account_id) AS total_accounts
FROM banks b
JOIN accounts a
    ON b.bank_id = a.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY total_accounts DESC
LIMIT 10;

-- ==========================================
-- Query 3: Top Banks by Transaction Volume
-- (Fast Version)
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    SUM(af.total_transactions) AS total_transactions
FROM banks b
JOIN account_features af
    ON b.bank_id = af.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY total_transactions DESC
LIMIT 10;

-- ==========================================
-- Query 4: Top Banks by Total Amount Sent
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    ROUND(SUM(af.total_amount_sent), 2) AS total_amount_sent
FROM banks b
JOIN account_features af
    ON b.bank_id = af.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY total_amount_sent DESC
LIMIT 10;

-- ==========================================
-- Query 5: Top Banks by Total Amount Received
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    ROUND(SUM(af.total_amount_received), 2) AS total_amount_received
FROM banks b
JOIN account_features af
    ON b.bank_id = af.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY total_amount_received DESC
LIMIT 10;

-- ==========================================
-- Query 6: Top Banks by Cross-Bank Connections
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    SUM(af.is_cross_bank_account) AS cross_bank_accounts,
    COUNT(af.account_id) AS total_accounts
FROM banks b
JOIN account_features af
    ON b.bank_id = af.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY cross_bank_accounts DESC
LIMIT 10;

-- ==========================================
-- Query 7: Top Banks by Average Transaction Amount
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    ROUND(AVG(af.average_amount_sent), 2) AS avg_amount_sent,
    ROUND(AVG(af.average_amount_received), 2) AS avg_amount_received
FROM banks b
JOIN account_features af
    ON b.bank_id = af.bank_id
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY avg_amount_sent DESC
LIMIT 10;

-- ==========================================
-- Query 8: Banks with Highest Laundering Transactions
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    COUNT(*) AS laundering_transactions
FROM banks b
JOIN transactions t
    ON b.bank_id = t.from_bank_id
WHERE t.is_laundering = 1
GROUP BY
    b.bank_id,
    b.bank_name
ORDER BY laundering_transactions DESC
LIMIT 10;

-- ==========================================
-- Query 9: Banks by Laundering Percentage
-- ==========================================

SELECT
    b.bank_id,
    b.bank_name,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN t.is_laundering = 1 THEN 1 ELSE 0 END) AS laundering_transactions,
    ROUND(
        100 * SUM(CASE WHEN t.is_laundering = 1 THEN 1 ELSE 0 END) / COUNT(*),
        4
    ) AS laundering_percentage
FROM banks b
JOIN transactions t
    ON b.bank_id = t.from_bank_id
GROUP BY
    b.bank_id,
    b.bank_name
HAVING laundering_transactions > 0
ORDER BY laundering_percentage DESC
LIMIT 10;

-- ==========================================
-- Query 10: Banking Summary
-- ==========================================

SELECT
    COUNT(DISTINCT bank_id) AS total_banks,
    COUNT(account_id) AS total_accounts,
    ROUND(AVG(total_transactions), 2) AS avg_transactions_per_account,
    ROUND(AVG(total_amount_sent), 2) AS avg_amount_sent,
    ROUND(AVG(total_amount_received), 2) AS avg_amount_received,
    ROUND(AVG(average_amount_sent), 2) AS avg_transaction_sent,
    ROUND(AVG(average_amount_received), 2) AS avg_transaction_received
FROM account_features;
