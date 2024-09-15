import base64
import json
import hashlib
import hmac
import re
from datetime import datetime


class JWT:
    def __init__(self):
        self._secret = "é2adfD21$98FASDD"

    @staticmethod
    def base64_url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

    @staticmethod
    def base64_url_decode(data: str) -> bytes:
        padding: str = '=' * (4 - len(data) % 4)
        return base64.urlsafe_b64decode(data + padding)

    def generate_token(self, header: dict, payload: dict, validity: int = 600) -> str:
        if validity <= 0:
            raise ValueError("Validity must be a positive integer")

        base64_header = self.base64_url_encode(json.dumps(header).encode())
        base64_payload = self.base64_url_encode(json.dumps(payload).encode())

        secret = base64.urlsafe_b64encode(self._secret.encode())
        signature = hmac.new(secret, f"{base64_header}.{base64_payload}".encode(), hashlib.sha256).digest()
        base64_signature = self.base64_url_encode(signature)

        return f"{base64_header}.{base64_payload}.{base64_signature}"

    def is_expired(self, token: str) -> bool:
        payload = self.get_payload(token)
        now = datetime.utcnow()
        return payload['exp'] < int(now.timestamp())

    def check_validity(self, token: str) -> bool:
        header = self.get_header(token)
        payload = self.get_payload(token)
        verify_token = self.generate_token(header, payload)
        return token == verify_token

    @staticmethod
    def is_valid(token: str) -> bool:
        return re.match(r'^[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+$', token) is not None

    def get_header(self, token: str) -> dict:
        parts = token.split('.')
        return json.loads(self.base64_url_decode(parts[0]).decode('utf-8'))

    def get_payload(self, token: str) -> dict:
        parts = token.split('.')
        return json.loads(self.base64_url_decode(parts[1]).decode('utf-8'))
