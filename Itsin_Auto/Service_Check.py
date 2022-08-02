import csv
import os
import sys
import re
import subprocess
import paramiko
import time


class getstart():
    def outdata(self, lines):
        output=""
        for line in lines.readlines():
            output +=line

        return output

    def run_getstart(self, args):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect("172.16.21.1", username="itsadmin", password="2022Dlcmdls!@", port="22", timeout=10)

            cli="config firewall policy"
            stdin, stdout, stderr = ssh_client.exec_command(cli)

            cli = "sh \| grep ips-sensor"
            stdin, stdout, stderr = ssh_client.exec_command(cli)
            msg = self.outdata(stdout)

            result=msg.find('set ips-sensor')
            if result == -1:
                print("IPS 안씀")
            elif result > 0:
                print("IPS 사용중")

            ssh_client.close()


        except Exception as e:
            print("Except: " + str(e))

        except:
            print("Unknown Exception")

        #f.close()


if __name__ == "__main__":
    getssluser = getstart()
    getssluser.run_getstart(sys.argv)
