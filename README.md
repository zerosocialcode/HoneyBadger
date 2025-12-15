HoneyBadger 🦡
​"Honey badger don't care. Honey badger takes what it wants."
​HoneyBadger is a high-performance, multi-threaded access audit and recovery tool designed for security professionals and researchers. It automates the process of validating credentials against Instagram's authentication endpoints with robust session management, device emulation, and smart proxy rotation.
​Built for speed, stability, and stealth.
​⚡ Key Features
​Multi-Threaded Engine: Utilizes ThreadPoolExecutor for concurrent auditing, maximizing throughput without locking the UI.
​Smart Device Emulation: Spoofs a legit Samsung Galaxy S9 (Android 8.0) fingerprint to mitigate immediate flagging.
​Encrypted Session Management: Automatically saves and encrypts valid sessions using Fernet (cryptography), allowing for persistent access without re-login.
​Advanced Error Handling: Intelligently detects and categorizes responses:
​SUCCESS - Valid credentials.
​CHALLENGE - 2FA or Checkpoint required.
​BLOCKED - IP or Action bans.
​RATELIMIT - API throttling detection.
​Live UI Dashboard: Clean, color-coded terminal interface with real-time status updates (powered by colorama).
​Proxy Rotation: Supports rotating proxy lists to prevent IP bans during bulk audits.
​🛠️ Installation
