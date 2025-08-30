# 🐝 Honeypot Project

A high-interaction honeypot designed to detect, log, and analyze malicious activity in a controlled environment.  
This project is built on Kali Linux and configured to mimic vulnerable services while capturing attacker behavior.

---

## 📖 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Setup](#-setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Security Notes](#-security-notes)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features
- Logs suspicious network activity (IP, timestamp, payload).
- Simulates vulnerable services (SSH, HTTP, etc.).
- Stores logs in structured files for later analysis.
- Extensible design for adding more traps and services.

---

## 🏗 Architecture
```text
+------------------+      +------------------+
|     Attacker     | <--> | Honeypot Service |
+------------------+      +------------------+
           |                       |
           v                       v
     +---------------+      +------------------+
     |   Log Files   | ---> |  Analysis Tools  |
     +---------------+      +------------------+
```
⚙️ Setup
1. Clone the repo
```bash

git clone git@github.com:ZEESHANAHMED-07/Honeypot.git
cd Honeypot
```


2. Create and activate a virtual environment
```bash

python3 -m venv .venv
source .venv/bin/activate
```


3. Install dependencies
```bash

pip install -r requirements.txt
```

4. Configure your honeypot

Logs are stored in the logs/ directory.

SSH keys remain local only inside keys/ (not pushed to GitHub).

Update src/config.py (if provided) to set ports, services, etc.

