import requests
import time

url = "http://localhost:8000/ask"
payload = {"query": "What is the capital of France?"}

for i in range(100):
    res = requests.post(url, json=payload)
    print(f"{i+1}: {res.status_code} - {res.json()}")
    time.sleep(0.2)  # slight delay between requests