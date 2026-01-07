# Import Modules
import json
import time
import threading

from neo_api_client import NeoAPI
from config import CONSUMER_KEY, MOBILE_NUMBER, UCC, MPIN, INSTRUMENT_TOKENS

class NeoFeedClient:

    def __init__(self, publisher,
                 consumer_key=CONSUMER_KEY,
                 instrument_tokens=INSTRUMENT_TOKENS,
                 mobile_number=MOBILE_NUMBER,
                 ucc=UCC,
                 mpin=MPIN):
        # publisher: object with .send(json_str)
        self.publisher = publisher
        self.instrument_tokens = instrument_tokens
        self.mobile_number = mobile_number
        self.ucc = ucc
        self.mpin = mpin

        self.client = NeoAPI(environment= "prod", consumer_key = CONSUMER_KEY)

        # wire callbacks
        self.client.on_message = self._on_message
        self.client.on_error = self._on_error
        self.client.on_close = self._on_close
        self.client.on_open = self._on_open

        # internal flags
        self.logged_in = False
        self.validated = False
        self.connected = False
        self.subscribed = False
        self.quote = False
        self.running = False

        # Thread-safe lock
        self.lock = threading.Lock()

        # watchdog
        self.last_message_ts = time.time()
        self.watchdog_interval = 10         # check every N seconds
        self.watchdog_threshold = 120        # restart if no message for N seconds

        # stop event
        self._stop_event = threading.Event()

    # Login and Validate
    def login_and_validate(self):
        """Step 1: TOTP login"""

        with self.lock:

            print("\n🔐 Performing Login...")

            totp = input("Enter TOTP: ").strip()  # get manually

            try:
                data = self.client.totp_login(
                    mobile_number= self.mobile_number,
                    ucc= self.ucc,
                    totp= totp,
                )
                print("TOTP Login OK")
                self.logged_in = True

            except Exception as e:
                print("TOTP Login Failed:", e)
                self.logged_in = False
                return False

            """Step 2: Validate MPIN"""
            try:
                data = self.client.totp_validate(mpin = MPIN)
                print("MPIN Validation OK:", data)
                self.validated = True

            except Exception as e:
                print("MPIN Validation Failed:", e)
                self.validated = False
                return False

        return True

    # Subscribe
    def _subscribe(self):

        try:
            # Avoid double subscribe
            if self.subscribed:
                return True

            # Depth
            self.client.subscribe(
                instrument_tokens=self.instrument_tokens,
                isIndex=False,
                isDepth=True
            )

            self.subscribed = True
            print("[NeoFeedClient] Subscribed to QUOTE + DEPTH :", self.instrument_tokens)
            return True
        except Exception as e:
            print("[NeoFeedClient] Subscribe failed:", e)
            self.subscribed = False
            return False

    # Quote
    def _quote(self):
        try:
            self.client.quotes(instrument_tokens=self.instrument_tokens, quote_type="all")
            self.quote = True
            print("[NeoFeedClient] Quote ok")

        except Exception as e:
            print("[NeoFeedClient] Quote failed:", e)
            self.quote = False
            return False

    def start(self):
        """
        Start the client: login -> validate -> subscribe -> watchdog.
        This returns quickly; background threads handle recovery and streaming.
        """
        if self.running:
            print("[NeoFeedClient] Already running")
            return

        self.running = True
        self._stop_event.clear()

        # Run initial connect/recover in background
        t = threading.Thread(target=self._run_forever, daemon=True)
        t.start()

        # Start watchdog thread
        wd = threading.Thread(target=self._watchdog, daemon=True)
        wd.start()


    # main run & loop
    def _run_forever(self):
        backoff = 1

        while not self._stop_event.is_set():
            try:
                # If already OK, just sleep and wait for close/error to trigger recovery
                if self.logged_in and self.validated and self.subscribed:
                    # nothing to do here — SDK handles socket read in background via callbacks
                    time.sleep(1)
                    continue

                print("[NeoFeedClient] Starting connection sequence...")
                ok = self.login_and_validate()
                if not ok:
                    print(f"[NeoFeedClient] Login/validate failed: retry in {backoff}s")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)
                    continue

                # if login OK, subscribe
                ok = self._subscribe()
                if not ok:
                    print(f"[NeoFeedClient] Subscribe failed: retry in {backoff}s")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)
                    continue

                # Quote
                ok = self._quote()
                if not ok:
                    print(f"[NeoFeedClient] Quote failed: retry in {backoff}s")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)
                    continue

                # reset exponential backoff after success
                backoff = 1
                print("[NeoFeedClient] Connection sequence complete, client should be streaming now.")

                # 🔴 DO NOT loop subscribe again
                while self.logged_in and self.validated and self.subscribed:
                    time.sleep(1)

            except Exception as e:
                print("[NeoFeedClient] Unexpected error in run loop:", e)
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)

    # watchdog - detect silent stalls
    def _watchdog(self):
        while not self._stop_event.is_set():
            time.sleep(self.watchdog_interval)
            age = time.time() - self.last_message_ts
            print(f"[NeoFeedClient] Age: {age}")

            if age > self.watchdog_threshold:
                print(f"[NeoFeedClient][Watchdog] No messages for {age:.1f}s (> {self.watchdog_threshold}), restarting client...")

                with self.lock:
                    print("🚨 Feed stalled, resetting flags")
                    self.logged_in = False
                    self.validated = False
                    self.subscribed = False

    def _on_open(self, *args, **kwargs):
        print("🟢 Neo SDK connection opened")

    def _on_message(self, message):
        """
        Called by SDK whenever a message arrives.
        We'll update last_message_ts and forward to Node WS.
        Accept dict/list or raw JSON string.
        """
        try:

            print("Full [MSG]: ", message)

            # update watchdog timestamp
            self.last_message_ts = time.time()

            if not isinstance(message, dict):
                return

            if message.get("type") != "stock_feed":
                return

            # normalize to JSON string before sending to Node
            for update in message.get("data", []):

                name = update.get("name")
                tk = update.get("tk")

                if not tk:
                    continue

                if name in ("sf", "if"):
                    payload = {
                        "type": "QUOTE",
                        "tk": tk,
                        "data": update
                    }
                    self.publisher.send(json.dumps(payload))

                    # Debug print - comment out if noisy
                    print("[NeoFeedClient] Message QUOTE:", payload)

                elif name == "dp":
                    payload = {
                        "type": "DEPTH",
                        "tk": tk,
                        "data": update
                    }
                    self.publisher.send(json.dumps(payload))

                    # Debug print - comment out if noisy
                    print("[NeoFeedClient] Message DEPTH:", payload)

        except Exception as e:
            print("[NeoFeedClient] Error forwarding msg:", e)

    def _on_error(self, e):

        print("❌ [NeoFeedClient] Neo SDK Error:", e)

        # Mark struct invalid and let run loop recover
        with self.lock:
            self.logged_in = False
            self.validated = False
            self.subscribed = False

    def _on_close(self, *args):

        print("🔴 [NeoFeedClient] Neo SDK Closed:", args)

        # Mark struct invalid and let run loop recover
        with self.lock:
            self.logged_in = False
            self.validated = False
            self.subscribed = False

    # Stop & Shutdown
    def stop(self):

        print("[NeoFeedClient] Stopping...")

        self._stop_event.set()

        self.running = False
        print("[NeoFeedClient] Stopped.")
