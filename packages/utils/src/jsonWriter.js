// Import Modules
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url'

const safeDate = new Date().toISOString().split("T")[0];

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const baseDir = path.join(__dirname, "../../../data/market/USDINR");

// Initialize empty array file if missing
if (!fs.existsSync(baseDir))
{

    fs.mkdirSync(baseDir, { recursive: true });

}

function appendFeed(data)
{

    try {

        const filePath = `USDINR_market_feed_${safeDate}.json`;

        const file_location = path.join(baseDir, filePath);

        // Ensure directory path exists (recursive)
        fs.mkdirSync(path.dirname(file_location), { recursive: true });

        let arr = [];

        if (fs.existsSync(file_location))
        {

            const raw = fs.readFileSync(file_location, 'utf-8');

            arr = JSON.parse(raw);

        }

        // append new data
        arr.push(data);

        // write back pretty formatted
        fs.writeFileSync(file_location, JSON.stringify(arr, null, 2), 'utf-8');

    } catch (e) {

        console.error("Error writing JSON", e);

    }

}

export {
    appendFeed
};