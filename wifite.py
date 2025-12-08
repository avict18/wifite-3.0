#!/usr/bin/env python3
"""
Wifite - Automated Wi-Fi Auditing Framework
Simplified professional tool for wireless security assessments.

DISCLAIMER: For authorized security testing and educational purposes only.
"""

import os
import sys
import signal
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Import core modules
from core.interface import InterfaceManager
from core.scanner import NetworkScanner
from core.handshake import HandshakeCapture

logo = '''
▄   ▄ ▄ ▗▞▀▀▘▄ ▗▄▄▄▖▗▞▀▚▖
█ ▄ █ ▄ ▐▌   ▄   █  ▐▛▀▀▘
█▄█▄█ █ ▐▛▀▘ █   █  ▝▚▄▄▖
      █ ▐▌   █   █       
                         
                         
WIFITE 3.0 - Automated Wi-Fi Auditing Framework
    by: avict18
'''

class WifiteFramework:
    """Main framework for Wi-Fi auditing."""
    
    def __init__(self):
        self.interface_manager = InterfaceManager()
        self.scanner = None
        self.handshake_capture = None
        self.monitor_interface = None
        
        # Setup signal handlers for cleanup
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle cleanup on interrupt."""
        print(f"\n{Fore.YELLOW}[!] Interrupted. Cleaning up...{Style.RESET_ALL}")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Cleanup resources."""
        if self.handshake_capture:
            self.handshake_capture._stop_capture()
    
    def display_menu(self):
        """Display main menu."""
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Fore.CYAN + logo + Style.RESET_ALL)
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}MAIN MENU{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}1. Handshake Capturing{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Captive Portal (Evil Twin) - Coming Soon{Style.RESET_ALL}")
        print(f"{Fore.WHITE}0. Exit{Style.RESET_ALL}\n")
    
    def handshake_capturing_workflow(self):
        """Complete handshake capturing workflow."""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}HANDSHAKE CAPTURING{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Step 1: Interface selection and preparation
        print(f"{Fore.YELLOW}[*] Step 1: Interface Preparation{Style.RESET_ALL}")
        monitor_iface = self.interface_manager.select_and_prepare_interface()
        
        if not monitor_iface:
            print(f"{Fore.RED}[-] Failed to prepare interface{Style.RESET_ALL}")
            return
        
        self.monitor_interface = monitor_iface
        
        # Step 2: Initialize scanner and handshake capture
        self.scanner = NetworkScanner(monitor_iface)
        self.handshake_capture = HandshakeCapture(monitor_iface)
        
        # Step 3: Scan for networks
        print(f"\n{Fore.YELLOW}[*] Step 2: Scanning for networks...{Style.RESET_ALL}")
        access_points = self.scanner.scan_networks(duration=5)
        
        if not access_points:
            print(f"{Fore.RED}[-] No networks found{Style.RESET_ALL}")
            return
        
        # Step 4: Display networks and select target
        print(f"{Fore.YELLOW}[*] Step 3: Select target network{Style.RESET_ALL}")
        ap_list = self.scanner.display_networks_table()
        
        try:
            choice = input(f"\n{Fore.YELLOW}Select target by number (1-{len(ap_list)}): {Style.RESET_ALL}").strip()
            target_idx = int(choice) - 1
            
            if 0 <= target_idx < len(ap_list):
                target = ap_list[target_idx]
                
                # Step 5: Capture handshake and auto-crack
                print(f"\n{Fore.YELLOW}[*] Step 4: Capturing handshake and cracking...{Style.RESET_ALL}")
                self.handshake_capture.capture_handshake_with_deauth(target)
                
            else:
                print(f"{Fore.RED}[-] Invalid selection{Style.RESET_ALL}")
        
        except (ValueError, KeyboardInterrupt):
            print(f"\n{Fore.YELLOW}[!] Cancelled{Style.RESET_ALL}")
    
    def run(self):
        """Main execution loop."""
        try:
            while True:
                self.display_menu()
                choice = input(f"{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.handshake_capturing_workflow()
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
                elif choice == '2':
                    print(f"\n{Fore.CYAN}[*] Captive Portal (Evil Twin) feature coming soon!{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
                elif choice == '0':
                    print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                    self.cleanup()
                    break
                
                else:
                    print(f"{Fore.RED}[-] Invalid option{Style.RESET_ALL}")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
            self.cleanup()

def main():
    """Entry point."""
    # Check for root privileges
    if os.geteuid() != 0:
        print(f"{Fore.RED}[-] This tool requires root privileges. Please run with sudo.{Style.RESET_ALL}")
        sys.exit(1)
    
    framework = WifiteFramework()
    framework.run()

if __name__ == '__main__':
    main()
