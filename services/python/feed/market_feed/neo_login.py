import threading
from neo_api_client import NeoAPI
from config import CONSUMER_KEY, MOBILE_NUMBER, UCC, MPIN

class NeoLoginManager:
    def __init__(self):
        self._totp = None
        self.lock = threading.Lock()

    def create_client(self):
        with self.lock:
            if not self._totp:
                self._totp = input("🔐 Enter TOTP (once): ").strip()

            client = NeoAPI(environment="prod", consumer_key=CONSUMER_KEY)
            client.totp_login(
                mobile_number=MOBILE_NUMBER,
                ucc=UCC,
                totp=self._totp
            )
            client.totp_validate(mpin=MPIN)
            return client
