import requests

key = "cat"
r = requests.get(f"https://google.com/search?q={key}")
print(r.text)
