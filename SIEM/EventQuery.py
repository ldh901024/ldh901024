import requests
import time
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# URL 설정
url = "https://192.168.249.100/phoenix/rest/query/eventQuery"

# XML 바디 데이터
data = """<?xml version="1.0" encoding="UTF-8"?>
<Reports><Report><DataSource/>
<Name>Search Result - 10:09:57 AM Mar 21 2024</Name>
<Description>Search Result - 10:09:57 AM Mar 21 2024 - 10:10:01 AM Mar 21 2024</Description>
<PatternClause>
<SubPattern id="2750372439" name="">
<SingleEvtConstr>reptDevIpAddr=59.9.162.1</SingleEvtConstr>
</SubPattern>
</PatternClause>
<ReportInterval>
<Low>1711419317</Low>
<High>1712024117</High>
</ReportInterval>
<SelectClause>
<AttrList>phRecvTime,reptDevIpAddr,eventType,eventName,rawEventMsg</AttrList>
</SelectClause></Report></Reports>"""

# 기본 인증 정보 설정
auth = HTTPBasicAuth('super/itsadmin', '2022Dlcmdls!@')

# 요청 보내기
response = requests.post(url, data=data, auth=auth, verify=False)

# 응답 출력
print(response.text)

# 응답으로부터 requestId와 expireTime 추출
root = ET.fromstring(response.text.strip())
request_id = root.attrib['requestId']
expire_time = root.find('.//expireTime').text

print("Request ID:", request_id)
print("Expire Time:", expire_time)

# 결과 조회 URL 생성
result_url = f"https://fsiem.itsin.co.kr/phoenix/rest/query/events/{request_id},{expire_time}/0/1000000"

# 일정 시간 대기
time.sleep(30)

# 결과 조회 요청
result_response = requests.get(result_url, auth=auth, verify=False)

# 결과 텍스트 파일로 저장
filename = 'result_response.txt'
with open(filename, 'w', encoding='utf-8') as file:
    file.write(result_response.text)

# <event> 태그의 개수 계산 (점진적 파싱)
event_count = 0
for _, elem in ET.iterparse(filename, events=('end',)):
    if elem.tag == 'event':
        event_count += 1
        elem.clear()  # 메모리 사용 최적화

# <event> 태그의 개수 출력
print("Event Count:", event_count)
