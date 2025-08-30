🐝 Honeypot Project

A high-interaction honeypot designed to detect, log, and analyze malicious activity in a controlled environment.
This project is built on Kali Linux and configured to mimic vulnerable services while capturing attacker behavior.

📖 Table of Contents

Features

Architecture

Setup

Usage

Project Structure

Security Notes

Contributing

License

✨ Features

Logs suspicious network activity (IP, timestamp, payload).

Simulates vulnerable services (SSH, HTTP, etc.).

Stores logs in structured files for later analysis.

Extensible design for adding more traps and services.

🏗 Architecture
+------------------+        +------------------+
|   Attacker       | <----> | Honeypot Service |
+------------------+        +------------------+
                                   |
                                   v
                           +---------------+
                           |   Log Files   |
                           +---------------+
                                   |
                                   v
                           +------------------+
                           | Analysis Tools   |
                           +------------------+

⚙️ Setup
1. Clone the repo

git clone git@github.com:ZEESHANAHMED-07/Honeypot.git
cd Honeypot

2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure your honeypot

Logs are stored in the logs/ directory.

SSH keys remain local only inside keys/ (not pushed to GitHub).

Update src/config.py (if provided) to set ports, services, etc.

▶️ Usage

Run the honeypot:

python src/honeypot.py


Logs will be generated under:

logs/

📂 Project Structure
Honeypot/
├── src/            # Honeypot source code
├── logs/           # Attack logs (ignored in Git)
├── keys/           # Local SSH keys (ignored in Git)
├── .gitignore      # Ignore sensitive files
├── README.md       # Project documentation
└── requirements.txt

🔒 Security Notes

⚠️ Important:

Run this only in a controlled environment (VM, VPS).

Never expose sensitive logs or private keys publicly.

Use for research and educational purposes only.

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your idea.

📜 License

MIT
