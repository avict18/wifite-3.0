"""
Interface Preparation Module
Handles wireless adapter detection, monitor mode checking, and enabling monitor mode.
"""

import subprocess
import re
import os
from colorama import Fore, Style

class InterfaceManager:
    """Manages wireless network interface operations."""
    
    def __init__(self):
        self.interface = None
        self.monitor_interface = None
    
    def detect_all_interfaces(self):
        """
        Detect all available wireless interfaces (both managed and monitor mode).
        Returns list of tuples: (interface_name, mode, is_monitor)
        """
        interfaces = []
        
        try:
            # Method 1: Use iwconfig to get all interfaces
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=False)
            
            for line in result.stdout.split('\n'):
                # Skip empty lines and headers
                if not line.strip() or 'lo' in line:
                    continue
                
                # Extract interface name (first word)
                match = re.search(r'^(\w+)\s+', line)
                if match:
                    iface = match.group(1)
                    
                    # Get mode
                    mode = self.get_interface_mode(iface)
                    is_monitor = (mode == 'monitor')
                    
                    # Check if it's a wireless interface
                    if 'IEEE 802.11' in line or 'no wireless extensions' not in line.lower():
                        if iface not in [i[0] for i in interfaces]:
                            interfaces.append((iface, mode, is_monitor))
            
            # Method 2: Check /sys/class/net for wireless interfaces
            if not interfaces:
                try:
                    net_dir = '/sys/class/net'
                    for item in os.listdir(net_dir):
                        if item == 'lo':
                            continue
                        wireless_path = os.path.join(net_dir, item, 'wireless')
                        if os.path.exists(wireless_path):
                            mode = self.get_interface_mode(item)
                            is_monitor = (mode == 'monitor')
                            if (item, mode, is_monitor) not in interfaces:
                                interfaces.append((item, mode, is_monitor))
                except Exception:
                    pass
            
            return interfaces
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error detecting interfaces: {e}{Style.RESET_ALL}")
            return []
    
    def get_interface_mode(self, interface):
        """Get current mode of the interface (managed/monitor/etc)."""
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True, check=False)
            match = re.search(r'Mode:(\w+)', result.stdout)
            if match:
                return match.group(1).lower()
            return 'unknown'
        except Exception:
            return 'unknown'
    
    def prepare_interface_with_airmon(self, interface):
        """
        Prepare interface using airmon-ng.
        Returns the monitor interface name (may be different from input if airmon-ng creates mon0, etc.)
        """
        try:
            # Check if already in monitor mode
            current_mode = self.get_interface_mode(interface)
            if current_mode == 'monitor':
                print(f"{Fore.GREEN}[+] Interface {interface} already in monitor mode{Style.RESET_ALL}")
                self.interface = interface
                self.monitor_interface = interface
                return interface
            
            # Kill interfering processes
            print(f"{Fore.YELLOW}[*] Killing interfering processes...{Style.RESET_ALL}")
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], capture_output=True, check=False)
            
            # Use airmon-ng to start monitor mode
            print(f"{Fore.YELLOW}[*] Starting monitor mode on {interface}...{Style.RESET_ALL}")
            result = subprocess.run(
                ['sudo', 'airmon-ng', 'start', interface],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse airmon-ng output to find monitor interface
            output = result.stdout + result.stderr
            
            # Look for "monitor mode enabled on (interface)"
            match = re.search(r'\(monitor mode enabled on (\w+)\)', output, re.IGNORECASE)
            if match:
                monitor_iface = match.group(1)
                print(f"{Fore.GREEN}[+] Monitor mode enabled on {monitor_iface}{Style.RESET_ALL}")
                self.interface = interface
                self.monitor_interface = monitor_iface
                return monitor_iface
            
            # Alternative: airmon-ng might create mon0, mon1, etc.
            # Check if interface name changed (e.g., wlan0 -> wlan0mon)
            if 'monitor mode enabled' in output.lower():
                # Try to find the new interface name
                # Common patterns: wlan0 -> wlan0mon, or creates mon0
                possible_names = [f"{interface}mon", f"mon{interface[-1] if interface[-1].isdigit() else '0'}"]
                
                for name in possible_names:
                    if self.get_interface_mode(name) == 'monitor':
                        print(f"{Fore.GREEN}[+] Monitor mode enabled on {name}{Style.RESET_ALL}")
                        self.interface = interface
                        self.monitor_interface = name
                        return name
                
                # If we can't find it, assume the original interface is now in monitor mode
                if self.get_interface_mode(interface) == 'monitor':
                    self.interface = interface
                    self.monitor_interface = interface
                    return interface
            
            print(f"{Fore.RED}[-] Failed to enable monitor mode{Style.RESET_ALL}")
            return None
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error preparing interface: {e}{Style.RESET_ALL}")
            return None
    
    def select_and_prepare_interface(self):
        """
        Interactive interface selection and preparation.
        Shows all available interfaces and lets user select one.
        If interface is already in monitor mode, skips preparation.
        Returns the monitor interface name.
        """
        # Detect all interfaces
        all_interfaces = self.detect_all_interfaces()
        
        if not all_interfaces:
            print(f"{Fore.RED}[-] No wireless interfaces detected!{Style.RESET_ALL}")
            return None
        
        # Display interfaces
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Available Interfaces:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'#':<4} {'Interface':<15} {'Mode':<12} {'Status'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
        
        for i, (iface, mode, is_monitor) in enumerate(all_interfaces, 1):
            status = f"{Fore.GREEN}Monitor Ready{Style.RESET_ALL}" if is_monitor else f"{Fore.YELLOW}Managed{Style.RESET_ALL}"
            print(f"{Fore.WHITE}{i:<4} {iface:<15} {mode:<12} {status}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # User selection
        try:
            choice = input(f"{Fore.YELLOW}Select interface by number (1-{len(all_interfaces)}): {Style.RESET_ALL}").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(all_interfaces):
                selected_iface, selected_mode, is_monitor = all_interfaces[idx]
                
                # If already in monitor mode, return it
                if is_monitor:
                    print(f"{Fore.GREEN}[+] Using {selected_iface} (already in monitor mode){Style.RESET_ALL}")
                    self.interface = selected_iface
                    self.monitor_interface = selected_iface
                    return selected_iface
                
                # Otherwise, prepare it
                return self.prepare_interface_with_airmon(selected_iface)
            else:
                print(f"{Fore.RED}[-] Invalid selection{Style.RESET_ALL}")
                return None
                
        except (ValueError, KeyboardInterrupt):
            return None
