# app/streamlit_app/Home.py
import streamlit as st
from api_client import score_transaction

st.title("Suspicious Transaction Scoring")

with st.form("tx_form"):
    transaction_id = st.text_input("Transaction ID", value="tx_demo_001")
    amount = st.number_input("Amount", min_value=0.0, value=2500.0)
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
    country = st.selectbox("Country", ["US", "IR", "KP", "GB"])
    device_id = st.text_input("Device ID", value="dev_demo")
    is_new_device = st.checkbox("Is new device?", value=True)
    retries = st.number_input("Retries last 10 min", min_value=0, value=0)
    timestamp = st.text_input("Timestamp (ISO8601)", value="2025-09-25T22:00:00Z")
    submitted = st.form_submit_button("Score")

if submitted:
    tx = {
        "transaction_id": transaction_id,
        "amount": amount,
        "currency": currency,
        "country": country,
        "device_id": device_id,
        "is_new_device": is_new_device,
        "retries_last_10min": int(retries),
        "timestamp": timestamp,
    }
    try:
        result = score_transaction(tx)
        st.success(f"Risk: {result['risk_level']} (score={result['score']})")
        st.write("Flags:", result["flags"])
    except Exception as e:
        st.error(f"Scoring failed: {e}")
