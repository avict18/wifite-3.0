
'''
Wifite is a Python-based tool that scans for nearby Wi-Fi networks and attempts to crack their passwords using various methods. This tool is designed for educational purposes only and should not be used to illegally access or compromise Wi-Fi networks.
'''

import os
import pyfiglet
from colorama import Fore, Style

lines = '-'*30+'>'
result = "#please wait...\n"
logo = pyfiglet.figlet_format('wifite')

def main():
    while True:
        print(Fore.GREEN+logo)
        print(Style.RESET_ALL)
        print('V1.0'+'                    '+Fore.RED+'by Avict\n'+Fore.RESET)
        print("1. Scan for nearby networks")
        print("2. Crack WEP/WPA/WPA2 networks")
        print("3. Quit")
        choice = input('Place ur choice: ')
        print('\n')
        match choice:
            case '1':
                os.system('python3 scan.py')
            case '2':
                os.system('python3 crack.py')
            case '3':
                print('Goodbye!\n'+Fore.CYAN+'GitHub by Avict'+Fore.RESET)
                break    
            

if __name__ == '__main__':
    main()