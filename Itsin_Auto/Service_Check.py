import csv
import os
import sys
import re
import subprocess
import paramiko
import time
import socket

class TimeOutException(Exception):
    pass

class getstart():
    def outdata(self, lines):
        output = ""
        for line in lines.readlines():
            output += line

        return output

    def run_getstart(self, args):
        # File Open
        with open('/NAS/ll.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            array2d = list(csv_reader)

        fused = open('/NAS/IPS_Usage.txt', 'w')
        funused = open('/NAS/IPS_Unused.txt', 'w')

        array = []
        array.append([])
        arraynum=0

        VendorCheck = ["Backup_FG", "test"]

        # Array 입력.
        for line in array2d:
            list_len = len(line)
            num = 0
            while True:
                Tempstr = line[num]
                for vStr in VendorCheck:
                    if line[num] == vStr:
                        array.append([])
                        array[arraynum].append(line[num - 1])
                        array[arraynum].append(line[num])
                        array[arraynum].append(line[num + 1])
                        array[arraynum].append(line[num + 2])
                        array[arraynum].append(line[num + 3])
                        array[arraynum].append(line[num + 4])
                        arraynum = arraynum + 1
                    else:
                        continue

                num = num + 1

                if Tempstr is None:
                    break

                if num >= list_len:
                    break

        try:
            #raise NotImplementedError
            print("오류발생 Pass!")
            for service, vendor, lhost_ip, lhost_port, lhost_id, lhost_pw in array:
                if service == "MSS":
                    try:
                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh_client.connect(lhost_ip, username=lhost_id, password=lhost_pw, port=lhost_port, timeout=10)

                        print(lhost_ip + " 시도중")
                        cli = "config firewall policy"
                        stdin, stdout, stderr = ssh_client.exec_command(cli, timeout=10)

                        cli = "sh \| grep ips-sensor"
                        stdin, stdout, stderr = ssh_client.exec_command(cli, timeout=10)
                        msg = self.outdata(stdout)

                        result = msg.find('set ips-sensor')
                        if result == -1:
                            print("IPS 안씀")
                            funused.write("Service :" + service + " Connect IP : " + lhost_ip + "\n")

                        elif result > 0:
                            print("IPS 사용중")
                            fused.write("Service :" + service + " Connect IP : " + lhost_ip  + "\n")

                        ssh_client.close()
                    except Exception as e:
                        print("For Except: " + str(e))
                        continue
                else:
                    print("놉")

        except Exception as e:
            print("Except: " + str(e))
            pass

        except:
            print("Unknown Exception")
            pass

if __name__ == "__main__":
    getssluser = getstart()
    getssluser.run_getstart(sys.argv)
