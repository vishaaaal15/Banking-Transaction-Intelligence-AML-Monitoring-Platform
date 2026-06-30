# Banking Transaction Intelligence & AML Monitoring Platform

**Tools:** SQL · Python (Z-score, IQR anomaly detection) · Power BI
**Scope:** 250,000+ transactions · ₹1.2B+ transaction volume

## Overview
A transaction monitoring project simulating an AML (Anti-Money Laundering) surveillance workflow, combining rule-based SQL monitoring with statistical anomaly detection in Python to surface suspicious activity for compliance review.

## What I did
- Processed 250,000+ simulated banking transactions representing ₹1.2B+ in volume across multiple payment channels.
- Wrote SQL rule-based monitoring logic to flag transactions breaching threshold and pattern-based AML criteria, identifying 847 suspicious transactions and 23 accounts warranting escalation.
- Applied Z-score and IQR-based anomaly detection in Python to catch outlier behavior not captured by static rules.
- Built 4 executive Power BI dashboards tracking AML alert volume, fraud KRIs, and compliance review metrics.
- Structured escalation logic and reporting so findings could be reviewed and acted on transparently, reflecting how a compliance/control function would consume the output.

## Why it matters
AML monitoring isn't just about flagging transactions — it's about giving compliance teams a clear, explainable trail from raw data to escalation decision. This project focuses on that full chain: detection logic, dashboarding, and review-ready output.

## Repo contents
- `/sql` — rule-based monitoring and escalation queries
- `/python` — anomaly detection (Z-score, IQR) scripts
- `/dashboards` — Power BI files and exported screenshots
- `/docs` — flagging methodology and threshold definitions

## Data note
This project uses a synthetic transaction dataset built to resemble realistic banking activity patterns. No real account or institutional data is used.
