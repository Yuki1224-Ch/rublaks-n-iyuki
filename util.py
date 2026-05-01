# util.py - FIXED - NO CLASS, ONLY FUNCTIONS
import os
import json
import random
import string
from typing import List

ROOT = os.path.abspath(os.path.dirname(__file__))

def get_config() -> dict:
    path = os.path.join(ROOT, "config.json")
    if not os.path.isfile(path):
        raise FileNotFoundError("config.json not found!")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_accounts() -> List[str]:
    path = os.path.join(ROOT, "input", "combos.txt")
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if ":" in line and line.strip()]

def get_proxies() -> List[str]:
    path = os.path.join(ROOT, "proxies.txt")
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and line.startswith("http")]

def random_string(n: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))