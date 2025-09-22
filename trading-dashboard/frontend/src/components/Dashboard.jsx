import React, { useState } from 'react';
import { Grid, Paper, Box, Tabs, Tab, Typography } from '@mui/material';
import PriceChart from './PriceChart';
import LivePrices from './LivePrices';
import AISentiment from './AISentiment';
import AIChat from './AIChat';
import TradingPanel from './TradingPanel';
import TradingSignals from './TradingSignals';

const Dashboard = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [selectedPair, setSelectedPair] = useState('EURUSD');

  const currencyPairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'];

  return (
    <Box sx={{ p: 2, backgroundColor: '#0a0a0a', minHeight: '100vh', color: 'white' }}>
      {/* Header with Currency Pairs */}
      <Box sx={{ mb: 3, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h4" sx={{ color: 'white', mb: 1, fontWeight: 'bold' }}>
          🎯 TRADING DASHBOARD
        </Typography>
        <Tabs
          value={selectedTab}
          onChange={(e, newValue) => {
            setSelectedTab(newValue);
            setSelectedPair(currencyPairs[newValue]);
          }}
          sx={{
            '& .MuiTab-root': { 
              color: 'white', 
              fontWeight: 'bold',
              fontSize: '1.1rem'
            },
            '& .Mui-selected': { 
              color: '#4caf50',
              backgroundColor: '#1e1e1e'
            }
          }}
        >
          {currencyPairs.map((pair) => (
            <Tab key={pair} label={pair} />
          ))}
        </Tabs>
      </Box>

      {/* Main Grid - 70/30 Split */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {/* Left Panel - Chart (70%) */}
        <Grid item xs={12} md={8.4}>
          <Paper sx={{ 
            p: 2, 
            height: '400px', 
            backgroundColor: '#1a1a1a',
            border: '1px solid #333'
          }}>
            <PriceChart pair={selectedPair} />
          </Paper>
        </Grid>

        {/* Right Panel - Live Prices & AI Sentiment (30%) */}
        <Grid item xs={12} md={3.6}>
          <Grid container spacing={2} direction="column">
            <Grid item>
              <Paper sx={{ 
                p: 2, 
                backgroundColor: '#1a1a1a',
                border: '1px solid #333'
              }}>
                <LivePrices />
              </Paper>
            </Grid>
            <Grid item>
              <Paper sx={{ 
                p: 2, 
                backgroundColor: '#1a1a1a',
                border: '1px solid #333'
              }}>
                <AISentiment pair={selectedPair} />
              </Paper>
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      {/* Middle Section - AI Assistant & Trading Panel */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {/* AI Trading Assistant */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ 
            p: 2, 
            height: '250px', 
            backgroundColor: '#1a1a1a',
            border: '1px solid #333'
          }}>
            <AIChat pair={selectedPair} />
          </Paper>
        </Grid>

        {/* Trading Panel */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ 
            p: 2, 
            height: '250px', 
            backgroundColor: '#1a1a1a',
            border: '1px solid #333'
          }}>
            <TradingPanel pair={selectedPair} />
          </Paper>
        </Grid>
      </Grid>

      {/* Trading Signals */}
      <Paper sx={{ 
        p: 2, 
        backgroundColor: '#1a1a1a',
        border: '1px solid #333'
      }}>
        <TradingSignals />
      </Paper>
    </Box>
  );
};

export default Dashboard;
