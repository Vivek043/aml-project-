import streamlit as st
import pandas as pd

st.title("🚨 AML Suspicious Transaction Monitor")

# Load data
df = pd.read_csv("data/transactions_sample.csv", parse_dates=["timestamp"])

# Simple rule: flag if amount > 10,000
df["risk_score"] = df["amount"].apply(lambda x: 90 if x > 10000 else 20)
df["reason"] = df["amount"].apply(lambda x: "High amount transaction" if x > 10000 else "Normal")

# Show summary
st.metric("Total Transactions", len(df))
st.metric("Flagged Transactions", (df["risk_score"] >= 80).sum())

# Show flagged
flagged = df[df["risk_score"] >= 80]
st.subheader("Flagged Transactions")
st.dataframe(flagged[["transaction_id","customer_id","amount","country","risk_score","reason"]])
