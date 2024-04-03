import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

file = 'C:\\Users\\ldh90\\PycharmProjects\\ldh901024\\SOAR\\request.xml'
headers = {'Content-Type':'text/xml'}
URL = 'https://soar.itsin.co.kr/api/triggers/1/deferred/ips'

with open(file) as xml:
    print(xml)
    response = requests.post(URL, data=xml, headers=headers, verify=False)

status = response.status_code
text = response.text