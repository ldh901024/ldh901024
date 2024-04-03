import requests
import urllib3
import sys
import logging

# 로깅 설정
logging.basicConfig(filename='prtg_script.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logging.info("Starting PRTG Manager script")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PRTGManager():
    def __init__(self):
        self.prtg_host = "prtg.itsin.co.kr"
        self.prtg_port = "443"
        self.username = "itsadmin"
        self.passhash = "2670345824"
        self.base_url = f"https://{self.prtg_host}:{self.prtg_port}/api/"
        logging.info("PRTG Manager initialized")

    def group_exists(self, group_name):
        try:
            url = f"{self.base_url}table.json?content=groups&output=json&columns=objid,name&count=*&username={self.username}&passhash={self.passhash}"
            response = requests.get(url, verify=False)
            groups = response.json().get('groups', [])
            for group in groups:
                if group['name'] == group_name:
                    logging.info(f"Group '{group_name}' found with objid: {group['objid']}")
                    return group['objid']
            logging.info(f"Group '{group_name}' not found")
            return None
        except Exception as e:
            logging.error(f"Error checking group exists: {e}")
            return None

    def add_device(self, parent_id, device_name, device_host, device_type):
        try:
            print(self.username)
            print(self.passhash)
            url = f"{self.base_url}adddevice.htm?name={device_name}&host={device_host}&devicetype={device_type}&id={parent_id}&username={self.username}&passhash={self.passhash}"
            response = requests.get(url, verify=False)

            # Unauthorized error check
            if response.status_code == 401:
                logging.error("Unauthorized access. Please check your username and passhash.")
                return "Error: Unauthorized"

            # Check for redirection (status code 302)
            if response.status_code == 302:
                logging.info("Request redirected. Device might have been added, but further verification is needed.")
            return response.text
        except Exception as e:
            logging.error(f"Error adding device: {e}")
            return "Error"

    def run(self, group_name, device_name, device_host, device_type):
        parent_id = "2"  # Local Probe의 ID
        logging.info(f"Checking if group '{group_name}' exists...")
        group_id = self.group_exists(group_name)

        if group_id:
            logging.info(f"Adding device '{device_name}' to the group '{group_name}'...")
            result = self.add_device(group_id, device_name, device_host, device_type)
            logging.info(f"Device '{device_name}' addition result: {result}")
        else:
            logging.error(f"Group '{group_name}' not found. Device '{device_name}' cannot be added.")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        logging.error("Insufficient arguments provided.")
        sys.exit(1)

    group_name = sys.argv[1]
    device_name = sys.argv[2]
    device_host = sys.argv[3]
    device_type = sys.argv[4]

    manager = PRTGManager()
    manager.run(group_name, device_name, device_host, device_type)
