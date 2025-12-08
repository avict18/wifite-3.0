"""
Scanning and Enumeration Module
Performs multi-channel scanning to discover nearby access points and clients.
"""

import subprocess
import re
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from colorama import Fore, Style
from tabulate import tabulate

@dataclass
class AccessPoint:
    """Represents a discovered access point."""
    ssid: str
    bssid: str
    channel: int
    signal_strength: int  # dBm
    security: str  # WEP, WPA, WPA2, WPA3, WPS, Open
    encryption: str  # TKIP, CCMP, etc.
    clients: List[str] = field(default_factory=list)  # List of client MAC addresses
    wps_enabled: bool = False
    client_count: int = 0  # Number of clients
    
    def get_wps_status(self) -> str:
        """Return WPS status as Yes/No."""
        return "Yes" if self.wps_enabled else "No"
    
    def get_encryption_display(self) -> str:
        """Return encryption type for display."""
        if self.security == 'Open':
            return 'Open'
        elif self.security in ['WPA', 'WPA2', 'WPA3']:
            return self.security
        elif self.security == 'WEP':
            return 'WEP'
        else:
            return self.security or 'Unknown'

class NetworkScanner:
    """Scans for nearby wireless networks and clients."""
    
    def __init__(self, interface):
        self.interface = interface
        self.access_points: Dict[str, AccessPoint] = {}  # Keyed by BSSID
        self.scan_duration = 5  # seconds per channel
    
    def scan_networks(self, duration: int = 5):
        """
        Perform multi-channel scan to discover access points.
        Uses airodump-ng for comprehensive scanning.
        """
        print(f"\n{Fore.CYAN}[*] Starting network scan...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take a few seconds...{Style.RESET_ALL}\n")
        
        # Common channels: 2.4GHz (1-11) and 5GHz (36, 40, 44, 48, 149, 153, 157, 161, 165)
        channels = list(range(1, 12)) + [36, 40, 44, 48, 149, 153, 157, 161, 165]
        
        # Use airodump-ng for comprehensive scan
        try:
            # Create temp file for airodump-ng output
            temp_file = '/tmp/wifite_scan'
            
            # Run airodump-ng on all channels
            cmd = [
                'sudo', 'timeout', str(duration * 2),  # Give it more time
                'airodump-ng',
                '--write', temp_file,
                '--output-format', 'csv',
                self.interface
            ]
            
            print(f"{Fore.YELLOW}[*] Scanning all channels...{Style.RESET_ALL}")
            subprocess.run(cmd, capture_output=True, check=False)
            
            # Parse the CSV output
            self._parse_airodump_output(temp_file)
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error during scan: {e}{Style.RESET_ALL}")
            # Fallback to iwlist
            self._scan_with_iwlist()
        
        print(f"\n{Fore.GREEN}[+] Scan complete. Found {len(self.access_points)} access point(s){Style.RESET_ALL}\n")
        return list(self.access_points.values())
    
    def _parse_airodump_output(self, base_filename: str):
        """Parse airodump-ng CSV output."""
        csv_file = f'{base_filename}-01.csv'
        
        if not os.path.exists(csv_file):
            return
        
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Find where AP data starts (after BSSID header)
            ap_start = False
            for line in lines:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Check for header
                if 'BSSID' in line and 'First seen' in line:
                    ap_start = True
                    continue
                
                # Check for station section (clients)
                if 'Station MAC' in line:
                    ap_start = False
                    # Parse clients section
                    self._parse_clients_section(lines[lines.index(line + '\n'):])
                    break
                
                # Parse AP line
                if ap_start:
                    self._parse_ap_line(line)
        
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Could not parse airodump output: {e}{Style.RESET_ALL}")
    
    def _parse_ap_line(self, line: str):
        """Parse a single AP line from airodump-ng CSV."""
        try:
            # Split CSV line
            parts = [p.strip() for p in line.split(',')]
            
            if len(parts) < 14:
                return
            
            bssid = parts[0].strip()
            if not bssid or bssid == 'BSSID' or len(bssid) != 17:
                return
            
            # Extract fields from CSV
            # Format: BSSID, First seen, Last seen, channel, Speed, Privacy, Cipher, Auth, Power, beacons, #IV, LAN IP, ID-length, ESSID, Key
            channel = int(parts[3]) if len(parts) > 3 and parts[3].strip().isdigit() else 1
            power = int(parts[8]) if len(parts) > 8 and parts[8].strip().lstrip('-').isdigit() else -100
            encryption = parts[5] if len(parts) > 5 else 'Unknown'
            ssid = parts[13].strip() if len(parts) > 13 else '<hidden>'
            
            # Determine security type
            security = self._determine_security(encryption, parts)
            wps_enabled = 'WPS' in encryption or any('WPS' in p for p in parts)
            
            # Create or update AP
            if bssid not in self.access_points:
                self.access_points[bssid] = AccessPoint(
                    ssid=ssid,
                    bssid=bssid,
                    channel=channel,
                    signal_strength=power,
                    security=security,
                    encryption=encryption,
                    wps_enabled=wps_enabled,
                    client_count=0
                )
            else:
                # Update existing AP with better signal if found
                ap = self.access_points[bssid]
                if power > ap.signal_strength:
                    ap.signal_strength = power
                if ssid != '<hidden>' and ap.ssid == '<hidden>':
                    ap.ssid = ssid
        
        except Exception as e:
            pass  # Skip malformed lines
    
    def _parse_clients_section(self, lines: List[str]):
        """Parse clients section to count clients per AP."""
        ap_clients = {}  # BSSID -> count
        
        for line in lines[1:]:  # Skip header
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(',')
            if len(parts) > 5:
                # Check if client is associated with an AP (BSSID in parts[5])
                bssid = parts[5].strip() if len(parts) > 5 else ''
                if bssid and len(bssid) == 17:
                    ap_clients[bssid] = ap_clients.get(bssid, 0) + 1
        
        # Update AP client counts
        for bssid, count in ap_clients.items():
            if bssid in self.access_points:
                self.access_points[bssid].client_count = count
                self.access_points[bssid].clients = [f"client_{i}" for i in range(count)]  # Placeholder
    
    def _scan_with_iwlist(self):
        """Fallback scanning method using iwlist."""
        try:
            result = subprocess.run(
                ['sudo', 'iwlist', self.interface, 'scan'],
                capture_output=True,
                text=True,
                check=False
            )
            
            current_ap = None
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                # BSSID
                match = re.search(r'Address:\s*([0-9A-Fa-f:]{17})', line)
                if match:
                    bssid = match.group(1)
                    if bssid not in self.access_points:
                        self.access_points[bssid] = AccessPoint(
                            ssid='<hidden>',
                            bssid=bssid,
                            channel=1,
                            signal_strength=-100,
                            security='Unknown',
                            encryption='',
                            wps_enabled=False,
                            client_count=0
                        )
                    current_ap = self.access_points[bssid]
                    continue
                
                if current_ap:
                    # SSID
                    match = re.search(r'ESSID:"([^"]+)"', line)
                    if match:
                        current_ap.ssid = match.group(1)
                    
                    # Signal strength
                    match = re.search(r'Signal level=(-?\d+)', line)
                    if match:
                        current_ap.signal_strength = int(match.group(1))
                    
                    # Encryption
                    if 'WPA2' in line:
                        current_ap.security = 'WPA2'
                    elif 'WPA' in line:
                        current_ap.security = 'WPA'
                    elif 'WEP' in line:
                        current_ap.security = 'WEP'
                    
                    # WPS
                    if 'WPS' in line:
                        current_ap.wps_enabled = True
                    
                    # Channel
                    match = re.search(r'Channel:(\d+)', line)
                    if match:
                        current_ap.channel = int(match.group(1))
        
        except Exception:
            pass
    
    def _determine_security(self, encryption_str: str, parts: List[str]) -> str:
        """Determine security type from encryption string."""
        enc_lower = encryption_str.lower()
        full_text = ' '.join(parts).lower()
        
        if 'wpa3' in enc_lower or 'wpa3' in full_text:
            return 'WPA3'
        elif 'wpa2' in enc_lower or 'wpa2' in full_text:
            return 'WPA2'
        elif 'wpa' in enc_lower or 'wpa' in full_text:
            return 'WPA'
        elif 'wep' in enc_lower or 'wep' in full_text:
            return 'WEP'
        elif 'open' in enc_lower or 'none' in enc_lower:
            return 'Open'
        else:
            return 'Unknown'
    
    def display_networks_table(self):
        """Display discovered networks in a formatted table using tabulate."""
        if not self.access_points:
            print(f"{Fore.YELLOW}[!] No networks found{Style.RESET_ALL}")
            return []
        
        # Prepare table data
        table_data = []
        ap_list = sorted(self.access_points.values(), key=lambda x: x.signal_strength, reverse=True)
        
        for i, ap in enumerate(ap_list, 1):
            table_data.append([
                i,  # Number
                ap.ssid[:20] if len(ap.ssid) <= 20 else ap.ssid[:17] + '...',  # ESSID (truncated)
                ap.channel,  # CH
                ap.get_encryption_display(),  # ENC
                ap.signal_strength,  # POWER
                ap.get_wps_status(),  # WPS
                ap.client_count  # Clients
            ])
        
        # Display table
        headers = ['#', 'ESSID', 'CH', 'ENC', 'POWER', 'WPS', 'Clients']
        print(f"\n{Fore.CYAN}{tabulate(table_data, headers=headers, tablefmt='grid')}{Style.RESET_ALL}\n")
        
        return ap_list
    
    def get_ap_by_index(self, index: int):
        """Get access point by table index (1-based)."""
        ap_list = sorted(self.access_points.values(), key=lambda x: x.signal_strength, reverse=True)
        if 1 <= index <= len(ap_list):
            return ap_list[index - 1]
        return None
