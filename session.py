# session.py - IMPROVED - Full proxy format support
from curl_cffi import requests
from util import get_proxies, get_proxy_url
import random

class Session(requests.Session):
    def __init__(self, proxy=None):
        super().__init__(impersonate="chrome124")
        self.proxy_dict = None
        self.proxy_url = None
        
        if proxy:
            # Handle both dict (new format) and string (legacy format)
            if isinstance(proxy, dict):
                self.proxy_dict = proxy
                self.proxy_url = get_proxy_url(proxy)
                proxy_url = self.proxy_url
            else:
                self.proxy_url = proxy
                proxy_url = proxy
            
            if proxy_url:
                self.proxies = {"http": proxy_url, "https": proxy_url}
                self.proxy = proxy_url

    @staticmethod
    def random_session():
        proxies = get_proxies()
        proxy = random.choice(proxies) if proxies else None
        return Session(proxy)