# Web Enumeration and Scanning Script Documentation

This documentation provides detailed instructions on how to use the `web_enum.py` script for automating web application enumeration and scanning.

---

## Overview

The `web_enum.py` script simplifies the process of:

- **Directory brute-forcing** using **Gobuster**.
- **Vulnerability scanning** using **Nikto**.
- Extracting targets (IPs or domains with open ports) from **JSON** or **YAML** log files.
- Storing organized scan results in a designated output directory.

This tool is tailored for penetration testers, system administrators, and developers to quickly identify and analyze web application vulnerabilities.

---

## Prerequisites

### 1. Install Necessary Tools
Ensure the following are installed:

- **Python 3.6+**
- **Gobuster**
- **Nikto**

Install required Python dependencies:
```bash
pip install pyyaml
```

### 2. Wordlist for Gobuster
A wordlist is required for directory brute-forcing. Common locations include:

- `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

---

## Input Requirements

### Log File Structure
The script processes **JSON** or **YAML** files that specify hosts and their open ports. Below are examples:

#### JSON Format
```json
{
    "hosts": [
        {
            "ip": "192.168.1.10",
            "ports": [
                {"port": 80, "service": "http"},
                {"port": 443, "service": "https"}
            ]
        },
        {
            "ip": "example.com",
            "ports": [
                {"port": 443, "service": "https"}
            ]
        }
    ]
}
```

#### YAML Format
```yaml
hosts:
  - ip: 192.168.1.10
    ports:
      - port: 80
        service: http
      - port: 443
        service: https
  - ip: example.com
    ports:
      - port: 443
        service: https
```

---

## Usage

### Command-Line Arguments
The script accepts the following arguments:

- **`-l, --log`** (required): Path to the log file (JSON or YAML).
- **`-o, --output`** (required): Directory to store the scan results.

### Running the Script

#### Example: Using a JSON Log File
```bash
python web_enum.py -l /path/to/log_file.json -o /path/to/output_directory
```

#### Example: Using a YAML Log File
```bash
python web_enum.py -l /path/to/log_file.yaml -o /path/to/output_directory
```

---

## Output

Results are stored in the specified output directory. Files are named as:

- **Gobuster results**: `gobuster_<ip>_<port>.txt`
- **Nikto results**: `nikto_<ip>_<port>.txt`

### Example Output Structure
```
output_directory/
  gobuster_192.168.1.10_80.txt
  nikto_192.168.1.10_80.txt
  gobuster_192.168.1.10_443.txt
  nikto_192.168.1.10_443.txt
```

---

## Script Workflow

1. **Parse Log File**:
   - Reads the input log file (JSON or YAML).
   - Extracts IPs/domains and their open HTTP/HTTPS ports.

2. **Run Gobuster**:
   - Uses the provided wordlist to perform directory brute-forcing.

3. **Run Nikto**:
   - Conducts vulnerability scanning on the same targets.

4. **Save Results**:
   - Stores results in the specified output directory.

---

## Troubleshooting

### Common Issues and Solutions

- **Error: Unsupported file format**
  - Ensure the log file is JSON or YAML and uses the correct extension (`.json`, `.yaml`, `.yml`).

- **Error: Command not found**
  - Verify that `gobuster` and `nikto` are installed and in your system's PATH.

- **Empty Results**
  - Check if the log file contains valid targets with open HTTP/HTTPS ports.

### Debugging Tips

- Add verbose logging to the script by editing the `run_command` function to print more details.
- Confirm that the input log file is correctly formatted and accessible.

---

## Customization

The script can be customized by:

1. **Changing the Wordlist**:
   - Update the `-w` argument in the Gobuster command to point to a different wordlist.

2. **Adding Additional Arguments**:
   - Modify the script to pass extra parameters to Gobuster or Nikto using their respective `additional_args` fields.

---

## License

This script is licensed under the MIT License. You are free to use, modify, and distribute it under the terms of the license.
