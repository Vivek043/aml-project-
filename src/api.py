from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    source_account: str
    dest_account: str
    amount: float
    timestamp: str
    country: str
    channel: str
    location: str

@app.post("/score")
def score(txn: Transaction):
    # Simple rule-based scoring for now
    risk_score = 90 if txn.amount > 10000 else 20
    reason = "High amount transaction" if txn.amount > 10000 else "Normal"
    return {
        "transaction_id": txn.transaction_id,
        "risk_score": risk_score,
        "reason": reason
    }
