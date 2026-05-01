# main.py - FIXED
import sys, os, time, queue
from output import Output
from thread_lock import ThreadLock, lock
from threading import Thread
from counter import counter
from roblox import Roblox
from util import get_config, get_accounts  # FIXED
from combocheck import invalid, checked, locked

ROOT = os.path.abspath(os.path.dirname(__file__))

# Output folders
for folder in [
    "output", "output/usernames", "output/payment_info", "output/pending",
    "output/premium", "output/rap", "output/balance", "output/creation_date",
    "output/rare_items", "output/robux", "output/summary", "output/items",
    "output/badges"
]:
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)

# Files
for file in [
    "output/failed.txt", "output/invalid.txt", "output/valid.txt",
    "output/og_combo.txt", "output/valid_combo.txt", "output/cookies.txt",
    "output/locked.txt", "output/terminated.txt", "output/ageverified.txt",
    "output/temp_banned.txt"
]:
    if not os.path.isfile(file):
        open(file, "w").close()

# Skip files
invalid.read_file("output/invalid.txt")
checked.read_file("output/og_combo.txt")
locked.read_file("output/locked.txt")

# Config & combos
config = get_config()  # FIXED
THREAD_AMOUNT = config["threads"]
ACCOUNTS = get_accounts()  # FIXED

if not ACCOUNTS:
    Output("ERROR").log("No combos in input/combos.txt")
    sys.exit(1)

# Title
def change_terminal_name(name: str):
    if os.name == "nt":
        os.system(f"title {name}")
    else:
        sys.stdout.write(f"\033]0;{name}\007")
        sys.stdout.flush()

def title():
    last, start = 0, time.time()
    while True:
        try:
            now = time.time()
            elapsed = now - start or 1
            cps = (counter.get_value() - last) / elapsed
            last, start = counter.get_value(), now
            change_terminal_name(f"Checked: {counter.get_value()}/{len(ACCOUNTS)} ({cps:.2f}/s)")
        except:
            pass
        time.sleep(2)

def main():
    q = queue.Queue()
    for acc in ACCOUNTS:
        q.put(acc)

    threads = []
    for _ in range(min(THREAD_AMOUNT, len(ACCOUNTS))):
        t = Thread(target=Roblox(lock, counter, invalid, checked, locked, q).check)
        t.start()
        threads.append(t)

    Thread(target=title, daemon=True).start()

    for t in threads:
        t.join()

    Output("SUCCESS").log("Finished")

if __name__ == "__main__":
    main()