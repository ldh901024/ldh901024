import requests

# PRTG 서버 설정
prtg_server = 'prtg.itsin.co.kr'  # PRTG 서버 주소로 변경하세요.
username = 'itsadmin_API'
passhash = '3563855026'
new_tag = 'Axgate'  # 추가할 새 태그

# 태그 업데이트 함수
def update_device_tags(device_id, current_tags):
    updated_tags = f"{current_tags} {new_tag}"  # 현재 태그에 새 태그 추가
    update_url = f"https://{prtg_server}/api/setobjectproperty.htm"

    update_params = {
        'id': device_id,
        'name': 'tags',
        'value': updated_tags,
        'username': username,
        'passhash': passhash
    }

    # 설정 업데이트 API 요청 실행
    update_response = requests.get(update_url, params=update_params)
    update_response.raise_for_status()  # HTTP 요청 에러 체크

# 디바이스 목록 조회
device_url = f'https://{prtg_server}/api/table.json'
device_params = {
    'content': 'devices',
    'output': 'json',
    'columns': 'objid,tags',
    'username': username,
    'passhash': passhash
}

try:
    device_response = requests.get(device_url, params=device_params)
    device_response.raise_for_status()  # HTTP 요청 에러 체크
    devices = device_response.json().get('devices', [])

    # 각 디바이스에 대해 태그 업데이트
    for device in devices:
        device_id = device['objid']
        current_tags = device['tags']
        update_device_tags(device_id, current_tags)
        print(f"Device ID {device_id} updated with new tag '{new_tag}'.")

except requests.exceptions.HTTPError as err:
    print(f"HTTP 에러 발생: {err}")
except requests.exceptions.RequestException as e:
    print(f"요청 에러 발생: {e}")