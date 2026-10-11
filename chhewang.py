import subprocess
import requests
import scapy.all as scapy
import os
import threading
from typing import List, Dict, Any

class AndroidHackerTool:
    """
    Orchestrates various hacking modules against an Android device.
    """
    def __init__(self, device_serial: str = None, ip_address: str = None):
        self.serial = device_serial
        self.ip = ip_address
        self.adb_connected = False
        self._check_adb_connection()

    def _check_adb_connection(self):
        """Verifies if the device is accessible via ADB."""
        print("--- Running ADB Connection Check ---")
        try:
            # Check if the device is listed
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and self.serial in result.stdout:
                self.adb_connected = True
                print(f"✅ ADB Connection Successful for {self.serial or 'Default'}")
            else:
                print("❌ ADB Connection Failed. Ensure USB Debugging is enabled.")
        except FileNotFoundError:
            print("❌ ERROR: 'adb' command not found. Ensure ADB is installed and in PATH.")
        except Exception as e:
            print(f"❌ ADB connection error: {e}")

    # =========================================================================
    # 1. LOCAL SYSTEM HACKING (via ADB)
    # =========================================================================

    def run_adb_command(self, command: str) -> str:
        """Executes an arbitrary command on the device via ADB shell."""
        if not self.adb_connected:
            return "ERROR: ADB not connected."
        try:
            cmd_full = ['adb', '-s', self.serial if self.serial else 'default', 'shell', command]
            result = subprocess.run(cmd_full, capture_output=True, text=True, timeout=15)
            return result.stdout + result.stderr
        except Exception as e:
            return f"ADB Execution Error: {e}"

    def attack_filesystem(self, path: str = '/sdcard/Download'):
        """Dumps or lists files from the device's local storage."""
        print("\n--- [1] FILESYSTEM ATTACHMENT ---")
        print(f"Attempting to inspect: {path}")

        # Command to list contents (can be modified to pull specific files)
        list_cmd = f'ls -l {path}'
        output = self.run_adb_command(list_cmd)
        print(f"--- FILES LIST ---\n{output}")

        # Example: Pulling a specific file (requires knowing the file name)
        # pull_cmd = f'adb pull /path/to/secret.txt /local/destination/'
        # print(f"\nPulling file... {self.run_adb_command(pull_cmd)}")


    # =========================================================================
    # 2. NETWORK HACKING (Man-in-the-Middle / Traffic Sniffing)
    # =========================================================================

    def sniff_traffic(self):
        """Uses Scapy to sniff traffic, essential if attacking over Wi-Fi."""
        print("\n--- [2] NETWORK SNIFFING (Requires Wi-Fi/Local Subnet Access) ---")
        print("Note: This requires the sniffing tool to be run locally or within Termux on the phone.")
        try:
            # Example: Sniffing all traffic on the default interface
            packets = scapy. sniff(count=10, store=True)
            print(f"✅ Successfully captured {len(packets)} packets.")
            # You would add logic here to parse HTTP headers, analyze payloads, etc.
        except Exception as e:
            print(f"❌ Sniffing failed. Is Scapy/Wireshark configured correctly? Error: {e}")

    # =========================================================================
    # 3. APPLICATION/API HACKING (If the phone has exposed services)
    # =========================================================================

    def attack_api_endpoints(self, endpoint_url: str, payload_data: Dict):
        """Tests the phone's exposed APIs (e.g., if it runs a local web server)."""
        print("\n--- [3] API/WEBSERVICE ATTACK ---")
        try:
            response = requests.post(endpoint_url, json=payload_data, timeout=10)
            print(f"✅ API Request Sent. Status Code: {response.status_code}")
            print(f"Server Response Snippet: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"❌ API Attack Failed: Could not reach endpoint {endpoint_url}. Error: {e}")


# =========================================================================
# MAIN EXECUTION FLOW
# =========================================================================
if __name__ == "__main__":
    print("=============================================================")
    print("          📱 ANDROID HACKING FRAMEWORK INITIATOR 📱")
    print("=============================================================")

    # --- INPUT GATHERING ---
    # You must decide how to connect: USB Serial or Wi-Fi IP
    serial = input("Enter Device Serial (e.g., SM-G998B) or leave blank for default: ").strip()
    ip = input("Enter Device IP Address (if attacking over network): ").strip()

    # Initialize the tool instance
    hacker = AndroidHackerTool(device_serial=serial, ip_address=ip)

    # --- INTERACTION MENU ---
    while True:
        print("\n\n--- CHOOSE ATTACK VECTOR ---")
        print(" [1] Local System Attack (ADB Shell / File Access)")
        print(" [2] Network Sniffing Attack (Traffic Interception)")
        print(" [3] API / Web Service Attack (Exposed Services)")
        print(" [R] Run all available quick tests")
        print(" [X] Exit Tool")

        choice = input("Select an option: ").upper()

        if choice == '1':
            # Option 1: Local System Attack

            # Check if connected first
            if hacker.adb_connected:
                print("\n>>> --- ADB Shell & File Access ---")

                # Demonstrate shell command execution
                shell_cmd = input("Enter shell command (e.g., 'ls /sdcard', 'dumpsys'): ")
                shell_output = hacker.run_adb_command(shell_cmd)
                print("\n--- COMMAND OUTPUT ---")
                print(shell_output)

                # Demonstrate filesystem monitoring/dumping
                # hacker.attack_filesystem() 

            else:
                print("Cannot run ADB commands; device not connected.")

        elif choice == '2':
            # Option 2: Network Sniffing
            hacker.sniff_traffic()

        elif choice == '3':
            # Option 3: API Attack
            api_url = input("Enter target API URL (e.g., http://192.168.1.10:8080/api/login): ").strip()
            payload = {'username': 'guest', 'password': 'default'} # Example payload
            if api_url:
                hacker.attack_api_endpoints(api_url, payload)

        elif choice == 'R':
            print("\n[RUNNING QUICK FIRE TESTS]")
            hacker.attack_filesystem()
            hacker.sniff_traffic()
            hacker.attack_api_endpoints("http://192.168.1.1/status", {'test': True})

        elif choice == 'X':
            print("\nExiting Android Hacker Tool.")
            break
        else:
            print("Invalid choice. Please try again.")
