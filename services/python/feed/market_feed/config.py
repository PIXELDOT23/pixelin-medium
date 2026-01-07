# config.py
import os
from dotenv import load_dotenv

load_dotenv()

NODE_WS_URL = os.getenv("NODE_WS_URL", "ws://localhost:5000")

CONSUMER_KEY = os.getenv("NEO_CONSUMER_KEY", "f0b5adb4-2e5f-4f41-8804-2b951e485bb2")

MOBILE_NUMBER = os.getenv("NEO_MOBILE", "+919597040027")

UCC = os.getenv("NEO_UCC", "YGY9G")

MPIN = os.getenv("NEO_MPIN", "192001")

# list of instrument dicts as strings or environment config
INSTRUMENT_TOKENS = [
    {"instrument_token": "465849", "exchange_segment": "mcx_fo"}
]
# 2932 465849
