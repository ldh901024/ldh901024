import socket
import time

def send_to_syslog(message, server_address=("10.243.169.100", 514)):
    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 메시지 전송
        sock.sendto(message.encode(), server_address)

    except Exception as e:
        print("오류가 발생했습니다:", str(e))

    finally:
        # 소켓 닫기
        sock.close()

def send_data_to_syslog(data, source_ip):
    try:
        # 데이터를 원격 시스로그 서버로 전송
        send_to_syslog(data.replace("[SOURCE_IP]", source_ip))
        print("데이터를 성공적으로 원격 시스로그 서버로 전송했습니다.")

    except Exception as e:
        print("오류가 발생했습니다:", str(e))

def generate_ips(start_ip, end_ip):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    ips = []

    while start != end:
        ips.append('.'.join(map(str, start)))
        start[3] += 1
        if start[3] > 255:
            start[3] = 0
            start[2] += 1
            if start[2] > 255:
                start[2] = 0
                start[1] += 1
                if start[1] > 255:
                    start[1] = 0
                    start[0] += 1
                    if start[0] > 255:
                        break

    return ips

# 시작 IP와 종료 IP 지정
start_ip = '188.165.33.1'
end_ip = '188.165.33.200'

# 출발지 IP 지정
source_ip_1 = '10.243.169.100'
source_ip_2 = '10.243.169.101'

# IP 리스트 생성
ip_list = generate_ips(start_ip, end_ip)

# IP 리스트를 순회하며 데이터를 원격 시스로그 서버로 전송
for index, ip in enumerate(ip_list):
    # 전송할 데이터 생성
    if index < 3:
        source_ip = source_ip_1
    else:
        source_ip = source_ip_2

    data = f'''2023-06-07 10:32:32|10.2.230.61|12504|10.2.224.118|443|Etc.|Personal Information Leakage|개인 정보 유출 탐지|중간|탐지|GET /comm/filedown/536 HTTP/1.1
    X-Forwarded-For: 188.165.191.121
    X-Forwarded-Proto: https
    X-Forwarded-Port: 443
    Host: www.lxsemicon.com
    X-Amzn-Trace-Id: Root=1-647fdeb8-69ddc158531909d53d57f28c
    User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate;q=1.0, *;q=0.5
    DNT: 1
    Referer: https://www.lxsemicon.com/
    Origin: https://www.lxsemicon.com
    sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="102", "Chromium";v="102"
    sec-ch-ua-mobile: ?0
    sec-gpc: 1
    sec-ch-ua-platform: "Windows"

    |{ip}|DETECT|WAF|10.2.230.13|[마이 넘버(개인 번호) - 일본: 2015 20## ####,2015 20## ####,2015 20## ####]|https|www.lxsemicon.com|/comm/filedown/536|703|[Empty value]|FR'''

    send_data_to_syslog(data, source_ip)