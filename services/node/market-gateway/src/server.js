// Import Modules
import express from 'express';
import http from 'node:http';

// Routes
import MarketRoute from "#api/market.route.js";

// Import Services
import { startMarketWS } from "#ws/marketWs.js";

// Props
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// market Route
app.use('/api', MarketRoute);

const server = http.createServer(app);

server.listen(4000, () => {

    console.log('Server started on port 5000...');

});

// WS Server for python feed
startMarketWS(server);





