# HoneyBadger

**HoneyBadger** is a tool for security professionals to automate credential verification and Instagram account recovery audits. It helps researchers and red-teamers efficiently test large numbers of username/password combinations, supporting concurrent execution, encrypted session management, and proxy rotation.

---

## Features

- **Automated Credential Checking:**  
  Test Instagram username/password combinations automatically.
- **Bulk or Single-Target Modes:**  
  Check a single account or audit many in batch.
- **Proxy Support:**  
  Utilize IP rotation to reduce bans and rate limits.
- **Encrypted Session Management:**  
  Credentials and session settings are stored securely for efficiency and persistence.
- **Comprehensive Logging:**  
  All successful credentials and activity are logged.

---

## Intended Use

> **For authorized security testing and account recovery by legitimate operators only. Usage without explicit permission is strictly forbidden and may be illegal.**

---

## Installation & Setup

### Requirements

- Python 3.7+
- pip

Install dependencies:

```sh
pip install -r requirements.txt
```

---

## Usage

Run the tool:

```sh
python3 run.py
```

Prepare:
- **Usernames file:** One username per line.
- **Passwords file:** One password per line (required).
- **Proxies file (optional):** Each proxy as `ip:port` per line.

---

## Architecture & How it Works

- **Session Management:**  
  Uses strong encryption to securely store and reload login sessions for accounts, minimizing repeat logins and detection risk.
- **Attack Logic:**  
  Leverages [instagrapi](https://github.com/adw0rd/instagrapi) to simulate Instagram login, handle device emulation, and interpret all common responses (e.g., 2FA requests, rate limits).
- **Proxy Handling:**  
  Rotates proxies per attempt when provided.
- **Concurrent Processing:**  
  Runs multiple login attempts in parallel using Python threading.

---

## Output

- **Successful credentials:** Written to `logs/success.log`.
- **Audit and debug logs:** Written to `logs/honeybadger_debug.log`.

---

## Code Structure

```
.
├── run.py
├── requirements.txt
└── src/
     ├── app.py           # Audit logic and orchestration
     ├── core/
     │    ├── attack.py   # Instagram login and attack code
     │    └── session.py  # Encrypted session saving/loading
```

---

## License

[MIT License](LICENSE)  
© [zerosocialcode](https://github.com/zerosocialcode) and contributors.

---

## Disclaimer

This software is intended for lawful research and audit purposes only. By using HoneyBadger you agree to use it only on accounts and systems for which you have explicit authorization. The maintainers are not responsible for any misuse or damages arising from use of this tool.
```
