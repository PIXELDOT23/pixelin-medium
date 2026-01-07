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

export {
    storeMarketData,
    getMarketData,
    getByKey
};
