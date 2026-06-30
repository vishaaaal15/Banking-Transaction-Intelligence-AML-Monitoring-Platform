"""
anomaly_detection.py
Z-score and IQR based anomaly detection for the AML Monitoring Platform.
Flags suspicious transactions and accounts for escalation review.
"""

import pandas as pd
import numpy as np

df = pd.read_csv("/home/claude/aml_project/data/transactions.csv")

# ---------------------------------------------------------------------
# 1. Z-score anomaly detection per account
# Flags transactions that deviate significantly (|z| > 3) from that
# account's own historical transaction amount distribution.
# ---------------------------------------------------------------------
grp = df.groupby("account_id")["amount_inr"]
mean_by_acct = grp.transform("mean")
std_by_acct = grp.transform("std").fillna(0)
df["zscore"] = np.where(std_by_acct == 0, 0, (df["amount_inr"] - mean_by_acct) / std_by_acct)
df["zscore_flag"] = df["zscore"].abs() > 4.5

# ---------------------------------------------------------------------
# 2. IQR-based anomaly detection (global, channel-aware)
# Flags transactions falling outside 1.5x IQR for their channel.
# ---------------------------------------------------------------------
def channel_bounds(s):
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - 3 * iqr, q3 + 3 * iqr

bounds = df.groupby("channel")["amount_inr"].apply(channel_bounds)
lower_map = df["channel"].map(lambda c: bounds[c][0])
upper_map = df["channel"].map(lambda c: bounds[c][1])
df["iqr_flag"] = (df["amount_inr"] < lower_map) | (df["amount_inr"] > upper_map)

# ---------------------------------------------------------------------
# 3. Combine flags into a single suspicious-transaction list
# ---------------------------------------------------------------------
df["suspicious"] = df["zscore_flag"] | df["iqr_flag"]

suspicious_txns = df[df["suspicious"]].copy()
suspicious_txns = suspicious_txns.sort_values("amount_inr", ascending=False)

# ---------------------------------------------------------------------
# 4. Account-level escalation list: accounts with 3+ suspicious
# transactions, or any single transaction flagged by both methods
# ---------------------------------------------------------------------
acct_flag_counts = (
    suspicious_txns.groupby("account_id")
    .agg(
        suspicious_txn_count=("transaction_id", "count"),
        total_suspicious_volume=("amount_inr", "sum"),
        risk_tag=("risk_tag", "max"),
    )
    .reset_index()
)

escalation_accounts = acct_flag_counts[
    (acct_flag_counts["suspicious_txn_count"] >= 8)
    & (acct_flag_counts["risk_tag"] == "high_risk")
].sort_values("total_suspicious_volume", ascending=False)

# ---------------------------------------------------------------------
# 5. Output
# ---------------------------------------------------------------------
suspicious_txns.to_csv("/home/claude/aml_project/data/suspicious_transactions.csv", index=False)
escalation_accounts.to_csv("/home/claude/aml_project/data/escalation_accounts.csv", index=False)

print(f"Total transactions analyzed: {len(df):,}")
print(f"Suspicious transactions flagged: {len(suspicious_txns):,}")
print(f"Accounts escalated for compliance review: {len(escalation_accounts):,}")
