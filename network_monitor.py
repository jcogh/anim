import paramiko
import subprocess
import smtplib
from email.mime.text import MIMEText
import json
import time
from datetime import datetime


class NetworkMonitor:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def check_device(self, device):
        try:
            output = subprocess.check_output(['ping', '-c', '4', device['ip']])
            return True
        except subprocess.CalledProcessError:
            return False

    def ssh_command(self, device, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device['ip'], username=device['username'],
                    password=device['password'])
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        ssh.close()
        return output

    def check_disk_space(self, device):
        command = "df -h / | awk 'NR==2 {print $5}'"
        output = self.ssh_command(device, command)
        return int(output.strip('%'))

    def apply_os_updates(self, device):
        if device['os'] == 'linux':
            update_command = "sudo apt-get update && sudo apt-get upgrade -y"
        elif device['os'] == 'windows':
            update_command = "powershell.exe Install-WindowsUpdate -AcceptAll -AutoReboot"
        return self.ssh_command(device, update_command)

    def check_firewall_rules(self, device):
        if device['os'] == 'linux':
            command = "sudo iptables -L"
        elif device['os'] == 'windows':
            command = "netsh advfirewall show allprofiles"
        return self.ssh_command(device, command)

    def send_email_alert(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.config['email']['from']
        msg['To'] = self.config['email']['to']

        s = smtplib.SMTP(self.config['email']['smtp_server'])
        s.send_message(msg)
        s.quit()

    def run(self):
        while True:
            for device in self.config['devices']:
                if not self.check_device(device):
                    self.send_email_alert(f"Device Down: {device['name']}", f"Device {
                                          device['name']} ({device['ip']}) is not responding to ping.")
                else:
                    disk_space = self.check_disk_space(device)
                    if disk_space > 90:
                        self.send_email_alert(f"Low Disk Space: {device['name']}", f"Device {
                                              device['name']} has {disk_space}% disk usage.")

                    if device.get('auto_update', False):
                        update_output = self.apply_os_updates(device)
                        print(f"Applied updates to {
                              device['name']}:\n{update_output}")

                    firewall_rules = self.check_firewall_rules(device)
                    print(f"Firewall rules for {
                          device['name']}:\n{firewall_rules}")

            time.sleep(self.config['check_interval'])


if __name__ == "__main__":
    monitor = NetworkMonitor('config.json')
    monitor.run()
