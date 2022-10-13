import requests
import json
import sys
import pandas
import csv
import logging
import logging.handlers
import socket
import argparse

class start():
    def run_start(self, args):
        API_KEY="b4a7f2504758428823beb3b8f6fa68fb65e0960cdd6c86977aa8474e16ccc234865c20f1a6039d7c"
        url = 'https://api.abuseipdb.com//api/v2/check'

        headers = {
            'Accept' : 'application/json',
            'Key' : API_KEY
        }

        parameters = {
            'ipAddress' : "58.226.22.109",
            'maxAgeInDays': '90'
        }
        response = requests.get(url=url, headers=headers, params=parameters)
        json_Data = json.loads(response.content)
        json_main = json_Data['data']['abuseConfidenceScore']
        print(json_main)
        print(type(json_main))
        tempint=str(json)

        level = 0
        #facility = "info"
        #host = '210.103.187.27'
        #port = 514
        #message = json_main

        #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #data = '<%d>%s' % (level, message)
        #data_byte = data.encode('utf-8')

        #sock.sendto(data_byte, (host, port))
        #sock.close()


if __name__ == "__main__":
    getiplist = start()
    getiplist.run_start(sys.argv)
