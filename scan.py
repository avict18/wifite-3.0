import subprocess
from wifite import result
from wifite import logo
from wifite import lines
from colorama import Fore, Style
import os

def scan_networks():
    print(Fore.GREEN + logo + Fore.RESET)
    print(Fore.RED + "Scanning for nearby networks...")
    print(Fore.CYAN + result)
    print("This may take a few seconds...")
    
    # Run the command to scan for networks
    output = subprocess.check_output(['sudo', 'iwlist', 'wlan0', 'scan'])
    
    # Decode the output from bytes to string
    output = output.decode('utf-8')
    
    # Split the output into individual lines
    lines = output.split('\n')
    
    # Print the networks found
    print(f"Scan complete. Networks found:")
    for line in lines:
        if 'ESSID' in line:
            print(Fore.YELLOW + line + Fore.RESET)

if __name__ == '__main__':
    scan_networks()