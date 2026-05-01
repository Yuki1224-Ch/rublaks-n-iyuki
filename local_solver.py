# local_solver.py - FIXED
import time
import requests
from util import get_config  # FIXED
from json import loads

config = get_config()  # FIXED
KEY = config["2captchaKey"]
KEYS = [KEY] if not config.get("useKeyRotation") else [l.strip() for l in open(config.get("keyFile", "2captcha_keys.txt")) if l.strip()]

def get_token(session: requests.Session, metadata: str) -> str | None:
    try:
        data = loads(metadata)
        blob = data.get("unifiedCaptchaId") or data.get("captchaToken")
        if not blob: return None

        key = KEYS[0]
        proxy = getattr(session, "proxy", None)
        formatted = ""
        if proxy:
            proxy = proxy.split("://", 1)[-1]
            formatted = proxy.split("@", 1)[-1] if "@" in proxy else proxy

        submit = {
            "key": key, "method": "funcaptcha", "publickey": "476068BF-9607-4799-B53D-966BE98E2B81",
            "pageurl": "https://www.roblox.com/login", "surl": "https://roblox-api.arkoselabs.com",
            "data[blob]": blob
        }
        if formatted:
            submit["proxy"] = formatted
            submit["proxytype"] = "HTTP"

        r = requests.post("http://2captcha.com/in.php", data=submit, timeout=30)
        if not r.text.startswith("OK|"): return None
        cid = r.text.split("|")[1]

        for _ in range(60):
            time.sleep(5)
            poll = requests.get("http://2captcha.com/res.php", params={"key": key, "action": "get", "id": cid})
            if poll.text.startswith("OK|"):
                return poll.text.split("|")[1]
        return None
    except:
        return None