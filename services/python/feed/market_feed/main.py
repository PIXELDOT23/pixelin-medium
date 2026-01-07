# Import Modules
import signal
import time
import threading

from ws_publisher import WSPublisher
from feed_client import NeoFeedClient

def run():
    publisher = WSPublisher()           # Connects to Node websocket server
    feed = NeoFeedClient(publisher)     # wire feed to publisher
    # Setup signal handlers for clean shutdown
    shutdown_event = threading.Event()

    def _signal_handler(sig, frame):
        print("\n🔴 [runner] Caught signal, shutting down...")
        shutdown_event.set()
        feed.stop()
        publisher.close()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Start Neo feed client
    feed.start()

    try:
        while not shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        _signal_handler(None, None)

    print("🔴 [runner] Exiting.")


if __name__ == '__main__':
    run()
