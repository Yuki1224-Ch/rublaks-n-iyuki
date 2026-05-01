# util.py - IMPROVED - Proxy format support & utility functions
import os
import json
import random
import string
import re
from typing import List, Optional, Dict

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

def parse_proxy(proxy_line: str) -> Optional[Dict[str, str]]:
    """
    Parse proxy from multiple formats:
    - host:port
    - http://host:port
    - https://host:port
    - username:password@host:port
    - http://username:password@host:port
    - https://username:password@host:port
    - username:password:host:port
    - host:port:username:password
    
    Returns dict with keys: 'url', 'host', 'port', 'username', 'password', 'protocol'
    """
    proxy_line = proxy_line.strip()
    if not proxy_line or proxy_line.startswith('#'):
        return None
    
    # Default values
    result = {
        'url': '',
        'host': '',
        'port': '',
        'username': '',
        'password': '',
        'protocol': 'http'
    }
    
    # Remove any whitespace
    proxy_line = proxy_line.strip()
    
    # Pattern 1: protocol://username:password@host:port
    pattern1 = r'^(https?)://([^:]+):([^@]+)@([^:]+):(\d+)$'
    match = re.match(pattern1, proxy_line)
    if match:
        result['protocol'] = match.group(1)
        result['username'] = match.group(2)
        result['password'] = match.group(3)
        result['host'] = match.group(4)
        result['port'] = match.group(5)
        result['url'] = f"{result['protocol']}://{result['username']}:{result['password']}@{result['host']}:{result['port']}"
        return result
    
    # Pattern 2: protocol://host:port
    pattern2 = r'^(https?)://([^:]+):(\d+)$'
    match = re.match(pattern2, proxy_line)
    if match:
        result['protocol'] = match.group(1)
        result['host'] = match.group(2)
        result['port'] = match.group(3)
        result['url'] = f"{result['protocol']}://{result['host']}:{result['port']}"
        return result
    
    # Pattern 3: username:password@host:port (no protocol)
    pattern3 = r'^([^:]+):([^@]+)@([^:]+):(\d+)$'
    match = re.match(pattern3, proxy_line)
    if match:
        result['username'] = match.group(1)
        result['password'] = match.group(2)
        result['host'] = match.group(3)
        result['port'] = match.group(4)
        result['url'] = f"http://{result['username']}:{result['password']}@{result['host']}:{result['port']}"
        return result
    
    # Pattern 4: Check for 4-part colon-separated formats
    parts = proxy_line.split(':')
    if len(parts) == 4:
        # Try to determine format by checking which part is numeric (port)
        # Format A: username:password:host:port (parts[3] is port/numeric)
        # Format B: host:port:username:password (parts[1] is port/numeric)
        
        try:
            port_a = int(parts[3])  # Check if last part is numeric (Format A)
            port_b = int(parts[1])  # Check if second part is numeric (Format B)
            
            # If both are numeric, prefer Format A (username:password:host:port)
            # as it's more common
            result['username'] = parts[0]
            result['password'] = parts[1]
            result['host'] = parts[2]
            result['port'] = parts[3]
            result['url'] = f"http://{result['username']}:{result['password']}@{result['host']}:{result['port']}"
            return result
            
        except ValueError:
            # Neither format matches perfectly, try Format A as default
            result['username'] = parts[0]
            result['password'] = parts[1]
            result['host'] = parts[2]
            result['port'] = parts[3]
            result['url'] = f"http://{result['username']}:{result['password']}@{result['host']}:{result['port']}"
            return result
    
    # Pattern 6: host:port (simple)
    if len(parts) == 2 and parts[1].isdigit():
        result['host'] = parts[0]
        result['port'] = parts[1]
        result['url'] = f"http://{result['host']}:{result['port']}"
        return result
    
    # Pattern 7: host:port with protocol prefix check
    if len(parts) == 2:
        try:
            int(parts[1])
            result['host'] = parts[0]
            result['port'] = parts[1]
            result['url'] = f"http://{result['host']}:{result['port']}"
            return result
        except ValueError:
            pass
    
    return None

def get_proxies() -> List[Dict[str, str]]:
    """Get list of parsed proxies with full format support"""
    path = os.path.join(ROOT, "proxies.txt")
    if not os.path.isfile(path):
        return []
    
    proxies = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_proxy(line)
            if parsed:
                proxies.append(parsed)
    return proxies

def get_proxy_url(proxy: Optional[Dict[str, str]]) -> Optional[str]:
    """Extract URL from parsed proxy dict"""
    if not proxy:
        return None
    return proxy.get('url')

def format_proxy_for_2captcha(proxy: Optional[Dict[str, str]]) -> str:
    """
    Format proxy for 2captcha API
    Format: host:port or username:password:host:port
    """
    if not proxy:
        return ""
    
    if proxy.get('username') and proxy.get('password'):
        return f"{proxy['username']}:{proxy['password']}:{proxy['host']}:{proxy['port']}"
    return f"{proxy['host']}:{proxy['port']}"

def random_string(n: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))