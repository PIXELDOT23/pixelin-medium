# Import Packages
import time
import threading
import signal

# Import Configs
from config import INSTRUMENT_TOKENS, NODE_WS_URL

# Import Modules
from ws_publisher import WSPublisher
from neo_login import NeoLoginManager
from sf_socket import NeoSFClient
from dp_socket import NeoDPClient

def health_monitor(feeds):
    while True:
        for f in feeds:
            age = time.time() - f.last_msg_ts if f.last_msg_ts else -1
            print(
                f"[HEALTH] {f.name} | age={age:.2f}s | reconnects={f.reconnects}"
            )
        time.sleep(5)

def run():
    publisher = WSPublisher(NODE_WS_URL)
    login_mgr = NeoLoginManager()

    sf = NeoSFClient("SF", login_mgr.create_client, publisher, INSTRUMENT_TOKENS)
    dp = NeoDPClient("DP", login_mgr.create_client, publisher, INSTRUMENT_TOKENS)

    sf.start()
    dp.start()

    threading.Thread(target=health_monitor, args=([sf, dp],), daemon=True).start()

    stop = threading.Event()

    def shutdown(sig, frame):
        print("🔴 Shutting down...")
        stop.set()
        sf.stop()
        dp.stop()
        publisher.close()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while not stop.is_set():
        time.sleep(1)

if __name__ == "__main__":
    run()
