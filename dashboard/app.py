import streamlit as st
import pandas as pd
import requests

st.title("🚨 AML Suspicious Transaction Monitor")

# Load sample data
df = pd.read_csv("data/transactions_sample.csv")

# Call API for scoring
results = []
for _, row in df.iterrows():
    txn = row.to_dict()
    r = requests.post("https://aml-project-8y05.onrender.com/", json=txn)
    results.append(r.json())

scored_df = pd.DataFrame(results)

st.metric("Total Transactions", len(scored_df))
st.metric("Flagged Transactions", (scored_df["risk_score"] >= 80).sum())

st.subheader("Flagged Transactions")
st.dataframe(scored_df[scored_df["risk_score"] >= 80])
