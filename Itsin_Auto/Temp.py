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

        f = open('C:\Temp\syslog.txt', 'r', encoding='UTF-8')
        data = ''
        lines = f.readlines()
        for line in lines:
            data += line
        f.close()

        level = 0
        #facility = "info"
        host = '210.103.187.28'
        port = 514
        #message = str(data)
        message = "CEF:0|Symantec|DataLossPrevention|11.5|Policy123|Policy123|5|cs1Label=Sender cs1=sender123 cs2Label=Recipient cs2=recepient123 msg=rule123 cn1=1 cn1Label=MatchCount cs3Label=IncidentSnapshot cs3=123 cs4Label=DLPSeverity cs4=1 suid=123CEF:0|Symantec|DataLossPrevention|11.5|Policy456|Policy456|5|cs1Label=Sender cs1=sender456 cs2Label=Recipient cs2=recepient456 msg=rule456 cn1=1 cn1Label=MatchCount cs3Label=IncidentSnapshot cs3=456 cs4Label=DLPSeverity cs4=1 suid=456"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '<%d>%s' % (level, message)
        data_byte = data.encode('utf-8')

        sock.sendto(data_byte, (host, port))
        sock.close()


if __name__ == "__main__":
    getiplist = start()
    getiplist.run_start(sys.argv)
