import React from 'react';
import { Typography, Box } from '@mui/material';

const TradingSignals = ({ pair, title = "TRADING SIGNALS", emoji = "⚡" }) => {
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        {emoji} {title}
      </Typography>
      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        backgroundColor: '#121212',
        border: '1px solid #333',
        borderRadius: 1
      }}>
        <Typography variant="body2" sx={{ color: '#666', textAlign: 'center' }}>
          {title} for {pair}
          <br />
          (TradingSignals in development)
        </Typography>
      </Box>
    </Box>
  );
};

export default TradingSignals;
