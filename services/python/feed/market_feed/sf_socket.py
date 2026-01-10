# Import Modules
import time

# Base  socket module
from base_socket import NeoSocketBase


class NeoSFClient(NeoSocketBase):

    def _subscribe(self):
        self.client.subscribe(
            instrument_tokens=self.tokens,
            isIndex=False,
            isDepth=False
        )
        print("📈 [SF] subscribed")

    def handle_message(self, msg):
        if msg.get("type") != "stock_feed":
            return

        for d in msg.get("data", []):
            if d.get("name") == "sf":
                self.publisher.send({
                    "type": "QUOTE",
                    "tk": d["tk"],
                    "data": d,
                    "__src_ts": time.time()
                })
