import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';

const Dashboard = () => {
  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        🎯 Currency Trading Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom>
              Welcome to Your Trading Dashboard!
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Backend connection: Testing...
            </Typography>
            <Typography variant="body2" sx={{ mt: 2 }}>
              🚀 React Frontend is running!<br/>
              ✅ Node.js v22.19.0 installed<br/>
              ✅ npm v10.9.3 working<br/>
              ⚡ Ready to connect to backend
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
