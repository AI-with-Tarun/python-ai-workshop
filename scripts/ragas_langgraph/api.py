import requests

URL = "http://127.0.0.1:8000/healthcheck"
response = requests.get(URL)

print(response.json())

URL = "http://127.0.0.1:8000/users2"

payload = {
    "name": "R",
    "age": 24
}
response = requests.post(URL,json=payload)
print(response.json())
