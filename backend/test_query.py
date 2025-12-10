import requests

data = {"question": "What is Physical AI?", "selected_text": None}
resp = requests.post("http://127.0.0.1:8000/api/query", json=data)
print(resp.json())

requests.post("http://127.0.0.1:8000/ingest")

