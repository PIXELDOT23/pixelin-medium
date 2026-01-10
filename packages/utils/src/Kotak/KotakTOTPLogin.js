// Import Import Modules
import axios from "axios";

/**
 *
 * Kotak Unified Login – Step 1 + Step 2 combined
 *
 * @param {Object} params
 *
 * @param {string} params.token - OAuth access token (from /oauth/token)
 *
 * @param {string} params.mobileNumber - Registered mobile number (+91...)
 *
 * @param {string} params.ucc - Client UCC code
 *
 * @param {string} params.totp - Live TOTP code (valid for 30 seconds)
 *
 * @param {string} params.mpin - 6-digit MPIN
 *
 * @returns {Promise<Object>} Final session object { session_token, ucc, user_name }
 *
 */

// Kotak API TOTP Login
async function KotakTOTPLogin({ token, mobileNumber, ucc, totp, mpin }) {

    try {

        // || TOTP Login -----------------------------------------------------------------------------------------------
        const TOTPConfig = {
            method: 'post',
            maxBodyLength: Infinity,
            url: 'https://mis.kotaksecurities.com/login/1.0/tradeApiLogin',
            headers: {
                'Authorization': `${ token }`,
                'neo-fin-key': 'neotradeapi',
                'Content-Type': 'application/json'
            },
            data : { mobileNumber, ucc, totp }
        };

        const step_1 = await axios(TOTPConfig);

        const { sid, token: auth } = step_1.data.data;

        console.log("Step: 1 || ✅ TOTP Login Success");

        // || TOTP Login -----------------------------------------------------------------------------------------------

        // || Validate MPIN --------------------------------------------------------------------------------------------
        const ValidateConfig = {
            method: 'post',
            maxBodyLength: Infinity,
            url: 'https://mis.kotaksecurities.com/login/1.0/tradeApiValidate',
            headers: {
                Authorization: `${ token }`,
                'accept': 'application/json',
                'neo-fin-key': 'neotradeapi',
                'Content-Type': 'application/json',
                sid,
                auth,
            },
            data : { mpin }
        };

        const step_2 = await axios(ValidateConfig);

        console.log("Step: 2 || ✅ MPIN Validate success");

        // || Validate MPIN --------------------------------------------------------------------------------------------

        return step_2.data;

    } catch (e) {

        if (e.response) {

            console.error("❌ Kotak Login Error:", e.response.status, e.response.data);

            throw e.response.data;

        } else {

            console.error("❌ Network/Error:", e.message);

            throw e;

        }


    }

}

// Export
export { KotakTOTPLogin };