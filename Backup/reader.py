import csv
import os
import sys
import re
import subprocess

import compare

class getstart():
    def run_getstart(self, args):

        with open("C:\\Users\\ldh\\Downloads\\ll.csv", 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)        
            array2d=list(csv_reader)

        scheck = compare.Compare_result()

        mssFGCnt=0
        mssAXCnt=0
        maintainFGCnt=0
        maintainAXCnt=0

        VendorCheck=["Backup_FG", "Backup_Axgate", "Backup_Cisco"]

        #===============2D Dynamic List===========================#
        array=[]
        array.append([])
        arraynum=0

        for line in array2d:
            list_len=len(line)
            num=0
            while True:
                Tempstr=line[num]
                for vStr in VendorCheck:
                    if line[num] == vStr:
                        array.append([])
                        array[arraynum].append(line[num-1])
                        array[arraynum].append(line[num])
                        array[arraynum].append(line[num+1])
                        array[arraynum].append(line[num+2])
                        array[arraynum].append(line[num+3])
                        array[arraynum].append(line[num+4])
                        arraynum=arraynum+1
                    else:
                        continue

                num=num+1
           
                if Tempstr is None:
                    break

                if num >= list_len:
                    break

        try:
            arraylen=len(array)
            fornum=2

            for service, vendor, lhost_ip, lhost_port, lhost_id, lhost_pw in array:
                #=============================cmd and file_path Information====================
                lfilename=lhost_ip + ".conf"
                findfile="ls -al {t_local_path} | grep {t_filename}".format(t_local_path=local_path, t_filename=lfilename)
                local_path = "/backup_Config/{t_service}/{t_vendor}/{t_filename}".format(t_service=service, t_vendor=vendor, t_filename=lfilename)
                local_path_Axgate = "/backup_Config/{t_service}/{t_vendor}/{t_filename}".format(t_service=service, t_vendor=vendor, t_filename=lfilename)
                findfile_Axgate="ls -al {t_local_path} | grep {t_filename}".format(t_local_path=local_path_Axgate, t_filename=lfilename)
                print(local_path)
                print(local_path_Axgate)
                #==============================================================================
                #=======================String Clear===================================#
                service = re.sub("[\[\]\']","",str(service))
                lhost_id = re.sub("[\[\]\']","",str(lhost_id))
                lhost_pw = re.sub("[\[\]\']","",str(lhost_pw))
                vendor = re.sub("[\[\]\']","",str(vendor))
                lhost_ip = re.sub("[\[\]\']","",str(lhost_ip))
                lhost_port = re.sub("[\[\]\']","",str(lhost_port))
                #======================================================================#

                result = scheck.service_check(vendor,service)


                if result == "MSS_FG":
                    scpcmd="get sys gl | grep scp"
                    scheck.SSH_SCPCheck(lhost_ip,lhost_id,lhost_pw,lhost_port,scpcmd)
                    ssh_result = scheck.SSH_Connection(lhost_ip,lhost_id,lhost_pw,lhost_port,local_path)
                    findcmd = findfile
                    mssFGCnt += 1
                elif result == "MSS_Axgate":
                    Axgate_cmd='sh run'
                    ssh_result = scheck.SSH_Connection_Axgate(lhost_ip, lhost_id, lhost_pw + '\n', lhost_port, local_path, Axgate_cmd)
                    ssh_result = ssh_result.replace("","")
                    ssh_result = ssh_result.replace("--More--","")
                    with open(local_path_Axgate, 'w', encoding='utf-8') as f:
                        print(ssh_result, file=f)

                    #findcmd = findfile_Axgate
                    mssAXCnt += 1
                   
                elif result == "Maintain_FG":
                    scheck.SSH_SCPCheck(lhost_ip,lhost_id,lhost_pw,lhost_port,scpcmd)
                    ssh_result = scheck.SSH_Connection(lhost_ip,lhost_id,lhost_pw,lhost_port,local_path)
                    findcmd = findfile
                    maintainFGCnt += 1

                elif result == "Maintain_Axgate":
                    Axgate_cmd = 'sh run'
                    ssh_result = scheck.SSH_Connection_Axgate(lhost_ip, lhost_id, lhost_pw + '\n', lhost_port,local_path, Axgate_cmd)
                    ssh_result = ssh_result.replace("", "")
                    ssh_result = ssh_result.replace("--More--", "")
                    with open(local_path_Axgate, 'w', encoding='utf-8') as f:
                        print(ssh_result, file=f)

                    # findcmd = findfile_Axgate
                    maintainAXCnt += 1
                else:
                    print("기타장비\n")

                
                #==================file check============================
                #scheck.FileCheck(findcmd,service,vendor,lhost_ip)

                if arraylen <= fornum:
                    continue 

                fornum=fornum+1

            with open('./backup_result','w') as bresult:
                bresult.writelines(mssFGCnt)
                bresult.writelines(maintainFGCnt)
                
        except Exception as e:
            print("Except: " + str(e))

        except:
            print("Unknown Exception")

if __name__ == "__main__":
    os.system('rm -rf /NAS/false_check.txt')
    getiplist = getstart()
    getiplist.run_getstart(sys.argv)

