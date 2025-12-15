import os
import shutil
import sys
import time
import threading
import random
import re
from colorama import Fore, Style, init

init(autoreset=True)

class Theme:
    # We will pick a random primary color for the banner each time
    COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    
    PRIMARY = Fore.YELLOW
    SECONDARY = Fore.WHITE
    SUCCESS = Fore.GREEN
    WARNING = Fore.LIGHTYELLOW_EX
    ERROR = Fore.RED
    MUTED = Fore.LIGHTBLACK_EX
    RESET = Style.RESET_ALL

def get_terminal_width():
    try:
        columns, _ = shutil.get_terminal_size(fallback=(80, 24))
        return columns
    except:
        return 80

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def print_centered(text):
    width = get_terminal_width()
    clean_text = strip_ansi(text)
    padding = max(0, (width - len(clean_text)) // 2)
    print(" " * padding + text)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_banner():
    """Loads banner from .banner/banner.txt or falls back to text."""
    banner_path = os.path.join(".banner", "banner.txt")
    if not os.path.exists(banner_path):
         banner_path = os.path.join("data", "banner.txt")

    if os.path.exists(banner_path):
        try:
            with open(banner_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            pass
    return "HONEYBADGER"

def print_header():
    clear_screen()
    
    banner_color = random.choice(Theme.COLORS)
    banner_text = load_banner()
    
    for line in banner_text.splitlines():
        print_centered(f"{banner_color}{line}{Theme.RESET}")

    print_centered(f"{Theme.SECONDARY}Honey badger don't care. Honey badger takes what it wants.{Theme.RESET}")
    print("\n")

def print_separator():
    print("")

def print_status(message, status="INFO"):
    symbol = "•"
    color = Theme.PRIMARY
    
    if status == "OK":
        symbol = "✓"
        color = Theme.SUCCESS
    elif status == "FAIL":
        symbol = "✗"
        color = Theme.ERROR
    elif status == "WARN":
        symbol = "!"
        color = Theme.WARNING
    elif status == "BUSY":
        symbol = "»"
        color = Theme.WARNING

    print(f"  {color}{symbol}{Theme.RESET} {message}")

def print_centered_status(message, color=Theme.PRIMARY):
    print_centered(f"{color}{message}{Theme.RESET}")

def print_summary(success_count, total_count, duration):
    print("\n")
    print_centered(f"{Theme.PRIMARY}AUDIT SUMMARY{Theme.RESET}")
    print_centered(f"Total Targets         : {total_count}")
    print_centered(f"Successful Recoveries : {Theme.SUCCESS}{success_count}{Theme.RESET}")
    print_centered(f"Execution Time        : {round(duration, 2)}s")
    
    if success_count > 0:
        print("\n")
        print_centered(f"{Theme.SUCCESS}[✓] Audit Complete. Credentials exported to logs/success.log{Theme.RESET}")
    else:
        print("\n")
        print_centered(f"{Theme.MUTED}[-] Audit Complete. No valid credentials found.{Theme.RESET}")
