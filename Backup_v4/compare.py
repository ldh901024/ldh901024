import paramiko
from scp import SCPClient, SCPException
import time


class CompareResult:
    @staticmethod
    def service_check(cvendor, cservice):
        if cservice == "MSS":
            return f"{cservice}_{cvendor.split('_')[-1]}"
        elif cservice == "Maintain":
            return f"{cservice}_{cvendor.split('_')[-1]}"
        return None

    @staticmethod
    def ssh_connection(host, id, pw, port_num, local_path):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, username=id, password=pw, port=port_num, timeout=10)

            with SCPClient(ssh_client.get_transport()) as scp:
                scp.get("/sys_config", local_path)
            return True

        except SCPException:
            return False

    @staticmethod
    def ssh_connection_axgate(host, id, pw, port_num, local_path, cmd='sh run'):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, username=id, password=pw, port=port_num, timeout=10)

            channel = ssh_client.invoke_shell()
            channel.settimeout(30)

            CompareResult.wait_for_prompt(channel)
            CompareResult.execute_command(channel, id + "\n")
            CompareResult.wait_for_prompt(channel)
            CompareResult.execute_command(channel, pw + "\n")

            output = CompareResult.execute_command(channel, cmd + '\n', wait_for_more=True)
            channel.close()

            if output:
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(output)

            return True

        except Exception as e:
            print(f"SSH connection to Axgate device failed: {e}")
            return False

    @staticmethod
    def ssh_scp_check(host, id, pw, port_num):
        command = "conf sys gl\nset admin-scp en\nend\n"
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, username=id, password=pw, port=port_num, timeout=10)

        stdin, stdout, stderr = ssh_client.exec_command(command)
        ssh_client.close()

    @staticmethod
    def wait_for_prompt(channel, prompt='>', timeout=10):
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time:
                raise TimeoutError("Prompt not found.")
            if channel.recv_ready():
                output = channel.recv(9999).decode('utf-8')
                if prompt in output:
                    break
                time.sleep(0.1)

    @staticmethod
    def execute_command(channel, command, wait_for_more=False, more_prompt='--More--', timeout=10):
        channel.send(command)
        output = ""
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time:
                raise TimeoutError("Command execution timed out.")
            if wait_for_more and more_prompt in output:
                channel.send(' ')
            elif channel.recv_ready():
                output += channel.recv(9999).decode('utf-8')
            else:
                break
            time.sleep(0.1)
        return output
