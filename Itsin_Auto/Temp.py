import time
import numpy as np
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

        host = '210.103.187.28'
        port = 10518

        #f = open('C:\\Users\\ldh\\Downloads\\wapple.csv', 'r', encoding='UTF-8')
        rdr = csv.reader(f)
        #data = ''
        data = []
        for line in rdr:
            data.append('[WAF]'.join(line))
        i=0
        print(data)
        #for line in data:
            #print(str(i) + "번째 줄 : ")
            #print(line)
            #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #data_byte = line.encode('utf-8')
            #sock.sendto(data_byte, (host, port))

            #if i==30:
                #break

            #i += 1
        #    data += line
        #f.close()
        #level = 0
        #facility = "info"



        """
        break_num = 0
        sleep_num = 0
        while True:
            sock.sendto(data_byte, (host, port))
            if break_num > 27145:
                break
            if sleep_num > 500:
                sleep_num = 0
                time.sleep(1)

            break_num += 1
            sleep_num += 1
        """
        sock.close()


if __name__ == "__main__":
    getiplist = start()
    getiplist.run_start(sys.argv)
