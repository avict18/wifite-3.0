# 🔥 WiFite 3.0 - Automated Wi-Fi Auditing Framework

<div align="center">

```
▄   ▄ ▄ ▗▞▀▀▘▄ ▗▄▄▄▖▗▞▀▚▖
█ ▄ █ ▄ ▐▌   ▄   █  ▐▛▀▀▘
█▄█▄█ █ ▐▛▀▘ █   █  ▝▚▄▄▖
      █ ▐▌   █   █       
```

**Professional Wi-Fi Security Assessment Tool**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPLv3-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**by: avict18**

</div>

---

## ⚠️ **IMPORTANT DISCLAIMER**

> **This tool is for EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.**
> 
> Unauthorized access to computer networks is illegal. Use this tool only on networks you own or have explicit written permission to test. The developers assume NO liability for misuse of this software.

---

## 📖 Overview

**WiFite 3.0** is a streamlined, automated Wi-Fi auditing framework designed for authorized wireless security assessments. It automates the complete workflow of:

1. **Interface Preparation** - Automatic monitor mode setup
2. **Network Scanning** - Multi-channel AP discovery with detailed information
3. **Handshake Capture** - Active deauthentication and packet capture
4. **Automatic Cracking** - Offline password testing with wordlists

The framework orchestrates established tools (Aircrack-NG Suite) and provides a clean, menu-driven interface for security professionals.

---

## ✨ Features

### 🔧 **Core Capabilities**

- **Automatic Interface Management**
  - Detects all wireless interfaces (managed and monitor mode)
  - Automatically prepares interfaces using `airmon-ng`
  - Skips preparation if interface is already in monitor mode
  - Supports multiple interfaces (wlan0, mon0, etc.)

- **Comprehensive Network Scanning**
  - Multi-channel scanning (2.4GHz and 5GHz)
  - Displays networks in formatted table with:
    - ESSID (Network name)
    - Channel (CH)
    - Encryption type (ENC)
    - Signal strength (POWER)
    - WPS status (Yes/No)
    - Number of connected clients

- **Handshake Capture & Auto-Cracking**
  - Active deauthentication attacks
  - Automatic handshake validation
  - **Automatic password cracking** when handshake is captured
  - Stores handshakes in `./avict_hs/` folder
  - Uses default wordlist: `wordlists/avict.txt` (203K+ passwords)

- **Clean Menu System**
  - Simple, intuitive interface
  - Option 1: Handshake Capturing (fully functional)
  - Option 2: Captive Portal (Evil Twin) - Coming Soon
  - Option 0: Exit

---

## 📦 Installation

### Prerequisites

- **Linux** (Kali Linux recommended)
- **Python 3.7+**
- **Root/sudo privileges**
- **Aircrack-NG Suite** installed:
  ```bash
  sudo apt-get update
  sudo apt-get install aircrack-ng
  ```
- **Wireless adapter** supporting monitor mode and packet injection

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/avict18/wifite-3.0.git
cd wifite-3.0

# Install Python dependencies
pip install -r requirements.txt

# Run with sudo (required for monitor mode)
sudo python3 wifite.py
```

### Dependencies

The following Python packages are required (automatically installed via `requirements.txt`):

- `colorama` - Terminal colors
- `pyfiglet` - ASCII art
- `tabulate` - Table formatting

---

## 🚀 Usage

### Basic Workflow

1. **Start the framework:**
   ```bash
   sudo python3 wifite.py
   ```

2. **Select Option 1: Handshake Capturing**

3. **Interface Selection:**
   - Framework displays all available interfaces
   - Shows current mode (managed/monitor) and status
   - Select interface by number
   - If already in monitor mode, skips preparation
   - Otherwise, uses `airmon-ng` to prepare interface

4. **Network Scanning:**
   - Automatically scans all channels
   - Displays networks in formatted table
   - Shows: #, ESSID, CH, ENC, POWER, WPS, Clients

5. **Target Selection:**
   - Select target network by number
   - Framework automatically:
     - Locks to target channel
     - Sends deauthentication packets
     - Captures handshake
     - **Starts automatic password cracking**

6. **Results:**
   - If password found: Displays password immediately
   - Handshake saved in `./avict_hs/` folder
   - Can be used for offline cracking later

---

## 📁 Project Structure

```
wifite-3.0/
├── wifite.py              # Main framework and menu system
├── core/                  # Core modules
│   ├── __init__.py
│   ├── interface.py      # Interface detection and preparation
│   ├── scanner.py        # Network scanning with tabulate display
│   ├── handshake.py      # Handshake capture + auto-cracking
│   └── cracker.py        # Password cracking engine
├── wordlists/
│   └── avict.txt         # Default wordlist (203K+ passwords)
├── avict_hs/             # Captured handshake files (auto-created)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔍 Workflow Details

