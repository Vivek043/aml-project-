# notebooks/02_features_batch.py
import pandas as pd
import numpy as np

df = pd.read_csv("data/transactions_sample.csv", parse_dates=["timestamp"])

# Simple high-risk country list (placeholder)
HIGH_RISK = {"AE", "CN"}  # Example only; replace with real risk index
BLACKLIST = {"A00010", "A00077"}  # Example account IDs

# Hour of day
df["hour_of_day"] = df["timestamp"].dt.hour

# Per-customer stats
cust_stats = df.groupby("customer_id")["amount"].agg(["mean", "std"]).rename(columns={"mean":"cust_mean","std":"cust_std"})
df = df.join(cust_stats, on="customer_id")
df["amount_zscore"] = (df["amount"] - df["cust_mean"]) / (df["cust_std"].fillna(0) + 1e-3)

# Is high-risk country / blacklisted counterparty
df["is_high_risk_country"] = df["country"].isin(HIGH_RISK).astype(int)
df["is_blacklisted_counterparty"] = df["dest_account"].isin(BLACKLIST).astype(int)

# Approximate frequency features (batch-friendly)
df["date"] = df["timestamp"].dt.date
freq = df.groupby(["customer_id","date"])["transaction_id"].count().rename("txn_count_day")
df = df.join(freq, on=["customer_id","date"])

# Fill any missing
for col in ["cust_mean","cust_std","txn_count_day"]:
    df[col] = df[col].fillna(0)

feature_cols = [
    "amount","amount_zscore","hour_of_day","txn_count_day",
    "is_high_risk_country","is_blacklisted_counterparty"
]
X = df[feature_cols]
X.to_csv("data/features_batch.csv", index=False)
df.to_csv("data/transactions_with_features.csv", index=False)
print("Features saved:", X.shape)
