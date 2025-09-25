# services/scorer/main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from scoring_rules import score_transaction

app = FastAPI(title="Transaction Scoring Service")

class Transaction(BaseModel):
    transaction_id: str
    amount: float = Field(ge=0)
    currency: str
    country: str
    device_id: str
    is_new_device: bool = False
    retries_last_10min: int = 0
    customer_id: Optional[str] = None
    merchant_id: Optional[str] = None
    timestamp: str

class ScoreResponse(BaseModel):
    transaction_id: str
    score: float
    risk_level: str
    flags: List[str]

@app.post("/score", response_model=ScoreResponse)
def score(tx: Transaction):
    result = score_transaction(tx.dict())
    return ScoreResponse(
        transaction_id=tx.transaction_id,
        score=result["score"],
        risk_level=result["risk_level"],
        flags=result["flags"],
    )