### Stage 1: Interface Preparation

- **Detects all interfaces** using `iwconfig` and `/sys/class/net`
- **Shows interface table** with mode and status
- **Checks if already in monitor mode** → skips if ready
- **Uses `airmon-ng`** to prepare interface if needed
- **Handles multiple interfaces** (wlan0, mon0, wlan1, etc.)

### Stage 2: Network Scanning

- **Multi-channel scan** using `airodump-ng`
- Scans 2.4GHz (channels 1-11) and 5GHz (36, 40, 44, 48, 149, 153, 157, 161, 165)
- **Parses CSV output** to extract:
  - SSID, BSSID, Channel
  - Signal strength (dBm)
  - Encryption type (WEP/WPA/WPA2/WPA3)
  - WPS status
  - Client count

### Stage 3: Handshake Capture

- **Locks interface** to target channel
- **Sends deauthentication packets** to force client reconnection
- **Captures EAPOL frames** using `airodump-ng`
- **Validates handshake** using `aircrack-ng`
- **Stores capture file** in `./avict_hs/` folder

### Stage 4: Automatic Cracking

- **Automatically starts** when handshake is captured
- **Uses default wordlist**: `wordlists/avict.txt`
- **Offline password testing** using `aircrack-ng`
- **No network interaction** during cracking
- **Displays password** if found, or saves handshake for later

---

## 🛠️ Technical Details

### Handshake Capture Method

The framework uses **active deauthentication** technique:

1. Starts background packet capture (`airodump-ng`)
2. Sends deauth packets to connected clients
3. Clients automatically reconnect
4. EAPOL handshake occurs during reconnection
5. Handshake is captured and validated

### Offline Cracking Process

All password testing is **completely offline**:

1. Uses captured handshake file (`.cap` format)
2. Tests passwords from wordlist
3. Cryptographic verification:
   - Derives PMK from candidate password
   - Computes MIC (Message Integrity Code)
   - Compares with captured MIC
   - Match = password found

### Wordlist

Default wordlist: `wordlists/avict.txt`
- **203,808 passwords**
- **2.02 MB**
- Automatically detected and used
- Can specify custom wordlist if needed

---

## 📊 Example Output

```
┌─────┬──────────────────────┬─────┬──────┬───────┬─────┬─────────┐
│  #  │       ESSID         │ CH  │ ENC  │ POWER │ WPS │ Clients │
├─────┼──────────────────────┼─────┼──────┼───────┼─────┼─────────┤
│  1  │ MyNetwork           │  6  │ WPA2 │  -45  │ No  │    2    │
│  2  │ Office_WiFi         │ 11  │ WPA2 │  -67  │ Yes │    5    │
│  3  │ Guest_Network       │  1  │ Open │  -78  │ No  │    0    │
└─────┴──────────────────────┴─────┴──────┴───────┴─────┴─────────┘
```

---

## ⚙️ Configuration

### Custom Wordlist

The framework automatically uses `wordlists/avict.txt` as default. To use a different wordlist:

1. Place your wordlist file in the project directory
2. The framework will prompt for wordlist path during cracking
3. Or modify `core/cracker.py` to change default path

### Handshake Storage

All captured handshakes are stored in:
- **Directory**: `./avict_hs/`
- **Format**: `.cap` files
- **Naming**: `{SSID}_{BSSID}_{timestamp}.cap`

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- 🔧 Bug fixes and performance improvements
- 📊 Additional attack methods
- 🎨 UI/UX enhancements
- 📚 Documentation improvements
- 🧪 Testing and validation

---

## 👥 Contributors

- **avict18** - Project Lead & Developer
- **MrpasswordTz** - Core Developer

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.

See the [LICENSE](LICENSE) file for details.

---

## ⚠️ Legal & Ethical Guidelines

### ✅ Permitted Uses

- Security research and education
- Authorized penetration testing
- Network security assessments (with written permission)
- Academic study of wireless security

### ❌ Strictly Prohibited

- Unauthorized network access
- Illegal surveillance
- Commercial exploitation without permission
- Any activity violating local laws

**The developers assume NO liability for misuse of this software.**

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/avict18/wifite-3.0/issues)
- **Repository**: [GitHub Repository](https://github.com/avict18/wifite-3.0)

---

<div align="center">

**"Knowledge is power. Use it responsibly."**

🚧 **Under Active Development** 🚧

</div>
