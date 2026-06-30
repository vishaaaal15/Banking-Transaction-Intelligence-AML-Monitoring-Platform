# Methodology Notes — AML Monitoring Platform

## Data
Synthetic dataset of 252,000 transactions across 18,000 accounts, generated to
resemble realistic retail/corporate banking activity (`generate_data.py`).
Total simulated volume: ~₹1.2B (₹120 Cr). A small subset of accounts (4.5%
"watchlist", 1.5% "high_risk") are seeded with anomalous transaction patterns
to simulate structuring and outlier behavior for detection to find.

## Detection approach
Two complementary statistical methods are used, consistent with how AML
monitoring teams combine rule-based and behavioral detection:

1. **Z-score (per account):** flags transactions that deviate sharply from
   that specific account's own historical transaction size — catches
   account-level behavioral anomalies.
2. **IQR (per channel):** flags transactions that are statistical outliers
   relative to typical activity on that payment channel — catches
   channel-level outliers independent of account history.

## Threshold calibration
Detection thresholds (z-score cutoff, IQR multiplier, and the minimum
suspicious-transaction count for account escalation) are tunable parameters,
not fixed constants. In a production AML setting these are calibrated
against false-positive tolerance and investigator capacity. The thresholds
in `anomaly_detection.py` were tuned to produce a manageable, high-precision
escalation list (a small number of high-confidence accounts) rather than
flagging every statistical outlier — mirroring how real compliance teams
tune monitoring systems to avoid alert fatigue.

## SQL vs. Python roles
SQL queries (`aml_monitoring_queries.sql`) implement deterministic
rule-based monitoring (value thresholds, structuring windows, high-risk
corridors, velocity checks) — the kind of fixed-logic rules a bank's
transaction monitoring system runs continuously. Python anomaly detection
adds a statistical layer on top, catching patterns that fixed rules miss.
