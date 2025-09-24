# notebooks/04_risk_scoring_and_explain.py
import pandas as pd
import numpy as np

df = pd.read_csv("data/scored_transactions.csv")

# weights (tune later)
alpha, beta, gamma, delta = 1.2, 1.5, 3.0, 0.8

z = (alpha * df["anomaly_score"] +
     beta * df["is_high_risk_country"] +
     gamma * df["is_blacklisted_counterparty"] +
     delta * df["amount_zscore"])

risk = 100 * (1 / (1 + np.exp(-z)))
df["risk_score"] = risk.round(2)

def explain(row):
    reasons = []
    if row["is_blacklisted_counterparty"] == 1:
        reasons.append("Connected to blacklisted account")
    if row["is_high_risk_country"] == 1:
        reasons.append("Transaction involves high-risk country")
    if row["amount_zscore"] > 3:
        reasons.append("Amount far above customer baseline")
    if row["anomaly_score"] > np.percentile(df["anomaly_score"], 97):
        reasons.append("Model detected unusual pattern")
    if row["txn_count_day"] > np.percentile(df["txn_count_day"], 95):
        reasons.append("Unusually high daily frequency")
    return "; ".join(reasons) or "No specific rules; model anomaly"

df["reason"] = df.apply(explain, axis=1)
df.to_csv("data/risk_scored_transactions.csv", index=False)

# Flag top risks (e.g., risk >= 80)
flags = df[df["risk_score"] >= 80].sort_values("risk_score", ascending=False)
flags.to_csv("data/flagged_transactions.csv", index=False)
print("Flagged count:", len(flags))
