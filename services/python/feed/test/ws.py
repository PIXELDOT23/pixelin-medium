# Import Modules
import time
import threading

# Neo API
from neo_api_client import NeoAPI
from websocket import continuous_frame

CONSUMER_KEY = "f0b5adb4-2e5f-4f41-8804-2b951e485bb2"
MOBILE_NUMBER = "+919597040027"
UCC = "YGY9G"
MPIN = "192001"
INSTRUMENT_TOKENS = [
    {"instrument_token": "2932", "exchange_segment": "cde_fo"}
]

# # Props
# inst_tokens = [{"instrument_token": "2932", "exchange_segment": "cde_fo"}]
#
# # Global State
# client = None
# connected = False
# connecting = False
# lock = threading.Lock()
# TOTP = None
#
# # Call-backs
# def on_message(message):
#     print('[Res]: ', message)
#
#
# def on_error(message):
#     result = message
#     print('[OnError]: ', result)
#
#
# def on_open(message):
#     global connected
#     connected = True
#     print('[OnOpen]: ', "WS Connected")
#
#     # Always resubscribe after open
#     try:
#         client.subscribe(instrument_tokens=INSTRUMENT_TOKENS, isDepth=False)
#         client.subscribe(instrument_tokens=INSTRUMENT_TOKENS, isDepth=True)
#
#     except Exception as e:
#         print("Resubscribe failed: ", e)
#
#
# def on_close(message):
#     global connected
#     connected = False
#     print('[OnClose]: ', message)
#
# # Connect & Login
# def connect():
#     global client, connecting
#
#     with lock:
#         if connecting:
#             return
#         connecting = True
#
#         try:
#             print("🔐 Logging in...")
#
#             client = NeoAPI(environment='prod', consumer_key=CONSUMER_KEY)
#             client.totp_login(mobile_number=MOBILE_NUMBER, ucc=UCC, totp=TOTP)
#             client.totp_validate(mpin=MPIN)
#
#             # Setup Callbacks for websocket events (Optional)
#             client.on_message = on_message  # called when message is received from websocket
#             client.on_error = on_error  # called when any error or exception occurs in code or websocket
#             client.on_close = on_close  # called when websocket connection is closed
#             client.on_open = on_open  # called when websocket successfully connects
#
#             # Initial subscribe (this triggers WS)
#             client.subscribe(instrument_tokens=INSTRUMENT_TOKENS, isDepth=False)
#             client.subscribe(instrument_tokens=INSTRUMENT_TOKENS, isDepth=True)
#
#             # Give WS time to stabilize
#             time.sleep(3)
#
#         except Exception as e:
#             print("Connect failed:", e)
#
#         finally:
#             connecting = False
#
# # Heart Beat
# def heartbeat():
#     while True:
#         time.sleep(20)
#
#         if not connected or client is None:
#             continue
#
#         try:
#             # Re-sub acts as keep alive
#             client.subscribe(instrument_tokens=INSTRUMENT_TOKENS, isDepth=True)
#
#         except Exception as e:
#             print("Resubscribe failed: ", e)
#
# # Watch Dog
# def watchdog():
#     while True:
#         time.sleep(5)
#
#         if not connected:
#             print("🔁 Reconnecting...")
#             try:
#                 connect()
#             except Exception as e:
#                 print("Reconnect error:", e)
#                 time.sleep(5)
#
# # Main
# if __name__ == "__main__":
#
#     TOTP = input("Enter TOTP: ").strip()
#
#     connect()
#
#     threading.Thread(target=heartbeat, daemon=True).start()
#     threading.Thread(target=watchdog, daemon=True).start()
#
#     print("🚀 Neo feed running (Ctrl+C to stop)")
#
#     while True:
#         time.sleep(1)

print("🔐 Logging in...")
TOTP = input("Enter TOTP: ").strip()

client = NeoAPI(environment='prod', consumer_key=CONSUMER_KEY)
client.totp_login(mobile_number=MOBILE_NUMBER, ucc=UCC, totp=TOTP)
client.totp_validate(mpin=MPIN)

client.help("socket")
