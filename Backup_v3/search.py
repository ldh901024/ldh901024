import sys
import os
import csv
import subprocess

lst = []

lstnum = 0

with open('/backup_list.txt', 'r', encoding='utf-8') as f:
    #for line in f.readline():
    while True:
        line = f.readline().strip()
        #lst.append([])
        lst.append(line.split(','))
        if not line: break


num=0
while True:

    if lst[num][0] is None: break
    
    filepath="/backup_Config/" + lst[num][0] + "/" + lst[num][1] + "/" + lst[num][2] + ".conf"

    result = os.system("ls " + filepath) 

    if result == 0:
        print('success')
    else:
        print('failed')
        with open('/NAS/failed_host.txt', 'a') as f:
            f.write('---'.join(lst[num]))
            f.write('\n')
        

    num = num + 1
