import axios from "axios";

async function getQuotes(baseUrl, token, queries) {

    try {

        // const joinedQuery = queries.join(",");
        //
        // console.log(joinedQuery);

        const url = `${baseUrl}/script-details/1.0/quotes/neosymbol/${queries}/all`;

        const { data } = await axios.get(url, {
            headers: {
                "Content-Type": "application/json",
                Authorization: token,
            },
        });

        return data;

    } catch (e) {

        console.error("Quote Fetch Error:", e.response?.data || e.message);

        return null;

    }

}

export { getQuotes };