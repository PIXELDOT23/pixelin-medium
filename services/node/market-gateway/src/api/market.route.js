// Import Modules
import { Router } from "express";

// Import Services
import { getMarketData } from "#store/marketDataStore.js";

// Props
const router = new Router();

// Market
router.get('/market', (req, res) => {

    res.status(200).json(getMarketData());

});


export default router;