import subprocess
import json
import yaml
import argparse
from pathlib import Path

def parse_log_file(log_file):
    """
    Parse JSON or YAML log file to extract open HTTP/S ports and associated IPs.

    :param log_file: Path to log file (JSON or YAML).
    :return: List of targets in the format [(ip, port), ...].
    """
    try:
        with open(log_file, 'r') as file:
            if log_file.endswith('.json'):
                data = json.load(file)
            elif log_file.endswith(('.yaml', '.yml')):
                data = yaml.safe_load(file)
            else:
                raise ValueError("Unsupported file format. Please provide a JSON or YAML file.")

        return [
            (entry.get("ip"), port_info.get("port"))
            for entry in data.get("hosts", [])
            for port_info in entry.get("ports", [])
            if port_info.get("service") in {"http", "https"}
        ]
    except (json.JSONDecodeError, yaml.YAMLError, FileNotFoundError, ValueError) as e:
        print(f"Error reading log file: {e}")
        return []

def run_command(command, description):
    """
    Run a command as a subprocess and print status messages.

    :param command: Command to run as a list.
    :param description: Description of the command's purpose.
    """
    print(f"Running {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"{description} completed successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e.stderr.strip()}")
        return None

def run_tool(tool_name, args, output_dir, ip, port, protocol):
    """
    Generalized function to run a specified tool (Gobuster or Nikto).

    :param tool_name: Name of the tool ("gobuster" or "nikto").
    :param args: List of additional arguments for the tool.
    :param output_dir: Directory to store the results.
    :param ip: Target IP.
    :param port: Target port.
    :param protocol: Protocol ("http" or "https").
    """
    url = f"{protocol}://{ip}:{port}"
    output_file = output_dir / f"{tool_name}_{ip}_{port}.txt"

    command = [tool_name] + args + ["-u" if tool_name == "gobuster" else "-h", url, "-o", str(output_file)]

    if run_command(command, f"{tool_name.capitalize()} on {url}"):
        print(f"Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Automate web application enumeration and scanning.")
    parser.add_argument("-l", "--log", required=True, help="Path to JSON or YAML log file containing open ports.")
    parser.add_argument("-o", "--output", required=True, help="Directory to store scan results.")

    args = parser.parse_args()
    log_file = args.log
    output_dir = Path(args.output)

    output_dir.mkdir(parents=True, exist_ok=True)

    targets = parse_log_file(log_file)
    if not targets:
        print("No targets found in the log file.")
        return

    for ip, port in targets:
        print(f"Processing target: {ip}:{port}")
        protocol = "https" if port == 443 else "http"
        run_tool("gobuster", ["dir", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"], output_dir, ip, port, protocol)
        run_tool("nikto", [], output_dir, ip, port, protocol)

    print("Web enumeration and scanning completed.")

if __name__ == "__main__":
    main()
