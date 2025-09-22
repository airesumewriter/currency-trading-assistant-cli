import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';

const LivePrices = () => {
  const [prices, setPrices] = useState({
    EURUSD: 1.1745,
    GBPUSD: 1.3474,
    USDJPY: 147.912,
    XAUUSD: 1845.60
  });

  const [previousPrices, setPreviousPrices] = useState({});

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/prices');
    
    ws.onmessage = (event) => {
      const newPrices = JSON.parse(event.data);
      setPreviousPrices(prices);
      setPrices(newPrices);
    };

    return () => ws.close();
  }, []);

  const getTrendIcon = (pair) => {
    if (!previousPrices[pair]) return <TrendingFlat color="disabled" />;
    if (prices[pair] > previousPrices[pair]) return <TrendingUp color="success" />;
    if (prices[pair] < previousPrices[pair]) return <TrendingDown color="error" />;
    return <TrendingFlat color="disabled" />;
  };

  const getTrendColor = (pair) => {
    if (!previousPrices[pair]) return 'text.secondary';
    if (prices[pair] > previousPrices[pair]) return 'success.main';
    if (prices[pair] < previousPrices[pair]) return 'error.main';
    return 'text.secondary';
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        📊 Live Prices
      </Typography>
      <Grid container spacing={2}>
        {Object.entries(prices).map(([pair, price]) => (
          <Grid item xs={12} key={pair}>
            <Card variant="outlined">
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="h6">{pair}</Typography>
                  {getTrendIcon(pair)}
                </Box>
                <Typography 
                  variant="h4" 
                  color={getTrendColor(pair)}
                  sx={{ fontFamily: 'Monospace', fontWeight: 'bold' }}
                >
                  {price}
                </Typography>
                {previousPrices[pair] && (
                  <Typography variant="body2" color="text.secondary">
                    Previous: {previousPrices[pair]}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default LivePrices;
