-- =====================================================================
-- Banking Transaction Intelligence & AML Monitoring Platform
-- SQL rule-based monitoring queries
-- Table: transactions(transaction_id, account_id, transaction_date,
--                      amount_inr, transaction_type, channel,
--                      counterparty_country, risk_tag)
-- =====================================================================

-- 1. High-value single transactions (structuring / large transfer flag)
-- Flags any transaction above ₹10,00,000 (₹10 lakh) for manual review.
SELECT
    transaction_id,
    account_id,
    transaction_date,
    amount_inr,
    channel,
    counterparty_country
FROM transactions
WHERE amount_inr > 1000000
ORDER BY amount_inr DESC;


-- 2. Potential structuring: multiple sub-threshold transactions from the
-- same account within a 3-day window that sum above ₹10,00,000.
-- (Classic AML pattern: breaking large amounts into smaller ones to avoid
--  triggering single-transaction thresholds.)
WITH txn_windows AS (
    SELECT
        account_id,
        transaction_date,
        amount_inr,
        SUM(amount_inr) OVER (
            PARTITION BY account_id
            ORDER BY transaction_date
            RANGE BETWEEN INTERVAL '2 days' PRECEDING AND CURRENT ROW
        ) AS rolling_3day_sum,
        COUNT(*) OVER (
            PARTITION BY account_id
            ORDER BY transaction_date
            RANGE BETWEEN INTERVAL '2 days' PRECEDING AND CURRENT ROW
        ) AS rolling_3day_count
    FROM transactions
)
SELECT *
FROM txn_windows
WHERE rolling_3day_sum > 1000000
  AND rolling_3day_count >= 3
ORDER BY account_id, transaction_date;


-- 3. High-risk corridor exposure: transactions involving counterparties
-- in jurisdictions flagged for elevated AML risk.
SELECT
    account_id,
    counterparty_country,
    COUNT(*) AS txn_count,
    SUM(amount_inr) AS total_volume
FROM transactions
WHERE counterparty_country IN ('AE', 'HK', 'CH')
GROUP BY account_id, counterparty_country
HAVING SUM(amount_inr) > 500000
ORDER BY total_volume DESC;


-- 4. Velocity check: accounts with an unusually high number of
-- transactions in a single day relative to their historical norm.
WITH daily_counts AS (
    SELECT
        account_id,
        transaction_date,
        COUNT(*) AS txns_that_day
    FROM transactions
    GROUP BY account_id, transaction_date
),
account_avg AS (
    SELECT
        account_id,
        AVG(txns_that_day) AS avg_daily_txns,
        STDDEV(txns_that_day) AS stddev_daily_txns
    FROM daily_counts
    GROUP BY account_id
)
SELECT
    d.account_id,
    d.transaction_date,
    d.txns_that_day,
    a.avg_daily_txns
FROM daily_counts d
JOIN account_avg a ON d.account_id = a.account_id
WHERE d.txns_that_day > a.avg_daily_txns + (3 * COALESCE(a.stddev_daily_txns, 1))
ORDER BY d.txns_that_day DESC;


-- 5. Escalation summary: accounts flagged by more than one rule above,
-- aggregated into a single escalation list for the compliance team.
WITH high_value AS (
    SELECT DISTINCT account_id FROM transactions WHERE amount_inr > 1000000
),
high_risk_corridor AS (
    SELECT account_id
    FROM transactions
    WHERE counterparty_country IN ('AE', 'HK', 'CH')
    GROUP BY account_id
    HAVING SUM(amount_inr) > 500000
)
SELECT
    t.account_id,
    COUNT(*) AS total_transactions,
    SUM(t.amount_inr) AS total_volume,
    MAX(t.risk_tag) AS account_risk_tag
FROM transactions t
WHERE t.account_id IN (SELECT account_id FROM high_value)
   OR t.account_id IN (SELECT account_id FROM high_risk_corridor)
GROUP BY t.account_id
ORDER BY total_volume DESC;


-- 6. Monthly AML alert volume trend (for executive dashboard)
SELECT
    DATE_TRUNC('month', transaction_date::date) AS month,
    COUNT(*) AS flagged_transactions,
    SUM(amount_inr) AS flagged_volume
FROM transactions
WHERE amount_inr > 1000000
   OR counterparty_country IN ('AE', 'HK', 'CH')
GROUP BY DATE_TRUNC('month', transaction_date::date)
ORDER BY month;
