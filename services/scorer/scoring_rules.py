# services/scorer/scoring_rules.py
from typing import Dict

RISK_WEIGHTS = {
    "high_amount_threshold": 0.6,
    "blacklisted_country": 0.7,
    "rapid_retries": 0.5,
    "new_device_high_amount": 0.4,
}

def score_transaction(tx: Dict) -> Dict:
    """
    tx expected keys: amount, country, device_id, retries_last_10min, is_new_device
    """
    flags = []
    score = 0.0

    if tx.get("amount", 0) >= 10000:
        flags.append("high_amount_threshold")
        score += RISK_WEIGHTS["high_amount_threshold"]

    if tx.get("country") in {"IR", "KP"}:
        flags.append("blacklisted_country")
        score += RISK_WEIGHTS["blacklisted_country"]

    if tx.get("retries_last_10min", 0) >= 3:
        flags.append("rapid_retries")
        score += RISK_WEIGHTS["rapid_retries"]

    if tx.get("is_new_device") and tx.get("amount", 0) >= 3000:
        flags.append("new_device_high_amount")
        score += RISK_WEIGHTS["new_device_high_amount"]

    # cap at 1.0 and derive risk level
    score = min(score, 1.0)
    risk_level = "low"
    if score >= 0.75:
        risk_level = "high"
    elif score >= 0.4:
        risk_level = "medium"

    return {
        "score": round(score, 3),
        "risk_level": risk_level,
        "flags": flags,
    }
