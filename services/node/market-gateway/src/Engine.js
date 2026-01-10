import readline from "node:readline/promises";
import cron from "node-cron";

// Import utils
import { KotakTOTPLogin, getQuotes, appendFeed } from '@pixelin-medium/utils'

import { normalizeQuote } from "#store/marketDataStore.js";

// Function to get timestamp
const timestamp = () => new Date().toLocaleString();

const Token = "f0b5adb4-2e5f-4f41-8804-2b951e485bb2"
const QUOTE = ["cde_fo|2932"]

async function startEngine()
{

    console.log("🔐 Logging into Kotak...");

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    // Get TOTP
    const TOTP = await rl.question("Enter TOTP: ");

    rl.close();

    const sessionLogin = await KotakTOTPLogin({
        token: Token,
        mobileNumber: "+919597040027",
        ucc: "YGY9G",
        totp: TOTP.trim(),
        mpin: "192001",
    });

    console.log("Session: ", sessionLogin);

    const { token, baseUrl } = sessionLogin.data;

    // Define market close time
    const closeTime = new Date;

    closeTime.setHours(process.env.MARKET_CLOSE_HOUR || 17);

    closeTime.setMinutes(process.env.MARKET_CLOSE_MINUTE || 15);

    closeTime.setSeconds(0);

    // Define Market Start Time
    const startTime =  new Date;

    startTime.setHours(9);

    startTime.setMinutes(15);

    startTime.setSeconds(0);

    const delayUntilStart = startTime - new Date();

    setTimeout(() => {

        cron.schedule("*/1 * * * * *", async () => {

            const now = new Date();

            if (now >= closeTime)
            {

                console.log("🔒 Market closed. Stopping recording.")

                process.exit(0);

            } else if (now >= startTime) {

                console.log(`${timestamp()} ⌛ Fetching live quotes... `)

                const quotes = await getQuotes(baseUrl, Token, QUOTE);

                if (!quotes) return null;

                const record = {
                    local: timestamp(),
                    data: quotes,
                };

                const normalized = normalizeQuote(record);

                appendFeed(normalized);

                console.log(normalized);

            }

        });

    }, delayUntilStart);

}

await startEngine();

export default startEngine;