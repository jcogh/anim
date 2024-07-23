import json
from datetime import datetime

class NetworkMonitor:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.alerted_devices = {}
    
    def check_device(self, device):
        return True

    def check_disk_space(self, device):
        return 50

    def apply_os_updates(self, device):
        return "Updates applied successfully."

    def check_firewall_rules(self, device):
        return "Firewall rules verified."

    def send_email_alert(self, subject, body):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"ALERT - Time: {timestamp}, Subject: {subject}, Body: {body}")
        return {"subject": subject, "body": body, "timestamp": timestamp}

    def run(self):
        alerts = []
        for device in self.config['devices']:
            device_name = device['name']
            
            device_status = self.check_device(device)
            if not device_status:
                if "down" not in self.alerted_devices.get(device_name, {}):
                    alert = self.send_email_alert(f"Device Down: {device_name}", 
                                                  f"Device {device_name} is not responding.")
                    self.alerted_devices[device_name] = self.alerted_devices.get(device_name, {})
                    self.alerted_devices[device_name]["down"] = alert
                    alerts.append(alert)
            elif "down" in self.alerted_devices.get(device_name, {}):
                alert = self.send_email_alert(f"Device Recovery: {device_name}", 
                                              f"Device {device_name} is back online.")
                alerts.append(alert)
                del self.alerted_devices[device_name]["down"]
            
            disk_space = self.check_disk_space(device)
            if disk_space > 90:
                if "disk" not in self.alerted_devices.get(device_name, {}):
                    alert = self.send_email_alert(f"Low Disk Space: {device_name}", 
                                                  f"Device {device_name} is {disk_space}% full.")
                    self.alerted_devices[device_name] = self.alerted_devices.get(device_name, {})
                    self.alerted_devices[device_name]["disk"] = alert
                    alerts.append(alert)
            elif disk_space <= 90 and "disk" in self.alerted_devices.get(device_name, {}):
                alert = self.send_email_alert(f"Disk Space Recovery: {device_name}", 
                                              f"Device {device_name} disk space is now {disk_space}% full.")
                alerts.append(alert)
                del self.alerted_devices[device_name]["disk"]
            
            if device.get('auto_update', False):
                self.apply_os_updates(device)
            
            self.check_firewall_rules(device)
        
        return alerts

if __name__ == "__main__":
    monitor = NetworkMonitor('config.json')
    monitor.run()
