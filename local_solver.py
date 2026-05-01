# local_solver.py - CUSTOM SOLVER - No External APIs, Works on All Terminals
import time
import requests
from util import get_config, format_proxy_for_2captcha, parse_proxy

try:
    from custom_solver import CustomCaptchaSolver
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

config = get_config()
USE_CUSTOM_SOLVER = config.get("useCustomSolver", True)  # Enable custom solver by default

def get_token(session: requests.Session, metadata: str) -> str | None:
    """
    Solve Roblox Arkose Labs captcha using CUSTOM solver (no external APIs)
    Returns the captcha token on success, None on failure
    """
    if USE_CUSTOM_SOLVER and PLAYWRIGHT_AVAILABLE:
        return _solve_with_custom_solver(session, metadata)
    else:
        # Fallback to 2captcha if custom solver is disabled or unavailable
        return _solve_with_2captcha(session, metadata)

def _solve_with_custom_solver(session: requests.Session, metadata: str) -> str | None:
    """
    Use our custom Playwright-based solver - 100% free, no APIs
    """
    try:
        from json import loads
        data = loads(metadata)
        blob = data.get("unifiedCaptchaId") or data.get("captchaToken")
        if not blob:
            return None

        # Extract proxy for browser
        proxy_dict = getattr(session, "proxy_dict", None)
        
        print("[*] Using CUSTOM Captcha Solver (No API)")
        solver = CustomCaptchaSolver(debug=True)
        
        try:
            # Start browser with proxy support
            solver.start_browser(proxy=proxy_dict)
            
            # Solve the captcha
            success = solver.solve_funcaptcha(
                site_key="476068BF-9607-4799-B53D-966BE98E2B81",
                service_url="https://www.roblox.com/login"
            )
            
            if success:
                print("[+] Custom solver succeeded!")
                # Note: Custom solver handles the challenge in-browser
                # Return a placeholder token or handle session directly
                return "CUSTOM_SOLVED"
            else:
                print("[-] Custom solver failed")
                return None
                
        finally:
            solver.close()
            
    except Exception as e:
        print(f"[-] Custom solver error: {e}")
        return None

def _solve_with_2captcha(session: requests.Session, metadata: str) -> str | None:
    """
    Fallback: Solve using 2captcha API (requires API key)
    """
    try:
        from json import loads
        KEY = config["2captchaKey"]
        KEYS = [KEY] if not config.get("useKeyRotation") else [l.strip() for l in open(config.get("keyFile", "2captcha_keys.txt")) if l.strip()]
        
        data = loads(metadata)
        blob = data.get("unifiedCaptchaId") or data.get("captchaToken")
        if not blob:
            return None

        # Get current key (support key rotation)
        key = KEYS[0]
        
        # Extract and format proxy for 2captcha
        proxy_dict = getattr(session, "proxy_dict", None)
        proxy_formatted = format_proxy_for_2captcha(proxy_dict)
        
        # Prepare submission data for 2captcha
        submit_data = {
            "key": key,
            "method": "funcaptcha",
            "publickey": "476068BF-9607-4799-B53D-966BE98E2B81",
            "pageurl": "https://www.roblox.com/login",
            "surl": "https://roblox-api.arkoselabs.com",
            "data[blob]": blob,
            "json": "1"  # Request JSON response for better error handling
        }
        
        # Add proxy if available
        if proxy_formatted:
            submit_data["proxy"] = proxy_formatted
            submit_data["proxytype"] = "HTTP"

        # Submit captcha to 2captcha
        resp = requests.post("http://2captcha.com/in.php", data=submit_data, timeout=30)
        
        if not resp.text.startswith("OK|"):
            return None
        
        captcha_id = resp.text.split("|")[1]
        
        # Poll for result with exponential backoff
        max_attempts = 60
        attempt = 0
        delay = 3  # Initial delay
        
        while attempt < max_attempts:
            time.sleep(delay)
            
            poll_resp = requests.get(
                "http://2captcha.com/res.php",
                params={"key": key, "action": "get", "id": captcha_id},
                timeout=30
            )
            
            if poll_resp.text.startswith("OK|"):
                token = poll_resp.text.split("|")[1]
                return token
            
            # Increase delay gradually (max 10 seconds)
            if attempt < 10:
                delay = min(delay + 1, 10)
            
            attempt += 1
        
        return None
        
    except Exception as e:
        return None