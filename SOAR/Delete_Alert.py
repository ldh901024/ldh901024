import requests
import urllib3
import sys
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class getstart():
    def run_getstart(self, args):
        authurl = "https://soar.itsin.co.kr/auth/authenticate"
        auth_data = {
            "credentials": {
                "loginid": "csadmin",
                "password": "Fortinet12#$"
            }
        }

        response = requests.post(authurl, json=auth_data, verify=False)
        text_json = response.json()
        token = text_json.get('token')
        print("Token:", token)

        if not token:
            print("Failed to get token.")
            return

        authheaders = {"Authorization": 'Bearer ' + token}

        alerturl = 'https://soar.itsin.co.kr/api/3/alerts?$limit=10000&__selectFields=["uuid"]'

        # 처음에는 쿼리 결과가 있을 것으로 가정하고 while 루프 진입
        has_results = True
        while has_results:
            response2 = requests.get(alerturl, headers=authheaders, verify=False)

            parsed_data = response2.json()
            uuid_list = [member['uuid'] for member in parsed_data.get('hydra:member', [])]

            print("Total UUIDs:", len(uuid_list))

            if not uuid_list:
                # 쿼리 결과가 없으면 루프 종료
                has_results = False
                break

            delete_url = "https://soar.itsin.co.kr/api/3/delete/alerts"

            # 100개씩 삭제 요청을 보내기
            for i in range(0, len(uuid_list), 100):
                batch_uuid_list = uuid_list[i:i+100]
                delete_data = {
                    "ids": batch_uuid_list
                }
                delete_data_json = json.dumps(delete_data)
                response3 = requests.delete(delete_url, headers=authheaders, data=delete_data_json, verify=False)
                if response3.status_code == 200:
                    print(f"Deleted {len(batch_uuid_list)} records successfully.")
                elif response3.status_code == 207:
                    print("Some records were partially deleted.")
                else:
                    print(f"Failed to delete records. Status code: {response3.status_code}")

if __name__ == "__main__":
    getssluser = getstart()
    getssluser.run_getstart(sys.argv)