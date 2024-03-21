import csv
import compare
import logging

logging.basicConfig(level=logging.ERROR)


class BackupManager:
    def __init__(self):
        self.mss_fg_count = 0
        self.mss_ax_count = 0
        self.maintain_fg_count = 0
        self.maintain_ax_count = 0
        self.vendor_check = ["Backup_FG", "Backup_Axgate", "Backup_Cisco"]
        self.comparator = compare.CompareResult()

    def read_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            return list(csv.reader(csv_file))

    def process_devices(self, devices):
        processed_devices = []

        for device in devices:
            for vendor in self.vendor_check:
                if vendor in device:
                    processed_device = self.extract_device_info(device)
                    processed_devices.append(processed_device)
                    self.write_backup_list(processed_device)

        return processed_devices

    def extract_device_info(self, device_info):
        return [device_info[i] for i in range(len(device_info)) if device_info[i] in self.vendor_check or i in range(device_info.index(self.vendor_check[0]) - 1, device_info.index(self.vendor_check[0]) + 4)]

    def write_backup_list(self, device_info):
        with open('/backup_list.txt', 'a') as file:
            file.write(','.join(device_info) + '\n')

    def backup_device_config(self, devices):
        for device in devices:
            result = self.comparator.service_check(device[1], device[0])
            if result:
                self.backup_config(result, device)

    def backup_config(self, result, device):
        service, vendor, lhost_ip, lhost_port, lhost_id, lhost_pw = device
        local_path = f"/backup_Config/{service}/{vendor}/{lhost_ip}.conf"

        if "FG" in vendor:
            self.comparator.ssh_scp_check(lhost_ip, lhost_id, lhost_pw, lhost_port)
            self.comparator.ssh_connection(lhost_ip, lhost_id, lhost_pw, lhost_port, local_path)
        elif "Axgate" in vendor:
            self.comparator.ssh_connection_axgate(lhost_ip, lhost_id, lhost_pw, lhost_port, local_path)

        self.increment_device_counter(result)

    def increment_device_counter(self, result):
        if "MSS_FG" in result:
            self.mss_fg_count += 1
        elif "MSS_Axgate" in result:
            self.mss_ax_count += 1
        elif "Maintain_FG" in result:
            self.maintain_fg_count += 1
        elif "Maintain_Axgate" in result:
            self.maintain_ax_count += 1

    def run(self, args):
        devices = self.read_csv("/NAS/ll.csv")
        processed_devices = self.process_devices(devices)
        self.backup_device_config(processed_devices)


if __name__ == "__main__":
    import sys

    backup_manager = BackupManager()
    backup_manager.run(sys.argv)
