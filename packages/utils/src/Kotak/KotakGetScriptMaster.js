// Import Modules
import axios from "axios";

// Import Helpers
import { parseCSVFromURL } from '../helpers/CSVParser.js';

/**
 * Fetch and optionally parse Scrip Master CSVs
 *
 * @param {Object} params
 * @param {string} params.baseUrl - Base URL from /tradeApiValidate response
 * @param {string} params.authToken - NEO API token
 * @param {boolean} [params.parseCSV=false] - If true, parse specific segment
 * @param {string} [params.segment="nse_fo"] - Exchange segment (nse_fo, bse_cm)
 *
 * @returns {Promise<Object>} Object with URLs and optionally parsed JSON
 */

async function KotakGetScriptMaster({ baseUrl, authToken, parseCSV = false, segment = "cde_fo" }) {

    try {

        const GetScriptConfig = {
            method: "get",
            maxBodyLength: Infinity,
            url: `${baseUrl}/script-details/1.0/masterscrip/file-paths`,
            headers: {
                Authorization: authToken,
            }
        };

        const { data } = await axios(GetScriptConfig);

        console.log("Layer", data);

        const { filesPaths, baseFolder } = data.data;

        console.log("✅ Scrip Master URLs fetched successfully", filesPaths);

        if (!parseCSV) return { filePaths: filesPaths, baseFolder };

        const targetFile = filesPaths.find((url) => url.includes(segment));
        if (!targetFile) return new Error(`Segment CSV not found for: ${segment}`);

        console.log(`📥 Parsing Scrip Master for: ${segment}`);
        const parsedData = await parseCSVFromURL(targetFile);

        // Optional: Auto-filter USDINR contracts for your bot
        const usdInrFutures = parsedData.filter((r) =>
            {

                return r.pInstType.includes('FUTCUR') && r.pSymbolName.includes("USDINR");

            }
        );

        console.log(`✅ Parsed ${usdInrFutures.length} USDINR instruments`, usdInrFutures);

        return { filePaths: filesPaths, baseFolder, usdInrFutures };

    } catch (e) {

        if (e.response) {

            console.error("❌ Kotak Scrip Master Error:", e.response.status, e.response.data);

            throw e.response.data;

        } else {

            console.error("❌ Network/Error:", e.message);

            throw e;

        }

    }

}

export { KotakGetScriptMaster };