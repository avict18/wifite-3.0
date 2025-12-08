"""
Offline Password Testing Module
Performs wordlist-based password cracking on captured handshakes.
"""

import subprocess
import os
import re
from pathlib import Path
from typing import Optional
from colorama import Fore, Style

class PasswordCracker:
    """Performs offline password cracking on handshake files."""
    
    def __init__(self, wordlist_path: Optional[str] = None):
        self.wordlist_path = wordlist_path or self._find_default_wordlist()
        self.cracked_password = None
    
    def _find_default_wordlist(self) -> Optional[str]:
        """Find common wordlist locations."""
        common_paths = [
            './wordlists/avict.txt',  # Project-specific wordlist (203K+ passwords)
            './wordlists/rockyou.txt',
            '/usr/share/wordlists/rockyou.txt',
            '/usr/share/wordlists/rockyou.txt.gz',
            '/usr/share/john/password.lst',
            '/usr/share/dict/words',
            './wordlist.txt',
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def crack_handshake(self, handshake_file: Path, wordlist: Optional[str] = None, 
                       use_hashcat: bool = False) -> Optional[str]:
        """
        Crack password from handshake file using wordlist.
        
        Args:
            handshake_file: Path to .cap handshake file
            wordlist: Path to wordlist file (uses default if None)
            use_hashcat: Use hashcat instead of aircrack-ng
        
        Returns:
            Cracked password or None
        """
        wordlist = wordlist or self.wordlist_path
        
        if not wordlist or not os.path.exists(wordlist):
            print(f"{Fore.RED}[-] Wordlist not found: {wordlist}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Please specify a wordlist with --wordlist option{Style.RESET_ALL}")
            return None
        
        if not handshake_file.exists():
            print(f"{Fore.RED}[-] Handshake file not found: {handshake_file}{Style.RESET_ALL}")
            return None
        
        print(f"\n{Fore.CYAN}[*] Starting offline password cracking...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Handshake: {handshake_file}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Wordlist: {wordlist}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This may take a while...{Style.RESET_ALL}\n")
        
        if use_hashcat:
            return self._crack_with_hashcat(handshake_file, wordlist)
        else:
            return self._crack_with_aircrack(handshake_file, wordlist)
    
    def _crack_with_aircrack(self, handshake_file: Path, wordlist: str) -> Optional[str]:
        """Crack using aircrack-ng."""
        try:
            cmd = [
                'sudo', 'aircrack-ng',
                '-w', wordlist,
                '-b', self._extract_bssid_from_file(handshake_file) or '',
                str(handshake_file)
            ]
            
            # Remove empty BSSID if extraction failed
            if not cmd[4]:
                cmd = [c for c in cmd if c != '-b' and c != '']
            
            print(f"{Fore.CYAN}[*] Running: {' '.join(cmd)}{Style.RESET_ALL}\n")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor output for password
            for line in process.stdout:
                print(line, end='')
                if 'KEY FOUND!' in line.upper():
                    # Extract password
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.upper() == 'FOUND!':
                            if i + 1 < len(parts):
                                password = parts[i + 1].strip('[]')
                                self.cracked_password = password
                                process.terminate()
                                return password
            
            process.wait()
            
            # Check stderr for errors
            stderr_output = process.stderr.read() if process.stderr else ''
            if '0 handshake' in stderr_output.lower():
                print(f"{Fore.RED}[-] No valid handshake in capture file{Style.RESET_ALL}")
            
            return None
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Cracking interrupted by user{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[-] Error during cracking: {e}{Style.RESET_ALL}")
            return None
    
    def _crack_with_hashcat(self, handshake_file: Path, wordlist: str) -> Optional[str]:
        """Crack using hashcat (requires .hccapx conversion)."""
        try:
            # Convert .cap to .hccapx using cap2hccapx
            hccapx_file = handshake_file.with_suffix('.hccapx')
            
            print(f"{Fore.CYAN}[*] Converting handshake to hashcat format...{Style.RESET_ALL}")
            result = subprocess.run(
                ['cap2hccapx', str(handshake_file), str(hccapx_file)],
                capture_output=True,
                text=True,
                check=False
            )
            
            if not hccapx_file.exists():
                print(f"{Fore.RED}[-] Failed to convert handshake format{Style.RESET_ALL}")
                return None
            
            # Run hashcat
            cmd = [
                'hashcat',
                '-m', '2500',  # WPA/WPA2 mode
                '-a', '0',     # Dictionary attack
                str(hccapx_file),
                wordlist
            ]
            
            print(f"{Fore.CYAN}[*] Running hashcat...{Style.RESET_ALL}\n")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            # Parse hashcat output
            if result.returncode == 0:
                # Password found
                lines = result.stdout.split('\n')
                for line in lines:
                    if hccapx_file.name in line:
                        # Extract password (format varies)
                        parts = line.split(':')
                        if len(parts) > 1:
                            password = parts[-1].strip()
                            self.cracked_password = password
                            return password
            
            return None
            
        except FileNotFoundError:
            print(f"{Fore.RED}[-] hashcat or cap2hccapx not found. Falling back to aircrack-ng{Style.RESET_ALL}")
            return self._crack_with_aircrack(handshake_file, wordlist)
        except Exception as e:
            print(f"{Fore.RED}[-] Error with hashcat: {e}{Style.RESET_ALL}")
            return None
    
    def _extract_bssid_from_file(self, handshake_file: Path) -> Optional[str]:
        """Extract BSSID from handshake file using aircrack-ng."""
        try:
            result = subprocess.run(
                ['aircrack-ng', str(handshake_file)],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            
            # Parse BSSID from output
            for line in result.stdout.split('\n'):
                if 'BSSID' in line or re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', line):
                    match = re.search(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', line)
                    if match:
                        return match.group(0)
            
            return None
        except Exception:
            return None

