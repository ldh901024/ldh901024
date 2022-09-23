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
        host = '172.16.21.175'
        port = 514
        message = str(data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '<%d>%s' % (level, message)
        data_byte = data.encode('utf-8')

        sock.sendto(data_byte, (host, port))
        sock.close()


if __name__ == "__main__":
    getiplist = start()
    getiplist.run_start(sys.argv)
