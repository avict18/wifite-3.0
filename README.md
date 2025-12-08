<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFite 3.0 - Advanced Wi-Fi Security Auditing Tool</title>
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f4c75;
            --highlight: #00adb5;
            --text: #eeeeee;
            --danger: #ff2e63;
            --warning: #ff9a00;
            --success: #00ffab;
            --code-bg: #0d1117;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--highlight), var(--success));
        }
        
        .logo {
            font-size: 3.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, var(--highlight), var(--success));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 173, 181, 0.3);
        }
        
        .tagline {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .warning-banner {
            background: linear-gradient(45deg, var(--danger), var(--warning));
            padding: 15px;
            border-radius: 10px;
            margin: 20px auto;
            max-width: 800px;
            text-align: center;
            border-left: 5px solid var(--danger);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 46, 99, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255, 46, 99, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 46, 99, 0); }
        }
        
        section {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        h2 {
            color: var(--highlight);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        h2::before {
            content: '▶';
            font-size: 0.8em;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .feature-card {
            background: rgba(15, 76, 117, 0.2);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(0, 173, 181, 0.2);
            transition: transform 0.3s, border-color 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: var(--highlight);
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .feature-card h3 {
            color: var(--success);
            margin-bottom: 10px;
        }
        
        .code-block {
            background: var(--code-bg);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            overflow-x: auto;
            border-left: 4px solid var(--highlight);
        }
        
        .code-block code {
            font-family: 'Courier New', monospace;
            color: var(--success);
        }
        
        .command {
            color: var(--highlight);
            font-weight: bold;
        }
        
        .comment {
            color: #6e7681;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            overflow: hidden;
        }
        
        th {
            background: var(--accent);
            padding: 15px;
            text-align: left;
            color: var(--highlight);
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        tr:hover {
            background: rgba(0, 173, 181, 0.1);
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            margin: 0 5px;
        }
        
        .badge-danger { background: var(--danger); }
        .badge-warning { background: var(--warning); color: #000; }
        .badge-success { background: var(--success); color: #000; }
        .badge-info { background: var(--highlight); }
        
        .contributors {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }
        
        .contributor-card {
            text-align: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            width: 150px;
        }
        
        .contributor-card img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin-bottom: 10px;
            border: 3px solid var(--highlight);
        }
        
        .status-bar {
            display: flex;
            align-items: center;
            gap: 20px;
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--success);
            animation: blink 2s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        footer {
            text-align: center;
            padding: 30px;
            margin-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .social-badges {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }
        
        .social-badge {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            transition: background 0.3s;
        }
        
        .social-badge:hover {
            background: rgba(0, 173, 181, 0.3);
        }
        
        .highlight {
            color: var(--highlight);
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            section {
                padding: 20px;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .logo {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="logo">🔥 WiFite 3.0</h1>
            <p class="tagline">Advanced Wi-Fi Security Auditing Tool</p>
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-indicator"></div>
                    <span>Version: 3.0 (Development)</span>
                </div>
                <div class="status-item">
                    <div class="status-indicator"></div>
                    <span>Python: 3.8+</span>
                </div>
                <div class="status-item">
                    <div class="status-indicator"></div>
                    <span>Status: Active Development</span>
                </div>
            </div>
        </header>
        
        <div class="warning-banner">
            <strong>⚠️ WARNING:</strong> This tool is for <span class="highlight">EDUCATIONAL PURPOSES ONLY</span> and should only be used on networks you own or have explicit permission to test.
        </div>
        
        <section>
            <h2>📖 Overview</h2>
            <p><strong>WiFite 3.0</strong> is a powerful, Python-based Wi-Fi security auditing tool designed for <span class="highlight">educational and authorized penetration testing purposes</span>. It automates the process of scanning, attacking, and cracking Wi-Fi networks while providing an intuitive interface for security professionals and researchers.</p>
        </section>
        
        <section>
            <h2>✨ Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <h3>Network Discovery</h3>
                    <ul>
                        <li>Scan and display all nearby Wi-Fi networks</li>
                        <li>Show detailed information (SSID, BSSID, Channel)</li>
                        <li>Filter targets by signal strength or encryption</li>
                        <li>Real-time signal monitoring</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <h3>Encryption Support</h3>
                    <ul>
                        <li><span class="highlight">WEP</span> cracking via ARP replay attacks</li>
                        <li><span class="highlight">WPA/WPA2</span> handshake capture</li>
                        <li><span class="highlight">WPS</span> PIN attacks</li>
                        <li>PMKID-based attacks</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Attack Methods</h3>
                    <ul>
                        <li>Dictionary attacks with custom wordlists</li>
                        <li>Brute-force pattern generation</li>
                        <li>Parallel multi-network attacks</li>
                        <li>Session saving and resuming</li>
                    </ul>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🛠️</div>
                    <h3>Technical Features</h3>
                    <ul>
                        <li>Multiple wireless interface support</li>
                        <li>Background attack automation</li>
                        <li>Real-time status monitoring</li>
                        <li>Verbose logging and debugging</li>
                    </ul>
                </div>
            </div>
        </section>
        
        <section>
            <h2>📦 Installation</h2>
            
            <h3>Prerequisites</h3>
            <div class="code-block">
                <code>
                    <span class="command"># Ensure Python 3.8+ is installed</span><br>
                    python3 --version<br><br>
                    
                    <span class="command"># Install system dependencies (Debian/Ubuntu)</span><br>
                    sudo apt update<br>
                    sudo apt install python3-pip aircrack-ng tshark reaver bully hcxdumptool hcxtools<br>
                </code>
            </div>
            
            <h3>Quick Installation</h3>
            <div class="code-block">
                <code>
                    <span class="command"># Clone the repository</span><br>
                    git clone https://github.com/avict18/wifite-3.0.git<br><br>
                    
                    <span class="command"># Navigate to project directory</span><br>
                    cd wifite-3.0<br><br>
                    
                    <span class="command"># Install Python dependencies</span><br>
                    pip install -r requirements.txt<br><br>
                    
                    <span class="command"># Make the script executable</span><br>
                    chmod +x wifite.py<br><br>
                    
                    <span class="command"># Run WiFite</span><br>
                    sudo python3 wifite.py<br>
                </code>
            </div>
            
            <h3>Docker Installation</h3>
            <div class="code-block">
                <code>
                    <span class="command"># Build Docker image</span><br>
                    docker build -t wifite3 .<br><br>
                    
                    <span class="command"># Run with network privileges</span><br>
                    docker run --net=host --privileged -it wifite3<br>
                </code>
            </div>
        </section>
        
        <section>
            <h2>🚀 Usage</h2>
            
            <h3>Basic Commands</h3>
            <div class="code-block">
                <code>
                    <span class="comment"># Basic scan</span><br>
                    sudo python3 wifite.py --scan<br><br>
                    
                    <span class="comment"># Target specific network</span><br>
                    sudo python3 wifite.py --target TARGET_BSSID --channel 6<br><br>
                    
                    <span class="comment"># WPA attack with custom wordlist</span><br>
                    sudo python3 wifite.py --wpa --dict /path/to/wordlist.txt<br><br>
                    
                    <span class="comment"># WPS PIN attack</span><br>
                    sudo python3 wifite.py --wps --bully<br>
                </code>
            </div>
            
            <h3>Common Flags</h3>
            <table>
                <thead>
                    <tr>
                        <th>Flag</th>
                        <th>Description</th>
                        <th>Example</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>--scan</code></td>
                        <td>Scan for networks only</td>
                        <td><span class="badge badge-info">Info</span></td>
                    </tr>
                    <tr>
                        <td><code>--target BSSID</code></td>
                        <td>Attack specific network</td>
                        <td><span class="badge badge-danger">Attack</span></td>
                    </tr>
                    <tr>
                        <td><code>--wpa</code></td>
                        <td>WPA/WPA2 attacks only</td>
                        <td><span class="badge badge-warning">WPA</span></td>
                    </tr>
                    <tr>
                        <td><code>--wep</code></td>
                        <td>WEP attacks only</td>
                        <td><span class="badge badge-warning">WEP</span></td>
                    </tr>
                    <tr>
                        <td><code>--wps</code></td>
                        <td>WPS PIN attacks</td>
                        <td><span class="badge badge-warning">WPS</span></td>
                    </tr>
                    <tr>
                        <td><code>--dict FILE</code></td>
                        <td>Custom dictionary file</td>
                        <td><span class="badge badge-info">Config</span></td>
                    </tr>
                    <tr>
                        <td><code>--verbose</code></td>
                        <td>Detailed output</td>
                        <td><span class="badge badge-info">Debug</span></td>
                    </tr>
                </tbody>
            </table>
        </section>
        
        <section>
            <h2>🏗️ Architecture</h2>
            <div class="code-block">
                <code>
                    wifite-3.0/<br>
                    ├── wifite.py              <span class="comment"># Main entry point</span><br>
                    ├── lib/                   <span class="comment"># Core modules</span><br>
                    │   ├── scanner.py        <span class="comment"># Network scanning</span><br>
                    │   ├── attacker.py       <span class="comment"># Attack orchestration</span><br>
                    │   ├── cracker.py        <span class="comment"># Password cracking</span><br>
                    │   └── utils.py          <span class="comment"># Helper functions</span><br>
                    ├── config/               <span class="comment"># Configuration files</span><br>
                    ├── wordlists/            <span class="comment"># Default dictionaries</span><br>
                    ├── outputs/              <span class="comment"># Capture files & logs</span><br>
                    ├── requirements.txt      <span class="comment"># Python dependencies</span><br>
                    └── README.md            <span class="comment"># Documentation</span><br>
                </code>
            </div>
        </section>
        
        <section>
            <h2>🤝 Contributing</h2>
            <p>We welcome contributions! Here's how you can help:</p>
            
            <h3>Development Setup</h3>
            <div class="code-block">
                <code>
                    <span class="command"># Install development dependencies</span><br>
                    pip install -r requirements-dev.txt<br><br>
                    
                    <span class="command"># Run tests</span><br>
                    python -m pytest tests/<br><br>
                    
                    <span class="command"># Code formatting</span><br>
                    black wifite.py lib/<br>
                </code>
            </div>
            
            <h3>Contribution Areas</h3>
            <ul>
                <li>🔧 Bug fixes and performance improvements</li>
                <li>📊 New attack vectors and techniques</li>
                <li>🎨 UI/UX enhancements</li>
                <li>📚 Documentation and examples</li>
                <li>🧪 Test coverage expansion</li>
                <li>🔌 Plugin system development</li>
            </ul>
        </section>
        
        <section>
            <h2>🌟 Contributors</h2>
            <div class="contributors">
                <div class="contributor-card">
                    <img src="https://github.com/avict18.png" alt="Avict">
                    <h4>Avict</h4>
                    <p>Project Lead</p>
                </div>
                <div class="contributor-card">
                    <img src="https://github.com/MrpasswordTz.png" alt="MrpasswordTz">
                    <h4>MrpasswordTz</h4>
                    <p>Core Developer</p>
                </div>
            </div>
        </section>
        
        <section>
            <h2>⚠️ Legal & Ethical Disclaimer</h2>
            <div class="warning-banner">
                <strong>IMPORTANT:</strong> This tool is for <span class="highlight">SECURITY RESEARCH ONLY</span>
            </div>
            
            <h3>✅ Permitted Uses</h3>
            <ul>
                <li>Security research and education</li>
                <li>Authorized penetration testing</li>
                <li>Network security assessments (with written permission)</li>
                <li>Academic study of wireless security</li>
            </ul>
            
            <h3>❌ Strictly Prohibited</h3>
            <ul>
                <li>Unauthorized network access</li>
                <li>Illegal surveillance</li>
                <li>Commercial exploitation without permission</li>
                <li>Any activity violating local laws</li>
            </ul>
            
            <p>The developers assume <strong>NO liability</strong> for misuse of this software. Users are solely responsible for complying with all applicable laws and regulations.</p>
        </section>
        
        <section>
            <h2>📄 License</h2>
            <p>This project is licensed under the <strong>GNU General Public License v3.0</strong></p>
            <div class="code-block">
                <code>
                    Copyright (C) 2024 WiFite 3.0 Contributors<br><br>
                    
                    This program is free software: you can redistribute it and/or modify<br>
                    it under the terms of the GNU General Public License as published by<br>
                    the Free Software Foundation, either version 3 of the License, or<br>
                    (at your option) any later version.<br><br>
                    
                    This program is distributed in the hope that it will be useful,<br>
                    but WITHOUT ANY WARRANTY; without even the implied warranty of<br>
                    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the<br>
                    GNU General Public License for more details.<br>
                </code>
            </div>
        </section>
        
        <footer>
            <div class="social-badges">
                <a href="https://github.com/avict18/wifite-3.0" class="social-badge">⭐ Star on GitHub</a>
                <a href="https://github.com/avict18/wifite-3.0/issues" class="social-badge">🐛 Report Issues</a>
                <a href="https://github.com/avict18/wifite-3.0/fork" class="social-badge">🔱 Fork Project</a>
            </div>
            
            <p style="margin-top: 20px; opacity: 0.8;">
                <strong>"Knowledge is power. Use it responsibly."</strong>
            </p>
            
            <div style="margin-top: 30px; font-size: 0.9em; opacity: 0.6;">
                <p>🚧 <strong>Under Construction</strong> — Regular updates with new features and improvements 🚧</p>
            </div>
        </footer>
    </div>
</body>
</html>