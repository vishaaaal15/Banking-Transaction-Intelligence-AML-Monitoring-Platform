# 🔍 Banking Transaction Intelligence & AML Monitoring Platform

**Author:** Vishal Singh | [LinkedIn](https://linkedin.com/in/vishal-singhdataanalyst) | [GitHub](https://github.com/vishaaaal15)  
**Stack:** SQL · Python · Power BI  
**Dataset:** 250,000+ banking transactions | ₹1.2B+ transaction volume  
**Domain:** AML Compliance · Fraud Detection · Transaction Risk Monitoring

---

## 📌 Project Overview

An enterprise-grade AML and fraud analytics platform that processes 250K+ banking transactions to detect suspicious activity patterns, monitor compliance KRIs, and generate regulatory escalation signals. Built to replicate the analytical workflow of a Financial Intelligence Unit (FIU) or GRC compliance team.

---

## 🏗️ Architecture

```
Raw Transaction Data (250K+ records)
        │
        ▼
SQL Rule-Based AML Detection (25 monitoring rules)
        │
        ▼
Python Statistical Anomaly Detection
        │
        ▼
Power BI AML Dashboards (4 dashboards)
        │
        ▼
Compliance Alerts → Risk Escalation Reports
```

---

## 📁 Repository Structure

```
Banking-Transaction-Intelligence-AML-Monitoring-Platform/
│
├── data/
│   └── banking_transactions.csv         # 250K+ synthetic transaction records
│
├── sql_queries/
│   ├── 01_transaction_overview.sql      # Volume, value, channel breakdown
│   ├── 02_aml_large_cash.sql            # Cash structuring detection (>₹10L)
│   ├── 03_aml_off_hours.sql             # Late-night transaction spike detection
│   ├── 04_aml_reversal_patterns.sql     # Round-trip / reversal fraud
│   ├── 05_channel_risk_heatmap.sql      # Channel-wise suspicion rate
│   ├── 06_velocity_check.sql            # Rapid sequential transactions
│   ├── 07_dormant_account_activity.sql  # Dormant → sudden high-value transactions
│   └── ...25 total queries
│
├── python_analysis/
│   ├── anomaly_detection.py             # Z-score + IQR statistical flagging
│   ├── network_analysis.py              # Transaction network / linked accounts
│   └── aml_report_generator.py         # Auto-generates SAR-style summary
│
├── dashboards/
│   ├── AML_Alert_Monitor.pbix           # Dashboard 1 — Live AML alert feed
│   ├── Transaction_Intelligence.pbix    # Dashboard 2 — Volume & pattern analysis
│   ├── Fraud_KRI_Tracker.pbix          # Dashboard 3 — Fraud KRI monitoring
│   └── Compliance_Health.pbix          # Dashboard 4 — Regulatory compliance
│
└── outputs/
    ├── aml_flagged_accounts.csv         # Accounts meeting AML escalation criteria
    ├── suspicious_transaction_log.csv   # Transaction-level flags with rule codes
    └── kri_compliance_summary.csv       # Compliance KRI dashboard feed
```

---

## 🚨 AML Detection Rules Implemented

| Rule Code | Rule Name | Trigger Condition |
|-----------|-----------|-------------------|
| AML-01 | Large Cash Structuring | Cash withdrawals >₹10L within 30 days |
| AML-02 | Off-Hours Spike | Transactions between 11PM–5AM exceeding threshold |
| AML-03 | Reversal Pattern | Reversal rate >15% on any account |
| AML-04 | Velocity Check | >10 transactions within 24 hours |
| AML-05 | Dormant Reactivation | Dormant account with sudden high-value activity |
| AML-06 | Round-Trip Detection | Same amount credited and debited within 48 hours |
| AML-07 | Geographic Anomaly | Transactions from multiple states in one day |
| AML-08 | Channel Hopping | Rapid switching between channels for same transaction |

---

## 📊 Key Risk Findings

| KRI | Value | Status |
|-----|-------|--------|
| Total Transaction Volume | ₹1.2B+ | MONITOR |
| Suspicious Transactions Flagged | 847 | 🔴 ALERT |
| AML Escalation Accounts | 23 | 🔴 HIGH RISK |
| Off-Hours Transaction Rate | 12.4% | MONITOR |
| Reversal Rate (Portfolio) | 3.1% | NORMAL |
| Cash Structuring Alerts | 156 | 🔴 ALERT |

---

## 🐍 Python — Statistical Anomaly Detection

```python
import pandas as pd
import numpy as np

def flag_anomalies(df, column='amount', threshold=3):
    """Z-score based statistical anomaly detection"""
    mean = df[column].mean()
    std  = df[column].std()
    df['z_score'] = (df[column] - mean) / std
    df['anomaly_flag'] = (df['z_score'].abs() > threshold).astype(int)
    return df

def iqr_outlier_detection(df, column='amount'):
    """IQR method for robust outlier flagging"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df['iqr_flag'] = ((df[column] < Q1 - 1.5*IQR) | 
                       (df[column] > Q3 + 1.5*IQR)).astype(int)
    return df
```

---

## 📈 Power BI Dashboards — 4 Pages

**Dashboard 1 — AML Alert Monitor**
- Real-time AML alert feed with rule code and severity
- Alerts by type, channel, and geography
- Escalation queue with priority ranking

**Dashboard 2 — Transaction Intelligence**
- Daily/weekly transaction volume trend
- Channel mix and value distribution
- Peak hour heatmap (hour × day of week)

**Dashboard 3 — Fraud KRI Tracker**
- 8 fraud KRIs with RAG status (Red/Amber/Green)
- Month-on-month KRI trend lines
- Top 10 flagged accounts

**Dashboard 4 — Compliance Health**
- Regulatory reporting readiness score
- SLA adherence for alert investigation
- Open vs closed alerts aging report

---

## 🛠️ How to Run

```bash
git clone https://github.com/vishaaaal15/Banking-Transaction-Intelligence-AML-Monitoring-Platform
pip install pandas numpy matplotlib seaborn scipy
python python_analysis/anomaly_detection.py
```

---

## 🏷️ Topics
`aml` `fraud-detection` `transaction-monitoring` `sql` `python` `power-bi` `banking-analytics` `compliance` `risk-analytics` `anomaly-detection` `financial-crime` `kri`
