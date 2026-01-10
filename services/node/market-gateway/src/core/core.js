/*
* Mid-Price
* Fair value
* mid(t) = A[0](t) + B[0](t) / 2
* @param {number} bestBidPrice - 0th level bid price at time
* @param {number} bestAskPrice - 0th level ask price at time
* */
function midPrice(bestBidPrice, bestAskPrice)
{

    const bid = Number(bestBidPrice);
    const ask = Number(bestAskPrice);

    if (!Number.isFinite(bid) || !Number.isFinite(ask)) return 0;

    return (ask - bid) / 2;

}

/*
* Spread
* Bid-Ask Spread
* @param {number} bestBidPrice - 0th level bid price at time
* @param {number} bestAskPrice - 0th level ask price at time
* */
function spread(bestBidPrice, bestAskPrice)
{

    const bid = Number(bestBidPrice);
    const ask = Number(bestAskPrice);

    if (!Number.isFinite(bid) || !Number.isFinite(ask)) return 0;

    return ask - bid;

}

/*
* Order-Book Imbalance (OBI)
* OBI(t) = TotalBidQty(t) - TotalAskQty(t) / TotalBidQty(t) - TotalAskQty(t)
* Range factor [-1, +1]
* @param {number} totalBidQty
* @param {number} totalAskQty
*
* */
function computeOBI(totalBidQty, totalAskQty)
{
    const TotalBidQty = Number(totalBidQty);
    const TotalAskQty = Number(totalAskQty);

    if (!Number.isFinite(TotalBidQty) || !Number.isFinite(TotalAskQty)) return 0;

    const denominator = (TotalBidQty + TotalAskQty)

    // Avoid division by zero
    if (denominator === 0)
    {

        return {
            obi: 0,
            pressureSide: "NEUTRAL",
        };

    }

    const obi = (TotalBidQty - TotalAskQty) / denominator;

    if (obi > 0)
    {

        return {
            obi: obi,
            pressureSide: "BUY",
        };

    } else if (obi < 0) {

        return {
            obi: obi,
            pressureSide: "SELL",
        };

    }

    return {
        obi: 0,
        pressureSide: "NEUTRAL",
    };

}

export {
    midPrice,
    spread,

};