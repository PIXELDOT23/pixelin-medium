// Import Modules
import { WebSocketServer } from 'ws';

// Import Services
import { storeMarketData } from "#store/marketDataStore.js";
import { updateQuote, updateDepth, isSnapReady, getState } from '#struct/marketState.js'

// Import Util
import { normalizeFeed, appendFeed } from "@pixelin-medium/utils";

function startMarketWS() {
    const wss = new WebSocketServer({ port: 5000 });

    console.log("Node WS server listening on ws://localhost:5000");

    wss.on("connection", (ws, req) => {
        console.log("Python connected:", req.socket.remoteAddress);

        ws.setMaxListeners(0);

        ws.on("message", (msg) => {

            const str = Buffer.isBuffer(msg) ? msg.toString() : msg;

            let parsed;

            try {

                parsed = JSON.parse(str);

            } catch {

                return;

            }

            if (!parsed) return;

            if (!parsed?.type || !parsed?.tk || !parsed?.data) return;

            // console.log(`Received ${type} data:`, data);

            console.log("Parsed: ", parsed)

            // Update struct
            if (parsed?.type === "QUOTE")
            {
                updateQuote({ tk: parsed?.tk, data: parsed?.data });

            }

            if (parsed?.type === "DEPTH") {

                updateDepth({ tk: parsed?.tk, data: parsed?.data });

            }

            // Get merged struct
            const { quote, depth } = getState(parsed?.tk);
            if (!quote) return;

            // Normalize (QUOTE or DEPTH)
            const normalized = normalizeFeed({ tk: parsed?.tk, quote, depth });
            if (!normalized) return;

            storeMarketData(normalized.token_name, normalized);


            console.log(
                "Stored:",
                normalized.token_name,
                "DEPTH:",
                depth ? "YES" : "NO"
            );

        });

        ws.on("close", () => console.log("Python disconnected"));
        ws.on("error", (err) => console.error("WS error:", err));
    });
}

export {
    startMarketWS,
};


