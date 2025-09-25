# scripts/mock_stream.py
import time, uuid, random, requests, os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

countries = ["US", "GB", "IR", "KP", "DE"]
def random_tx():
    amt = random.choice([50, 300, 1200, 3500, 12000])
    return {
        "transaction_id": f"tx_{uuid.uuid4().hex[:8]}",
        "amount": amt,
        "currency": "USD",
        "country": random.choice(countries),
        "device_id": f"dev_{uuid.uuid4().hex[:6]}",
        "is_new_device": random.random() < 0.3,
        "retries_last_10min": random.choice([0,1,2,3,4]),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

def send(tx):
    url = f"{API_BASE_URL}/score"
    r = requests.post(url, json=tx, timeout=5)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    for _ in range(20):
        tx = random_tx()
        result = send(tx)
        print(f"{tx['transaction_id']} -> {result['risk_level']} ({result['score']}) | {result['flags']}")
        time.sleep(1)
