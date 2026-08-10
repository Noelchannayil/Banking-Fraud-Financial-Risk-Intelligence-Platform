-- ==========================================
-- Query 1: Top Accounts by Total Network Degree
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.out_degree,
    nf.in_degree,
    nf.total_degree
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.total_degree DESC
LIMIT 10;

-- ==========================================
-- Query 2: Top Accounts by Outgoing Connections
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.unique_receivers,
    nf.total_outgoing_transactions,
    nf.out_degree
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.out_degree DESC
LIMIT 10;

-- ==========================================
-- Query 3: Top Accounts by Incoming Connections
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.unique_senders,
    nf.total_incoming_transactions,
    nf.in_degree
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.in_degree DESC
LIMIT 10;

-- ==========================================
-- Query 4: Top Accounts by Cross-Bank Connections
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.cross_bank_connections,
    nf.total_degree
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.cross_bank_connections DESC,
         nf.total_degree DESC
LIMIT 10;

-- ==========================================
-- Query 5: Top Accounts by Unique Receivers
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.unique_receivers,
    nf.total_outgoing_transactions
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.unique_receivers DESC
LIMIT 10;

-- ==========================================
-- Query 6: Top Accounts by Unique Senders
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.unique_senders,
    nf.total_incoming_transactions
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.unique_senders DESC
LIMIT 10;

-- ==========================================
-- Query 7: Top Accounts by Outgoing Transactions
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.total_outgoing_transactions,
    nf.unique_receivers
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.total_outgoing_transactions DESC
LIMIT 10;

-- ==========================================
-- Query 8: Top Accounts by Incoming Transactions
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.total_incoming_transactions,
    nf.unique_senders
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY nf.total_incoming_transactions DESC
LIMIT 10;

-- ==========================================
-- Query 9: Accounts with Balanced Activity
-- ==========================================

SELECT
    nf.account_id,
    a.customer_id,
    a.bank_id,
    nf.total_outgoing_transactions,
    nf.total_incoming_transactions,
    ABS(nf.total_outgoing_transactions - nf.total_incoming_transactions) AS transaction_difference
FROM network_features nf
JOIN accounts a
    ON nf.account_id = a.account_id
ORDER BY transaction_difference ASC
LIMIT 10;

-- ==========================================
-- Query 10: Network Activity Summary
-- ==========================================

SELECT
    COUNT(*) AS total_accounts,
    ROUND(AVG(unique_receivers), 2) AS avg_unique_receivers,
    ROUND(AVG(unique_senders), 2) AS avg_unique_senders,
    ROUND(AVG(total_outgoing_transactions), 2) AS avg_outgoing_transactions,
    ROUND(AVG(total_incoming_transactions), 2) AS avg_incoming_transactions,
    ROUND(AVG(total_degree), 2) AS avg_network_degree,
    ROUND(AVG(cross_bank_connections), 2) AS avg_cross_bank_connections
FROM network_features;