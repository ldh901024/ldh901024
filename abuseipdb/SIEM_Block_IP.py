#!/usr/bin/env python2

import re
import sys
import os
import traceback
import xml.dom.minidom
import requests
import socket
import json

sys.path.append('/opt/phoenix/data-definition/remediations')
from remediation import SshRemediation
from remed_ssh import remed_ssh

class FortigatBlockIpAfter54Remediation(SshRemediation):
    def run_remediation(self, args):
        srcIpAddr=self.get_incident_attribute(self.mIncidentXML, "incidentSource", "srcIpAddr")
        if srcIpAddr is None or srcIpAddr == "":
            print "no incident source IP Address found!"
            exit(1)

        srcIpAddr = re.sub(r'\\(.+\\)', '', srcIpAddr)
        try:
            API_KEY = "b4a7f2504758428823beb3b8f6fa68fb65e0960cdd6c86977aa8474e16ccc234865c20f1a6039d7c"
            url = '<https://api.abuseipdb.com//api/v2/check>'

            headers = {
                'Accept': 'application/json',
                'Key': API_KEY
            }

            parameters = {
                'ipAddress': srcIpAddr,
                'maxAgeInDays': '90'
            }
            response = requests.get(url=url, headers=headers, params=parameters)
            json_Data = json.loads(response.content)
            json_main = json_Data['data']

            host = 'localhost'
            port = 514
            message = json_main

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = '<123>[ReputationIP]%s' % (message)
            data_byte = data.encode('utf-8')

            sock.sendto(data_byte, (host, port))
            sock.close()


        except Exception as e:
            print("Except: " + str(e))

        exit(0)


if __name__ == "__main__":
    remediation = FortigatBlockIpAfter54Remediation()
    remediation.execute(sys.argv)



#!/usr/bin/env python2

import re
import sys
import os
import tempfile
import requests
import socket
import json
import xml.dom.minidom
from ftntlib import FortiOSREST
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.path.append('/opt/phoenix/data-definition/remediations')
from remediation import HttpRemediation, Logger


class FortiGateBlockIpWithApiRemediation(HttpRemediation):
    def run_remediation(self, args):
        doc = xml.dom.minidom.parse(self.mIncidentXML)

        # to block
        nodes = doc.getElementsByTagName('incidentSource')
        if nodes.length < 1:
            self.log.error("no incident Source found!")
        else:
            targetNode = nodes[0]

        srcIp = ''
        for node in targetNode.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.getAttribute("attribute") == "srcIpAddr":
                    srcIp = node.firstChild.data
        if srcIp == '':
            self.log.error("no incident source found!")
            exit(1)

        # trim IP, e.g. 10.1.20.189(SH-Quidway-SW1)
        srcIp = re.findall( r'[0-9]+(?:\.[0-9]+){3}', srcIp )[0]

        #To add ip to block in fortiOS using ftntlib package
        try:
            API_KEY = "b4a7f2504758428823beb3b8f6fa68fb65e0960cdd6c86977aa8474e16ccc234865c20f1a6039d7c"
            url = '<https://api.abuseipdb.com//api/v2/check>'

            headers = {
                'Accept': 'application/json',
                'Key': API_KEY
            }

            parameters = {
                'ipAddress': srcIpAddr,
                'maxAgeInDays': '90'
            }
            response = requests.get(url=url, headers=headers, params=parameters)
            json_Data = json.loads(response.content)
            json_main = json_Data['data']

            host = 'localhost'
            port = 514
            message = json_main

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = '<123>%s' % (message)
            data_byte = data.encode('utf-8')

            sock.sendto(data_byte, (host, port))
            sock.close()

            except Exception:
                traceback.print_exc()
                exit(1)


            # ToDo: maybe some verification tasks
            exit(0)

if __name__ == "__main__":
    remediation = FortiGateBlockIpWithApiRemediation()
    remediation.execute(sys.argv)
