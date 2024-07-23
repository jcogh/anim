import json
from unittest.mock import Mock
from datetime import datetime
from anim_script import NetworkMonitor

class MockDevice:
    def __init__(self, config):
        self.config = config
        self.is_up = True
        self.disk_usage = 50

    def ping(self):
        return self.is_up

    def get_disk_space(self):
        return self.disk_usage

def test_network_monitor():
    with open('config.json', 'r') as f:
        config = json.load(f)

    mock_devices = {device['name']: MockDevice(device) for device in config['devices']}

    monitor = NetworkMonitor('config.json')

    monitor.check_device = Mock(side_effect=lambda device: mock_devices[device['name']].ping())
    monitor.check_disk_space = Mock(side_effect=lambda device: mock_devices[device['name']].get_disk_space())

    print("Initial checks...")
    alerts = monitor.run()
    print(f"Alerts after initial check: {alerts}")
    assert len(alerts) == 0, "Should have no alerts initially"

    print("Simulating device down...")
    mock_devices[config['devices'][0]['name']].is_up = False
    alerts = monitor.run()
    print(f"Alerts after device down: {alerts}")
    assert len(alerts) == 1, "Should have one alert for device down"
    assert alerts[0]['subject'] == f"Device Down: {config['devices'][0]['name']}"
    assert 'timestamp' in alerts[0], "Alert should have a timestamp"

    print("Simulating low disk space...")
    mock_devices[config['devices'][1]['name']].disk_usage = 95
    alerts = monitor.run()
    print(f"Alerts after low disk space: {alerts}")
    assert len(alerts) == 1, "Should have one new alert for low disk space"
    assert alerts[0]['subject'] == f"Low Disk Space: {config['devices'][1]['name']}"

    print("Simulating device recovery...")
    mock_devices[config['devices'][0]['name']].is_up = True
    alerts = monitor.run()
    print(f"Alerts after device recovery: {alerts}")
    assert len(alerts) == 1, "Should have one alert for device recovery"
    assert alerts[0]['subject'] == f"Device Recovery: {config['devices'][0]['name']}"

    print("Simulating disk space recovery...")
    mock_devices[config['devices'][1]['name']].disk_usage = 50
    alerts = monitor.run()
    print(f"Alerts after disk space recovery: {alerts}")
    assert len(alerts) == 1, "Should have one alert for disk space recovery"
    assert alerts[0]['subject'] == f"Disk Space Recovery: {config['devices'][1]['name']}"

    print("Final run - all clear...")
    alerts = monitor.run()
    print(f"Alerts after all clear: {alerts}")
    assert len(alerts) == 0, "Should have no alerts when all is well"

    print("All tests passed successfully!")

if __name__ == "__main__":
    test_network_monitor()
