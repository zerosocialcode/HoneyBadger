# HoneyBadger (AVS)

**Version:** 3.0.0 (HoneyBadger Edition)
**Classification:** Security Assessment & Account Recovery
**License:** Proprietary / Authorized Use Only
**Slogan:** "Honey badger don’t care. Honey badger takes what it wants."

## Executive Summary
HoneyBadger (formerly Access Verification Suite) is an aggressive, specialized Python-based auditing framework designed for authorized credential verification and account recovery operations. It utilizes a modular architecture to perform scalable, automated authentication tests against target accounts, ensuring strict adherence to session handling and rate-limiting protocols.

## Key Capabilities

* **Audit Modes:**
    * **Targeted Recovery:** Rigorous verification for single-account access restoration.
    * **Bulk Audit:** Scalable assessment of multiple user accounts against a credential dataset.
* **Session Persistence:** Encrypted session management (AES-256) to maintain authenticated states.
* **Traffic Management:** Integrated proxy rotation engine to distribute network requests.
* **Reporting:** Granular logging of successful authentications and technical diagnostics.

## System Requirements
* Python 3.8+
* Network access to target endpoints (HTTPS)
* Dependencies: `instagrapi`, `cryptography`, `colorama`

## Installation

1.  **Deploy Repository:**
    ```bash
    git clone [https://github.com/your-org/honeybadger.git](https://github.com/your-org/honeybadger.git)
    cd honeybadger
    ```

2.  **Initialize Environment:**
    ```bash
    pip install -r requirements.txt
    ```

## Operational Guide

1.  **Data Provisioning:**
    Populate the `data/` directory with your assessment datasets:
    * `data/passwords.txt`: Newline-separated credential list.
    * `data/proxies.txt`: Proxy servers in `http://user:pass@ip:port` format.
    * `data/usernames.txt`: (For Bulk Mode) List of target identifiers.

2.  **Launch Sequence:**
    Execute the entry point script:
    ```bash
    python3 launch.py
    ```

3.  **Operation Selection:**
    Follow the interactive console to select the appropriate audit module (Single vs. Bulk).

## Compliance & Legal
**IMPORTANT:** This software is engineered for **authorized security auditing and personal account recovery only**. Unauthorized use against systems or accounts you do not own or have explicit permission to test is a violation of Terms of Service and applicable laws.
