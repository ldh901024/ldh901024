import os
import sys
import re
import subprocess
import paramiko
import time

from datetime import datetime


class getstart():

    def run_getstart(self, args):

        datetime.today()
        lyear = datetime.today().year
        lmonth = datetime.today().month

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("210.103.190.131", username="axroot", password="2022Dlcmdls!@", port=2222)

            channel = ssh.invoke_shell()

            out = channel.recv(9999)
            channel.send("2022Dlcmdls!@\n")

            while not channel.recv_ready():
                time.sleep(3)

            out = channel.recv(9999)
            print(out.decode("utf-8"))

            cmd = 'conf t\nsecurity zone untrust ip group G_2022/04_BlockIP\naddress 1.1.1.1/32\nend\nwr'
            cmds = cmd.split('\n')

            for i in cmds:
                print(i)
                channel.send(i)
                channel.send('\n')

            while not channel.recv_ready():
                time.sleep(3)

            out = channel.recv(9999)
            print(out.decode("utf-8"))


            allowed_exit = [-1, 0]

            channel.close()
            exit_code = channel.recv_exit_status()

            if exit_code not in allowed_exit:
                try:
                    print("false")

                except Exception as e:
                    print(e)

            ssh.close()

        except Exception as e:
            print("Except: " + str(e))

        except:
            print("Unknown Exception")


if __name__ == "__main__":
    getssluser = getstart()
    getssluser.run_getstart(sys.argv)

