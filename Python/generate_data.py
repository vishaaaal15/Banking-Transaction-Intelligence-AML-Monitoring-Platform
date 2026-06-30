"""
generate_data.py
Generates a synthetic banking transaction dataset (250,000+ records, ~₹1.2B+ volume)
for the Banking Transaction Intelligence & AML Monitoring Platform project.
No real customer or institutional data is used.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N_TRANSACTIONS = 252000
N_ACCOUNTS = 18000

CHANNELS = ["NEFT", "RTGS", "IMPS", "UPI", "Wire Transfer", "Cash Deposit", "Cheque"]
CHANNEL_WEIGHTS = [0.22, 0.10, 0.28, 0.25, 0.05, 0.06, 0.04]

TXN_TYPES = ["Credit", "Debit"]

COUNTRIES = ["IN", "AE", "SG", "US", "GB", "HK", "CH"]
COUNTRY_WEIGHTS = [0.82, 0.05, 0.04, 0.04, 0.02, 0.02, 0.01]
HIGH_RISK_COUNTRIES = {"AE", "HK", "CH"}

account_ids = [f"ACC{100000+i}" for i in range(N_ACCOUNTS)]

# Assign each account a baseline behavior profile so a subset can be made anomalous
account_profile = pd.DataFrame({
    "account_id": account_ids,
    "avg_txn_amount": np.random.lognormal(mean=8.15, sigma=0.6, size=N_ACCOUNTS),
    "risk_tag": np.random.choice(
        ["normal", "watchlist", "high_risk"], size=N_ACCOUNTS, p=[0.94, 0.045, 0.015]
    ),
})

rows = []
start_date = pd.Timestamp("2025-01-01")

for i in range(N_TRANSACTIONS):
    acc = account_profile.iloc[np.random.randint(0, N_ACCOUNTS)]
    base_amt = acc["avg_txn_amount"]

    # Inject anomalies for watchlist/high_risk accounts to simulate suspicious patterns
    if acc["risk_tag"] == "high_risk" and np.random.rand() < 0.35:
        amount = base_amt * np.random.uniform(8, 25)  # structuring / large outlier
    elif acc["risk_tag"] == "watchlist" and np.random.rand() < 0.20:
        amount = base_amt * np.random.uniform(4, 10)
    else:
        amount = max(500, np.random.normal(base_amt, base_amt * 0.35))

    country = np.random.choice(COUNTRIES, p=COUNTRY_WEIGHTS)
    day_offset = np.random.randint(0, 365)
    txn_date = start_date + pd.Timedelta(days=int(day_offset))

    rows.append({
        "transaction_id": f"TXN{1000000+i}",
        "account_id": acc["account_id"],
        "transaction_date": txn_date.strftime("%Y-%m-%d"),
        "amount_inr": round(amount, 2),
        "transaction_type": np.random.choice(TXN_TYPES),
        "channel": np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS),
        "counterparty_country": country,
        "risk_tag": acc["risk_tag"],
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/aml_project/data/transactions.csv", index=False)
account_profile.to_csv("/home/claude/aml_project/data/accounts.csv", index=False)

total_volume_cr = df["amount_inr"].sum() / 1e7
print(f"Rows generated: {len(df):,}")
print(f"Total volume: ₹{df['amount_inr'].sum():,.0f} (~₹{total_volume_cr:,.1f} Cr)")
