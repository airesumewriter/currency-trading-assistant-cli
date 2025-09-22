import React from 'react';
import { Typography, Box, LinearProgress } from '@mui/material';

const AISentiment = ({ pair }) => {
  const sentiment = {
    sentiment: 'BULLISH',
    confidence: 78,
    analysis: 'Strong upward momentum with RSI at 65'
  };

  return (
    <Box>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        🤖 AI SENTIMENT
      </Typography>
      <Box sx={{ textAlign: 'center' }}>
        <Typography 
          variant="h4" 
          sx={{ 
            color: sentiment.sentiment === 'BULLISH' ? '#4caf50' : '#f44336',
            mb: 1,
            fontWeight: 'bold'
          }}
        >
          {sentiment.sentiment} ({sentiment.confidence}%)
        </Typography>
        <LinearProgress 
          variant="determinate" 
          value={sentiment.confidence} 
          sx={{ 
            height: 10, 
            borderRadius: 5,
            mb: 2,
            backgroundColor: '#2d2d2d',
            '& .MuiLinearProgress-bar': {
              backgroundColor: sentiment.sentiment === 'BULLISH' ? '#4caf50' : '#f44336'
            }
          }}
        />
        <Typography variant="body2" sx={{ color: 'white', fontStyle: 'italic' }}>
          {sentiment.analysis}
        </Typography>
      </Box>
    </Box>
  );
};

export default AISentiment;
