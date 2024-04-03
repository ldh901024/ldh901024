import re
import sys

array = []
#array.append([])

A = "src-subnet 185.70.106.0"
B = "dst-subnet"
Count = 0

pattern = '\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'

with open(r"C:\Users\ldh\Downloads\efile1.txt", 'r') as fp:
    lines = fp.readlines()

    for line in lines:
        array.append([])
        if A in line:
            #print("A matching")
            regex = re.compile(pattern)
            mo = str(regex.findall(line))
            mo = mo.strip()
            #print(mo)
            array[Count].append(mo)

        if B in line:
            #print("B matching")
            regex = re.compile(pattern)
            mo = str(regex.findall(line))
            mo = mo.strip()
            #print(mo)
            array[Count].append(mo)
            Count += 1

    print(array)