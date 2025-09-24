# notebooks/03_model_isolation_forest.py
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

df = pd.read_csv("data/transactions_with_features.csv")
feature_cols = [
    "amount","amount_zscore","hour_of_day","txn_count_day",
    "is_high_risk_country","is_blacklisted_counterparty"
]
X = df[feature_cols].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

iso = IsolationForest(n_estimators=200, contamination=0.03, random_state=42)
iso.fit(X_scaled)

scores = -iso.score_samples(X_scaled)  # higher means more anomalous
df["anomaly_score"] = scores

joblib.dump(scaler, "models/scaler_if.joblib")
joblib.dump(iso, "models/iso_forest.joblib")
df.to_csv("data/scored_transactions.csv", index=False)
print("Saved data/scored_transactions.csv", df[["anomaly_score"]].describe())
