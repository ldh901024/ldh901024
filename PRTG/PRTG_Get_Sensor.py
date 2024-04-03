import requests
import xml.etree.ElementTree as ET

def query_sensors_with_custom_filter(api_url, username, passhash):
    # API 엔드포인트 설정
    sensors_api_endpoint = f"{api_url}/api/table.xml?content=sensors&output=xml&columns=objid,device,sensor,status&filter_tags=Snmpcustomsensor&username={username}&passhash={passhash}"

    try:
        session_sensors = []
        response = requests.get(sensors_api_endpoint)
        response.raise_for_status()

        # XML 데이터 파싱
        root = ET.fromstring(response.content)

        # 센서 정보 추출
        for item in root.findall('.//item'):
            sensor_name = item.find('sensor').text
            if 'session' in sensor_name.lower():  # 대소문자 구분 없이 'session'이 포함된 센서만 선택
                sensor_info = {
                    'objid': item.find('objid').text,
                    'device': item.find('device').text,
                    'sensor': sensor_name,
                    'status': item.find('status').text
                }
                session_sensors.append(sensor_info)

        return session_sensors

    except requests.exceptions.RequestException as e:
        print(f"Error querying sensors: {e}")

# PRTG 서버 URL 및 사용자 인증 정보 설정
prtg_server_url = 'https://prtg.itsin.co.kr'
username = 'itsadmin_API'
passhash = '3563855026'  # 여기에 사용자의 passhash 값을 입력합니다.

# 필터링된 센서 정보 가져오는 함수 호출
filtered_sensors = query_sensors_with_custom_filter(prtg_server_url, username, passhash)

# 결과 출력
if filtered_sensors:
    for sensor in filtered_sensors:
        print(f"Sensor ID: {sensor['objid']}, Device: {sensor['device']}, Sensor: {sensor['sensor']}, Status: {sensor['status']}")
else:
    print("No sensors with 'session' in their name were found.")