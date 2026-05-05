import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

const API_BASE = 'http://localhost:7776';

function Home() {
  const [loading, setLoading] = useState(true);
  const [usage, setUsage] = useState(null);
  const [history, setHistory] = useState([]);
  const [timeRange, setTimeRange] = useState('week');

  useEffect(() => {
    loadData();
  }, [timeRange]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [usageRes, providerRes, historyRes] = await Promise.all([
        fetch(`${API_BASE}/api/usage/tokens`),
        fetch(`${API_BASE}/api/usage/by-provider`),
        fetch(`${API_BASE}/api/history?limit=50`),
      ]);

      const usageData = await usageRes.json();
      const historyData = await historyRes.json();

      setUsage(usageData);
      setHistory(historyData.history || []);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  };

  const providerChartData = {
    labels: ['ElevenLabs', 'Brave API', 'Primary Model', 'Vision Model'],
    datasets: [
      {
        data: usage
          ? [
              usage.total_characters || 0,
              usage.total_brave_api_calls || 0,
              usage.total_primary_model_tokens || 0,
              usage.total_vision_model_tokens || 0,
            ]
          : [0, 0, 0, 0],
        backgroundColor: ['#1976d2', '#ff9800', '#d32f2f', '#388e3c'],
      },
    ],
  };

  const modelUsageData = {
    labels: ['Qwen3.5 Coder (Primary)', 'Qwen2.5 VL (Vision)'],
    datasets: [
      {
        label: 'Tokens Used',
        data: usage
          ? [usage.total_primary_model_tokens || 0, usage.total_vision_model_tokens || 0]
          : [0, 0],
        backgroundColor: ['#d32f2f', '#388e3c'],
      },
    ],
  };

  const timelineData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'API Calls',
        data: [12, 19, 8, 15, 22, 10, 14],
        borderColor: '#1976d2',
        backgroundColor: '#1976d2',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' },
    },
  };

  if (loading) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Token Manager</h1>
          <div style={{ textAlign: 'center' }}>Loading...</div>
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Token Manager</h1>
        <p>Monitor token usage across all services</p>
      </header>

      <div style={{ padding: '20px' }}>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <button onClick={() => setTimeRange('day')} style={timeRange === 'day' ? activeButton : buttonStyle}>Day</button>
          <button onClick={() => setTimeRange('week')} style={timeRange === 'week' ? activeButton : buttonStyle}>Week</button>
          <button onClick={() => setTimeRange('month')} style={timeRange === 'month' ? activeButton : buttonStyle}>Month</button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
          <div className="stat-card">
            <h3>Total Characters (TTS)</h3>
            <p className="stat-value elevenlabs">{usage?.total_characters?.toLocaleString() || 0}</p>
            <small>ElevenLabs usage</small>
          </div>

          <div className="stat-card">
            <h3>Brave API Calls</h3>
            <p className="stat-value brave">{usage?.total_brave_api_calls?.toLocaleString() || 0}</p>
            <small>Web search calls</small>
          </div>

          <div className="stat-card">
            <h3>Primary Model Tokens</h3>
            <p className="stat-value primary">{usage?.total_primary_model_tokens?.toLocaleString() || 0}</p>
            <small>Qwen3.5 Coder</small>
          </div>

          <div className="stat-card">
            <h3>Vision Model Tokens</h3>
            <p className="stat-value vision">{usage?.total_vision_model_tokens?.toLocaleString() || 0}</p>
            <small>Qwen2.5 VL</small>
          </div>

          <div className="stat-card total">
            <h3>Estimated Total</h3>
            <p className="stat-value">{usage?.total_combined_estimate?.toLocaleString() || 0}</p>
            <small>Combined estimate</small>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '30px' }}>
          <div className="chart-container">
            <h3>Usage by Provider</h3>
            <div style={{ height: '300px' }}>
              <Doughnut data={providerChartData} options={chartOptions} />
            </div>
          </div>

          <div className="chart-container">
            <h3>Model Usage Comparison</h3>
            <div style={{ height: '300px' }}>
              <Bar data={modelUsageData} options={chartOptions} />
            </div>
          </div>
        </div>

        <div className="chart-container" style={{ marginBottom: '30px' }}>
          <h3>Daily Timeline</h3>
          <div style={{ height: '300px' }}>
            <Line data={timelineData} options={chartOptions} />
          </div>
        </div>

        <div className="chart-container">
          <h3>Recent Usage History</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ccc' }}>
                <th style={{ textAlign: 'left', padding: '10px' }}>Timestamp</th>
                <th style={{ textAlign: 'left', padding: '10px' }}>Provider</th>
                <th style={{ textAlign: 'left', padding: '10px' }}>Metric</th>
                <th style={{ textAlign: 'right', padding: '10px' }}>Value</th>
              </tr>
            </thead>
            <tbody>
              {history.length === 0 ? (
                <tr><td colSpan="4" style={{ padding: '20px', textAlign: 'center' }}>No history data</td></tr>
              ) : (
                history.slice(0, 10).map((entry) => (
                  <tr key={entry.timestamp + entry.provider} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '10px' }}>{new Date(entry.timestamp).toLocaleString()}</td>
                    <td style={{ padding: '10px' }}>{entry.provider}</td>
                    <td style={{ padding: '10px' }}>{entry.metric_type}</td>
                    <td style={{ padding: '10px', textAlign: 'right' }}>{entry.value.toLocaleString()}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

const buttonStyle = {
  padding: '8px 16px',
  border: '1px solid #ccc',
  borderRadius: '4px',
  background: '#fff',
  cursor: 'pointer',
};

const activeButton = {
  ...buttonStyle,
  background: '#1976d2',
  color: '#fff',
  border: '1px solid #1976d2',
};

export default Home;
