import React, { useState, useEffect } from 'react';
import { Typography, Box } from '@mui/material';
import { api } from '../services/api';

const LivePrices = () => {
  const [prices, setPrices] = useState({});

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const response = await api.getMultiplePrices('EURUSD,GBPUSD,USDJPY,AUDUSD,USDCAD');
        setPrices(response.data.prices);
      } catch (error) {
        console.error('Error fetching prices:', error);
        // Mock data as fallback
        setPrices({
          EURUSD: 1.1745,
          GBPUSD: 1.3474,
          USDJPY: 147.912,
          AUDUSD: 0.6550,
          USDCAD: 1.3550
        });
      }
    };

    fetchPrices();
    const interval = setInterval(fetchPrices, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const getTrendIcon = (pair, currentPrice) => {
    // Simple mock trend logic
    const trends = {
      EURUSD: '↗',
      GBPUSD: '↗', 
      USDJPY: '↘',
      AUDUSD: '→',
      USDCAD: '↘'
    };
    return trends[pair] || '→';
  };

  return (
    <Box>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        💰 LIVE PRICES
      </Typography>
      {Object.entries(prices).map(([pair, price]) => (
        <Box key={pair} sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="body1" sx={{ color: 'white', fontFamily: 'monospace' }}>
            {pair}:
          </Typography>
          <Typography 
            variant="body1" 
            sx={{ 
              color: getTrendIcon(pair) === '↗' ? '#4caf50' : 
                    getTrendIcon(pair) === '↘' ? '#f44336' : '#ff9800',
              fontFamily: 'monospace',
              fontWeight: 'bold'
            }}
          >
            {price} {getTrendIcon(pair)}
          </Typography>
        </Box>
      ))}
    </Box>
  );
};

export default LivePrices;
