'use client';

import { useState } from 'react';

interface Metric {
  name: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  format: 'number' | 'currency' | 'percent';
}

const metrics: Metric[] = [
  { name: 'Total API Calls', value: '1.2M', change: '+23%', trend: 'up', format: 'number' },
  { name: 'Active Agents', value: '24', change: '+12%', trend: 'up', format: 'number' },
  { name: 'Avg Response Time', value: '1.2s', change: '-15%', trend: 'down', format: 'number' },
  { name: 'Daily Cost', value: '$2,450', change: '+8%', trend: 'up', format: 'currency' },
  { name: 'Success Rate', value: '99.2%', change: '+0.5%', trend: 'up', format: 'percent' },
  { name: 'Active Users', value: '156', change: '+5%', trend: 'up', format: 'number' },
];

const hourlyData = [
  { hour: '00:00', calls: 1200, latency: 1.1 },
  { hour: '04:00', calls: 800, latency: 1.0 },
  { hour: '08:00', calls: 4500, latency: 1.3 },
  { hour: '12:00', calls: 8200, latency: 1.5 },
  { hour: '16:00', calls: 9800, latency: 1.6 },
  { hour: '20:00', calls: 5600, latency: 1.2 },
];

const topAgents = [
  { name: 'Research Agent', calls: 45200, cost: 890, lat: 1.2 },
  { name: 'Writer Agent', calls: 32100, cost: 620, lat: 0.9 },
  { name: 'Analyzer Agent', calls: 28400, cost: 540, lat: 1.4 },
  { name: 'Triage Agent', calls: 19300, cost: 380, lat: 0.8 },
];

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('24h');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Analytics</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Real-time metrics & dashboards</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {['1h', '6h', '24h', '7d', '30d'].map(t => (
            <button
              key={t}
              onClick={() => setTimeRange(t)}
              style={{
                background: timeRange === t ? '#0F62FE' : '#fff',
                color: timeRange === t ? '#fff' : '#525252',
                border: '1px solid #E5E5E5',
                padding: '6px 12px',
                borderRadius: 6,
                fontSize: 12,
                cursor: 'pointer',
              }}
            >
              {t}
            </button>
          ))}
          <button style={{ background: '#10B981', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
            Live
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 16, marginBottom: 24 }}>
        {metrics.map(m => (
          <div key={m.name} style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
            <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>{m.name}</div>
            <div style={{ fontSize: 24, fontWeight: 600, marginBottom: 4 }}>{m.value}</div>
            <div style={{ fontSize: 12, color: m.trend === 'up' ? '#10B981' : '#DA1E28' }}>
              {m.change} vs last period
            </div>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16, marginBottom: 24 }}>
        {/* API Calls Chart */}
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>API Calls & Latency</h3>
          <div style={{ height: 200, display: 'flex', alignItems: 'flex-end', gap: 8 }}>
            {hourlyData.map((d, i) => (
              <div key={d.hour} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{ width: '100%', background: '#667EEA', borderRadius: '4px 4px 0 0', height: (d.calls / 100) }}>
                </div>
                <div style={{ fontSize: 10, color: '#6B7280', marginTop: 4 }}>{d.hour}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Agents */}
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Top Agents</h3>
          {topAgents.map(agent => (
            <div key={agent.name} style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 13 }}>{agent.name}</span>
                <span style={{ fontSize: 13, fontWeight: 500 }}>{agent.calls.toLocaleString()} calls</span>
              </div>
              <div style={{ height: 6, background: '#F4F4F4', borderRadius: 3, overflow: 'hidden' }}>
                <div style={{ height: '100%', width: `${agent.calls / 500}%`, background: '#667EEA', borderRadius: 3 }} />
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4, fontSize: 11, color: '#6B7280' }}>
                <span>${agent.cost}</span>
                <span>{agent.lat}s avg</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Breakdown */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Cost by Runtime</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
          {[
            { runtime: 'AWS Bedrock', cost: '$890', pct: 36 },
            { runtime: 'Azure AI Foundry', cost: '$620', pct: 25 },
            { runtime: 'Vertex AI', cost: '$540', pct: 22 },
            { runtime: 'Other', cost: '$400', pct: 17 },
          ].map(item => (
            <div key={item.runtime} style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontWeight: 600 }}>{item.cost}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>{item.runtime}</div>
              <div style={{ fontSize: 11, color: '#10B981' }}>{item.pct}%</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}