import os
import sys
import paramiko


command="get sys gl | grep scp"

host="172.16.21.1"
id="itsadmin"
pw="2022Dlcmdls!@"
portnum="22"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host,username=id,password=pw,port=portnum, timeout=10)

stdin, stdout, stderr = ssh_client.exec_command(command)
lines = stdout.readlines()
print(lines)
print("\n")

msg=""

for s in lines:
    msg += s + " "

#resultmsg=msg.strip()

result = msg.find("enable")


if result<0:
    command="conf sys gl\nset admin-scp enable\nend\n"
    stdin, stdout, stderr = ssh_client.exec_command(command)
    lines = stdout.readlines()
    print(lines)
else:
    print("Nothing")
