const snapReady = new Map(); // tk → { quote: bool, depth: bool }

const quoteState = new Map();
const depthState = new Map();

// Quote
function updateQuote({ tk, data })
{

    if (!tk) return null;

    const book = quoteState.get(tk) || {};

    for (const [k, v] of Object.entries(data || {}))
    {

        if (k === "ftm0" || k === "dtm1" || k === "name") continue;

        book[k] = v;

    }

    book.__ts = Date.now() / 1000;
    quoteState.set(tk, book);

    const snap = snapReady.get(tk) || {};
    if (data.request_type === "SNAP") snap.quote = true;
    snapReady.set(tk, snap);

}

// Depth
function updateDepth({ tk, data })
{

    if (!tk || !data) return null;

    const book = depthState.get(tk) || {};

    for (const [k, v] of Object.entries(data || {})) {

        if (k === "ftm0" || k === "dtm1" || k === "name") continue;

        book[k] = v;

    }

    book.__ts = Date.now() / 1000;
    depthState.set(tk, book);

    const snap = snapReady.get(tk) || {};
    if (data.request_type === "SNAP") snap.depth = true;
    snapReady.set(tk, snap);

}

// Check Snap
function isSnapReady(tk) {

    const s = snapReady.get(tk);

    return !!(s?.quote && s?.depth);

}

function getState(tk)
{

    return {
        quote: quoteState.get(tk) || {},
        depth: depthState.get(tk) || {},
    };

}

const MAX_SKEW_MS = 1000;

function canMerge(q, d) {

    return q && d && Math.abs(q.__ts - d.__ts) < MAX_SKEW_MS;

}


export {
    updateQuote,
    updateDepth,
    isSnapReady,
    getState,
    canMerge
};
