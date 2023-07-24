import requests
import re


id=9700
URL = "https://prtg.itsin.co.kr/api/historicdata.csv?id="+str(id)+"&sdate=2023-02-01-00-00-00&edate=2023-03-01-00-00-00&avg=3600&username=itsadmin_API&passhash=3563855026&usecaption=1&channelid=0&columns=datetime,value_"
response = requests.get(URL)
print(response.status_code)

result = response.text

data = []

rows = result.split('\n')

for row in rows:
    columns = row.split('\",')
    for i in range(len(columns)):
        columns[i] = columns[i].strip('"')
    data.append(columns)

num_result = 0
cal = len(data)
with open('./PRTG_API.txt', 'w') as f:
    for j in range(len(data)):
        num_data = re.findall(r'\d{1,4}\.\d+|\d{1,4}', data[j][2])
        #num_data = re.findall(r'\d{3,6}}\.', data[j][4])
        if len(num_data) > 0:
            num_data = [float(num) for num in num_data]
            f.writelines(str(num_data[0]))
            f.writelines('\n')

            print(num_data[0])
            num_result += num_data[0]
        else:
            print('No data found')
print("total : " + str(num_result))
print("cal : " + str(cal))
num_result /= cal
print(num_result)