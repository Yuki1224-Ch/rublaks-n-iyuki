# auth_intent.py - FIXED & WORKING
from curl_cffi import requests
from base64 import b64encode
from time import time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import random

class AuthIntent:
    @staticmethod
    def string_to_bytes(raw_string) -> bytes:
        return bytes(raw_string, 'utf-8')

    @staticmethod
    def export_public_key_as_spki(public_key) -> str:
        spki_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return b64encode(spki_bytes).decode('utf-8')

    @staticmethod
    def generate_signing_key_pair_unextractable() -> tuple:
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def sign(private_key, data) -> str:
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return b64encode(signature).decode('utf-8')

    @staticmethod
    def get_auth_intent(session: requests.Session) -> dict | None:
        try:
            # CRITICAL HEADERS
            session.headers.update({
                "Origin": "https://www.roblox.com",
                "Referer": "https://www.roblox.com/login",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
            })

            # Generate key pair
            private_key, public_key = AuthIntent.generate_signing_key_pair_unextractable()
            client_public_key = AuthIntent.export_public_key_as_spki(public_key)
            client_epoch_timestamp = str(int(time() * 1000))  # Roblox uses milliseconds

            # Get server nonce
            url = "https://apis.roblox.com/hba-service/v1/getServerNonce"
            resp = session.get(url, impersonate="chrome120", timeout=15)

            if resp.status_code != 200:
                return None

            server_nonce = resp.text.strip().strip('"')
            if not server_nonce or len(server_nonce) < 10:
                return None

            # Construct payload and sign
            payload = f"{client_public_key}|{client_epoch_timestamp}|{server_nonce}"
            sai_signature = AuthIntent.sign(private_key, AuthIntent.string_to_bytes(payload))

            return {
                "clientPublicKey": client_public_key,
                "clientEpochTimestamp": client_epoch_timestamp,
                "serverNonce": server_nonce,
                "saiSignature": sai_signature
            }

        except Exception as e:
            print(f"[DEBUG] AuthIntent failed: {e}")
            return None