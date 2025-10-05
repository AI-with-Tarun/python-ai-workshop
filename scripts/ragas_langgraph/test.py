import requests

#books endpoing
url = "http://127.0.0.1:8000/books/"
data = {"title": "Deep Learning using PyTorch", "author": "Luca Pietro Giovanni Antiga, Eli Stevens, Thomas Viehmann"}
#response = requests.post(url, json=data)

#movies endpoint
url = "http://127.0.0.1:8000/movies/"
data = {"title": "Avengers: Endgame", "director": "Anthony Russo, Joe Russo","year":2019}
response = requests.post(url, json=data)
print(response.json())