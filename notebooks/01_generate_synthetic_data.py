# notebooks/01_generate_synthetic_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
np.random.seed(42)

n = 1000
start = datetime(2025, 1, 1)
customers = [f"C{str(i).zfill(4)}" for i in range(100)]
accounts = [f"A{str(i).zfill(5)}" for i in range(200)]
countries = ["US", "IN", "GB", "AE", "CN", "BR"]
channels = ["card", "transfer", "cash", "online"]

rows = []
for i in range(n):
    ts = start + timedelta(minutes=int(np.random.exponential(scale=120)))
    cust = np.random.choice(customers)
    src = np.random.choice(accounts)
    dst = np.random.choice(accounts)
    amt_base = np.random.gamma(shape=2.0, scale=200.0)
    # inject some suspicious spikes
    if np.random.rand() < 0.03:
        amt_base *= np.random.uniform(10, 40)
    row = {
        "transaction_id": f"T{str(i).zfill(6)}",
        "customer_id": cust,
        "source_account": src,
        "dest_account": dst,
        "amount": round(amt_base, 2),
        "timestamp": ts.isoformat(),
        "country": np.random.choice(countries, p=[0.5, 0.2, 0.1, 0.05, 0.1, 0.05]),
        "channel": np.random.choice(channels),
        "location": f"Loc{np.random.randint(1,50)}"
    }
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("data/transactions_sample.csv", index=False)
print("Saved data/transactions_sample.csv", df.shape)
