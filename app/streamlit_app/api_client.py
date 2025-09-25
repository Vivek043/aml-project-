# app/streamlit_app/api_client.py
import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def score_transaction(tx: dict) -> dict:
    url = f"{API_BASE_URL}/score"
    resp = requests.post(url, json=tx, timeout=5)
    resp.raise_for_status()
    return resp.json()
