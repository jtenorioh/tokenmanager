import React from 'react';
import { Card, Grid, Typography } from '@mui/material';

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Token Manager</h1>
        <p>Monitor token usage across all services</p>
      </header>
      
      <main className="App-main">
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <div className="stat-card">
                <Typography variant="h5">Total Tokens</Typography>
                <Typography variant="h2" color="primary">0</Typography>
              </div>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <div className="stat-card">
                <Typography variant="h5">Primary Model</Typography>
                <Typography variant="h2" color="secondary">0</Typography>
              </div>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <div className="stat-card">
                <Typography variant="h5">Vision Model</Typography>
                <Typography variant="h2" color="success.main">0</Typography>
              </div>
            </Card>
          </Grid>
        </Grid>
      </main>
    </div>
  );
}

export default Home;
