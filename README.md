# ANIM: Automated Network Integration Monitor

## Overview

ANIM (Automated Network Integration Monitor) is a Python-based tool designed for network monitoring and management. It provides automated checks for device status, disk space, and firewall rules, with an alert system for quick notification of any issues.

## Features

- Device status monitoring
- Disk space checks
- Firewall rule verification
- Automated OS updates (when configured)
- Alert system with recovery notifications
- Timestamp logging for all alerts

## Requirements

- Python 3.7+
- Required Python packages:
  - json
  - datetime

## Installation

1. Clone the repository:
   ```
   git clone git@gitlab.com:jmc-gl/anim.git
   cd anim
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Create a `config.json` file in the project root directory with the following structure:

```json
{
  "devices": [
    {
      "name": "Device1",
      "ip": "192.168.1.1",
      "auto_update": true
    },
    {
      "name": "Device2",
      "ip": "192.168.1.2",
      "auto_update": false
    }
  ]
}
```

## Usage

Run the main script:

```
python anim_script.py
```

This will start the monitoring process based on the devices specified in `config.json`.

## Running Tests

To run the test suite:

```
python test_anim.py
```

## Contributing

Contributions to ANIM are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

