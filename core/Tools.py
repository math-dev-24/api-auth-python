from hashlib import sha256
from flask import jsonify
import re


class Tools:

    @staticmethod
    def hash_password(password: str) -> str:
        salt = "et2124$FDC56"
        password = salt + sha256((password + salt).encode('utf-8')).hexdigest()
        return password

    @staticmethod
    def email_validator(email: str) -> bool:
        match = re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
        return match is not None

    @staticmethod
    def compare_passwords(password: str, hashed_password: str) -> bool:
        return Tools.hash_password(password) == hashed_password

    @staticmethod
    def get_current_timestamp() -> int:
        return int(round(1000 * Tools.get_current_timestamp()))
