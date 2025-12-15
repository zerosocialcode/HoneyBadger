import os
import json
from cryptography.fernet import Fernet

SESSION_DIR = "honeybadger_sessions"
KEY_FILE = "honeybadger.key"

def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def save_session(username, settings):
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)
    
    try:
        key = get_or_create_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(json.dumps(settings).encode())
        
        safe_user = "".join(c for c in username if c.isalnum() or c in ('_'))
        path = os.path.join(SESSION_DIR, f"{safe_user}.enc")
        
        with open(path, "wb") as file:
            file.write(encrypted_data)
        return True
    except Exception:
        return False

def load_session(username):
    safe_user = "".join(c for c in username if c.isalnum() or c in ('_'))
    path = os.path.join(SESSION_DIR, f"{safe_user}.enc")
    
    if not os.path.exists(path):
        return None
    
    try:
        key = get_or_create_key()
        f = Fernet(key)
        with open(path, "rb") as file:
            decrypted_data = f.decrypt(file.read())
            return json.loads(decrypted_data.decode())
    except Exception:
        return None
