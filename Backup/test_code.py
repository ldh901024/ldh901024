#!/usr/bin/env python2

import re
import sys
import os
import traceback
import xml.dom.minidom
import time

sys.path.append('/opt/phoenix/data-definition/remediations')
from remediation import SshRemediation
from remed_ssh import remed_ssh
from datetime import datetime

class FortigatBlockIpAfter54Remediation(SshRemediation):
    def run_remediation(self, args):
        srcIpAddr=self.get_incident_attribute(self.mIncidentXML, "incidentSource", "srcIpAddr")
        if srcIpAddr is None or srcIpAddr == "":
            print "no incident source IP Address found!"
            exit(1)

        srcIpAddr = re.sub(r'\\(.+\\)', '', srcIpAddr)
        datetime.today()

        lyear = datetime.today().year
        lmonth = datetime.today().month
        try:
            sshClient = remed_ssh()
            sshClient.setPrompt("(.*[#$%] ?)$")
            # sshClient.setPrompt(".*")
            sshClient.startSession(self.mAccessIp, "2222", self.mUser, self.mPassword)
            cmds = [self.mPassword, "conf t", "security zone untrust ip group G_%s/%s_BlockIP" % (lyear, lmonth), "address %s/32" % srcIpAddr, "end", "wr"]
            time.sleep(0.1)
            results = sshClient.runMultiCmds(cmds, timeout=10)
            print(results)


        except Exception:
            traceback.print_exc()
            exit(1)
        exit(0)


if name == "main":
remediation = FortigatBlockIpAfter54Remediation()
remediation.execute(sys.argv)