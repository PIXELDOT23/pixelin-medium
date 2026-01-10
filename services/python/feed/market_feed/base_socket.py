import time
import threading

class NeoSocketBase:
    def __init__(self, name, client_factory, publisher, tokens):
        self.name = name
        self.client_factory = client_factory
        self.publisher = publisher
        self.tokens = tokens

        self.client = None
        self.running = False
        self.last_msg_ts = 0
        self.reconnects = 0

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False

    def _run(self):
        backoff = 1
        while self.running:
            try:
                self.client = self.client_factory()
                self._wire()
                self._subscribe()
                backoff = 1

                while self.running:
                    time.sleep(1)

            except Exception as e:
                print(f"❌ [{self.name}] error:", e)

            self.reconnects += 1
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)

    def _wire(self):
        self.client.on_open = lambda *_: print(f"🟢 [{self.name}] open")
        self.client.on_close = lambda *_: print(f"🔴 [{self.name}] closed")
        self.client.on_error = lambda e: print(f"❌ [{self.name}] error:", e)
        self.client.on_message = self._on_message

    def _on_message(self, msg):
        self.last_msg_ts = time.time()
        self.handle_message(msg)

    def _subscribe(self): ...
    def handle_message(self, msg): ...
