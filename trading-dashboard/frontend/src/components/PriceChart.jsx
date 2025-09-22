import React from 'react';
import { Typography, Box } from '@mui/material';

const PriceChart = ({ pair }) => {
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        📈 {pair} CHART
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
        <Typography variant="body2" sx={{ color: '#666' }}>
          Chart for {pair} will be displayed here
        </Typography>
      </Box>
    </Box>
  );
};

export default PriceChart;
