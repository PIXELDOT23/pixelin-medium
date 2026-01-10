const marketData = new Map();


function storeMarketData(key, data) {

    if (!key || !data) return;

    marketData.set(key, data);

}

function getMarketData() {

    const obj = {};

    for (const [key, value] of marketData.entries())
    {

        obj[key] = value;

    }

    return obj;
}

function getByKey(key) {

    return marketData.get(key) || null;

}

function normalizeQuote(record) {
    const [quote] = record.data; // same as record.data[0]

    return {
        local: record.local,
        ...quote,
    };
}


export {
    storeMarketData,
    getMarketData,
    getByKey,
    normalizeQuote
};
