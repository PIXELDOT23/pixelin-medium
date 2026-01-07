# Import Modules
import threading
import json

from websocket import create_connection, WebSocketConnectionClosedException, WebSocketException
from config import NODE_WS_URL

class WSPublisher:
    def __init__(self, url = NODE_WS_URL, reconnect_delay = 2):
        self.url = url
        self.ws = None
        self.lock = threading.Lock()
        self.reconnect_delay = reconnect_delay
        self._connect()

    def _connect(self):
        try:
            print(f"🔵 Connecting to Node WS at {self.url}")
            self.ws = create_connection(self.url, timeout = 5)
            print("🔵 Connected to Node WS")

        except Exception as e:
            print("🔴 WS connect failed: ", e)
            self.ws = None

    def send(self, msg):
        """message: JSON string"""
        with self.lock:

            if not self.ws:
                self._connect()

                if not self.ws:
                    print("🔴 Cannot send: no WS connection")
                    return False

            try:
                # if message is dict, convert
                if not isinstance(msg, str):
                    msg = json.dumps(msg)

                self.ws.send(msg)
                return True

            except WebSocketConnectionClosedException:
                print("🔴 WS closed, reconnecting...")
                self._connect()
                if self.ws:
                    try:
                        self.ws.send(msg)
                        return True

                    except Exception as e:
                        print("🔴 [WSPublisher] Send after reconnect failed:", e)

            except WebSocketException as e:
                print("🔴 [WSPublisher] WS send failed (WebSocketException):", e)
                # try to reconnect once
                self._connect()
                return False

            except Exception as e:
                print("🔴 [WSPublisher] WS send failed:", e)
                return False

    def close(self):
        with self.lock:
            try:
                if self.ws:
                    self.ws.close()
                    self.ws = None
                print("🔴 [WSPublisher] Closed")

            except Exception as e:
                print("🔴 [WSPublisher] WS close failed:", e)
        
