function normalizeFeed({ tk, quote, depth }) {

    if (!tk || !quote) return null;

    return {
        local: new Date().toLocaleString(),
        token_name: `${depth.ts}`,
        tk,
        ts: quote.ts,
        e: quote.e,

        quote,
        depth,

        __ts: Date.now()
    };
}

export {
    normalizeFeed
};

