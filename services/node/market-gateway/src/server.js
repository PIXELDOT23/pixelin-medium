// Import Modules
import express from 'express';

// Routes
import MarketRoute from "#api/market.route.js";

// Import Engine
import StartEngine from './Engine.js';

// Import Services
import { startMarketWS } from "#ws/marketWs.js";

// Props
const app = express();
const PORT = 4000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// market Route
app.use('/api', MarketRoute);

// Starting Engine
await StartEngine().catch(console.error);

// const server = http.createServer(app);

app.listen(PORT, () => {

    console.log(`Server started on port ${PORT}...`);

});

// WS Server for python feed
// startMarketWS(server);






