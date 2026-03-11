import requests

url = "https://httpbin.org/delay/10"

r = requests.get(url)

data = r.json()
print("ok:", data["url"])
