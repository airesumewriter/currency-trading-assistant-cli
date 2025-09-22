import React, { useState, useEffect } from 'react';
import { Typography, Box } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../services/api';

const PriceChart = ({ pair }) => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await api.getHistory(pair, 7);
        const history = response.data.history;
        
        // Convert history object to array for Recharts
        const data = Object.entries(history).map(([date, price]) => ({
          date: new Date(date).toLocaleDateString(),
          price: price
        }));
        
        setChartData(data.reverse()); // Show oldest to newest
      } catch (error) {
        console.error('Error fetching chart data:', error);
        // Mock data as fallback
        const mockData = [
          { date: 'Sep 16', price: 1.1700 },
          { date: 'Sep 17', price: 1.1720 },
          { date: 'Sep 18', price: 1.1750 },
          { date: 'Sep 19', price: 1.1740 },
          { date: 'Sep 20', price: 1.1760 },
          { date: 'Sep 21', price: 1.1770 },
          { date: 'Sep 22', price: 1.1745 },
        ];
        setChartData(mockData);
      }
    };

    fetchChartData();
  }, [pair]);

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
        📈 {pair} CHART (7 Days)
      </Typography>
      <Box sx={{ flex: 1, minHeight: 0 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
            <XAxis 
              dataKey="date" 
              stroke="#fff"
              fontSize={12}
            />
            <YAxis 
              stroke="#fff"
              domain={['dataMin - 0.002', 'dataMax + 0.002']}
              fontSize={12}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1a1a1a', 
                border: '1px solid #444',
                color: 'white',
                borderRadius: '4px'
              }}
              formatter={(value) => [`${value}`, 'Price']}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#4caf50" 
              strokeWidth={2}
              dot={{ fill: '#4caf50', strokeWidth: 2 }}
              activeDot={{ r: 4, fill: '#ff9800' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    </Box>
  );
};

export default PriceChart;
