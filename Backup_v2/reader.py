import csv
import os
import sys

import compare


class getstart():
    def run_getstart(self, args):

        with open("/NAS/ll.csv", 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            array2d = list(csv_reader)

        scheck = compare.Compare_result()

        mssFGCnt = 0
        mssAXCnt = 0
        maintainFGCnt = 0
        maintainAXCnt = 0

        VendorCheck = ["Backup_FG", "Backup_Axgate", "Backup_Cisco"]

        # ===============2D Dynamic List===========================#
        array = []
        array.append([])
        arraynum = 0

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

                        with open('/backup_list.txt', 'a') as file:
                            file.write(','.join(array[arraynum]))
                            file.write('\n')

                        arraynum = arraynum + 1
                    else:
                        continue

                num = num + 1

                if Tempstr is None:
                    break

                if num >= list_len:
                    break

        try:
            arraylen = len(array)
            fornum = 2

            for service, vendor, lhost_ip, lhost_port, lhost_id, lhost_pw in array:
                # =============================cmd and file_path Information====================
                lfilename = lhost_ip + ".conf"
                local_path = "/backup_Config/{t_service}/{t_vendor}/{t_filename}".format(t_service=service,
                                                                                         t_vendor=vendor,
                                                                                         t_filename=lfilename)
                local_path_Axgate = "/backup_Config/{t_service}/{t_vendor}/{t_filename}".format(t_service=service,
                                                                                                t_vendor=vendor,
                                                                                                t_filename=lfilename)
                # ==============================================================================
                """
                #=======================String Clear===================================#
                service = re.sub("[\[\]\']","",str(service))
                lhost_id = re.sub("[\[\]\']","",str(lhost_id))
                lhost_pw = re.sub("[\[\]\']","",str(lhost_pw))
                vendor = re.sub("[\[\]\']","",str(vendor))
                lhost_ip = re.sub("[\[\]\']","",str(lhost_ip))
                lhost_port = re.sub("[\[\]\']","",str(lhost_port))
                #======================================================================#
                """
                result = scheck.service_check(vendor, service)

                if result == "MSS_FG":
                    mssFGCnt += 1
                    scpcmd = "get sys gl | grep scp"
                    scheck.SSH_SCPCheck(lhost_ip, lhost_id, lhost_pw, lhost_port, scpcmd)
                    ssh_result = scheck.SSH_Connection(lhost_ip, lhost_id, lhost_pw, lhost_port, local_path)

                elif result == "MSS_Axgate":
                    mssAXCnt += 1
                    Axgate_cmd = 'sh run'
                    ssh_result = scheck.SSH_Connection_Axgate(lhost_ip, lhost_id, lhost_pw + '\n', lhost_port,
                                                              local_path, Axgate_cmd)
                    if not isinstance(ssh_result, bool):
                        ssh_result = ssh_result.replace("", "")
                        ssh_result = ssh_result.replace("--More--", "")
                        with open(local_path_Axgate, 'w', encoding='utf-8') as f:
                            print(ssh_result, file=f)

                elif result == "Maintain_FG":
                    maintainFGCnt += 1
                    scpcmd = "get sys gl | grep scp"
                    scheck.SSH_SCPCheck(lhost_ip, lhost_id, lhost_pw, lhost_port, scpcmd)
                    ssh_result = scheck.SSH_Connection(lhost_ip, lhost_id, lhost_pw, lhost_port, local_path)

                elif result == "Maintain_Axgate":
                    maintainAXCnt += 1
                    Axgate_cmd = 'sh run'
                    ssh_result = scheck.SSH_Connection_Axgate(lhost_ip, lhost_id, lhost_pw + '\n', lhost_port,
                                                              local_path, Axgate_cmd)
                    if not isinstance(ssh_result, bool):
                        ssh_result = ssh_result.replace("", "")
                        ssh_result = ssh_result.replace("--More--", "")
                        with open(local_path_Axgate, 'w', encoding='utf-8') as f:
                            print(ssh_result, file=f)

                else:
                    print("기타장비\n")

                # ==================file check============================

                if arraylen <= fornum:
                    continue

                fornum = fornum + 1

        except Exception as e:
            print("Except: " + str(e))

        except:
            print("Unknown Exception")


if __name__ == "__main__":
    os.system('rm -rf /NAS/false_check.txt')
    getiplist = getstart()
    getiplist.run_getstart(sys.argv)

