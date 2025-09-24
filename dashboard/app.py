# dashboard/app.py
import streamlit as st
import pandas as pd

st.title("AML: Flagged Transactions")
df = pd.read_csv("data/risk_scored_transactions.csv")
flags = df[df["risk_score"] >= 80].sort_values("risk_score", ascending=False)

st.metric("Total transactions", len(df))
st.metric("Flagged (risk ≥ 80)", len(flags))

st.dataframe(flags[[
    "transaction_id","customer_id","amount","country",
    "risk_score","reason","timestamp","source_account","dest_account"
]])
