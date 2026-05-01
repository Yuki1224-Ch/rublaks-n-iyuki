# session.py
from curl_cffi import requests
from util import get_proxies
import random

class Session(requests.Session):
    def __init__(self, proxy=None):
        super().__init__(impersonate="chrome124")
        if proxy:
            self.proxies = {"http": proxy, "https": proxy}
            self.proxy = proxy

    @staticmethod
    def random_session():
        proxies = get_proxies()
        proxy = random.choice(proxies) if proxies else None
        return Session(proxy)