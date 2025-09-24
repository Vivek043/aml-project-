import streamlit as st
import pandas as pd
import requests

st.title("🚨 AML Suspicious Transaction Monitor")

# Load sample data
df = pd.read_csv("data/transactions_sample.csv")

# --- CONFIG ---
USE_API = False  # set to True once your FastAPI service is deployed
API_URL = "https://your-api.onrender.com/score"

# --- SCORING LOGIC ---
if USE_API:
    results = []
    for _, row in df.iterrows():
        txn = row.to_dict()
        try:
            r = requests.post(API_URL, json=txn, timeout=5)
            if r.status_code == 200:
                results.append(r.json())
            else:
                st.warning(f"API error {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"API call failed: {e}")
    scored_df = pd.DataFrame(results)
else:
    # Simple local scoring rule
    df["risk_score"] = df["amount"].apply(lambda x: 90 if x > 10000 else 20)
    df["reason"] = df["amount"].apply(lambda x: "High amount transaction" if x > 10000 else "Normal")
    scored_df = df

# --- DISPLAY ---
if "risk_score" in scored_df.columns:
    st.metric("Total Transactions", len(scored_df))
    st.metric("Flagged Transactions", (scored_df["risk_score"] >= 80).sum())

    st.subheader("Flagged Transactions")
    flagged = scored_df[scored_df["risk_score"] >= 80]
    st.dataframe(flagged[["transaction_id","customer_id","amount","country","risk_score","reason"]])
else:
    st.warning("No 'risk_score' column found. Check API or scoring logic.")
    st.dataframe(scored_df)
