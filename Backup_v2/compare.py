import os
import sys
import paramiko
import time
import pdb
import pickle
from scp import SCPClient, SCPException


class Compare_result():
    def waitStrems(self,chan):
        time.sleep(1)
        outdata=errdata = ""
        while chan.recv_ready():
            outdata += str(chan.recv(1000))
        while chan.recv_stderr_ready():
            errdata += str(chan.recv_stderr(1000))
        return outdata, errdata
        
 

    def service_check(self,Cvendor,Cservice):
        if Cservice == "MSS":
            if Cvendor == "Backup_FG":
                Cresult="MSS_FG" 
                return Cresult
            elif Cvendor == "Backup_Axgate":
                Cresult="MSS_Axgate"
                return Cresult
            else:
                return "not search device"
        elif Cservice == "Maintain":
            if Cvendor =="Backup_FG":
                Cresult="Maintain_FG"
                return Cresult
            elif Cvendor == "Backup_Axgate":
                Cresult="Maintain_Axgate"
                return Cresult
            else:
                return "not search device"
        else:
            return "not search vendor"

    def SSH_Connection(self,host,id,pw,port_num,local_path):
        try:
            with open("/NAS/trydevice.txt", 'a', encoding='utf-8') as file:
                file.writelines(host+" / ID : "+id+" / PW : "+pw+" / Port : "+port_num)

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host,username=id,password=pw,port=port_num, timeout=10)

            with SCPClient(ssh_client.get_transport()) as scp:
                scp.get("/sys_config", local_path)
                ssh_client.close()
                return True

        except SCPException:
            return False
        except:
            return False
             

    def SSH_Connection_Axgate(self,host,id,pw,port_num,local_path,cmd):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, username=id, password=pw, port=port_num, timeout=10)

            channel = ssh_client.invoke_shell()
            channel.settimeout(30)

            out = channel.recv(9999)

            while True:
                if "Username" in out.decode("utf-8"):
                    channel.send(id)
                    channel.send("\n")
                    while not channel.recv_ready():
                        time.sleep(3)

                    out = channel.recv(9999)
                    time.sleep(1)

                elif "Password" in out.decode("utf-8"):
                    channel.send(pw)
                    channel.send("\n")
                    while not channel.recv_ready():
                        time.sleep(3)

                    out = channel.recv(9999)
                    time.sleep(1)

                else:
                    break

            result = ''
            channel.send(cmd+'\n')

            while not channel.recv_ready():
                time.sleep(3)

            out=channel.recv(9999).decode('utf-8')

            while out:
                if "--More--" in out:
                    result = result + '\n'
                    result = result + out
                    out = ''
                    channel.send(' ')
                    time.sleep(1)
                    if channel.recv_ready():
                        out = channel.recv(9999).decode('utf-8')


                elif out != "":
                    result = result + '\n'
                    result = result + out
                    out = ''
                    if channel.recv_ready():
                        out = channel.recv(9999).decode('utf-8')
                    time.sleep(1)

                else:
                    break

            channel.close()

            if isinstance(result, bool):
                result = "false"

            return result

        except Exception as e:
            print(e)
            return False   
       
        except:
            print("SSH_Connection Error")

    def SSH_SCPCheck(self,host,id,pw,port_num,cmd):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host,username=id,password=pw,port=port_num,timeout=10)
        
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            lines = stdout.readlines()
            msg=""
            for s in lines:
                msg += s + " "
        
            result=msg.find("enable")
         
            if result<0:
                command="conf sys gl\nset admin-scp en\nend\n"
                stdin, stdout, stderr = ssh_client.exec_command(command)
                lines = stdout.readlines()
            else:
                print("SCP Enable") 

            ssh_client.close()

        except (paramiko.AuthenticationException, paramiko.ssh_exception.NoValidConnectionsError):
            print("Auth Fail")

        except:
            print("Compare Exception")


    def FalseFileWrite(self,findresult,host,serviceresult):
        if findresult == True:
            print("Backup Success")
        else:
            if "MSS" in serviceresult:
                with open('/NAS/MSS_False.txt', 'a') as falsetxt:
                    falsetxt.writelines(host)
                    falsetxt.writelines('\n')

            else:
                with open('/NAS/Maintain_False.txt', 'a') as falsetxt:
                    falsetxt.writelines(host)
                    falsetxt.writelines('\n')

