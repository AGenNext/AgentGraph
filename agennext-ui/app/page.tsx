'use client';

import { useState } from 'react';
import { Header } from '@/components/Header';

interface Metric {
  label: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
}

const metrics: Metric[] = [
  { label: 'Active Agents', value: '24', change: '+12%', trend: 'up' },
  { label: 'Tasks Today', value: '156', change: '+8%', trend: 'up' },
  { label: 'API Calls', value: '12.4K', change: '+23%', trend: 'up' },
  { label: 'Avg Response', value: '1.2s', change: '-5%', trend: 'down' },
];

const recentActivity = [
  { type: 'agent', name: 'Research Agent', action: 'completed', time: '2 min ago' },
  { type: 'task', name: 'Data Sync #1234', action: 'completed', time: '5 min ago' },
  { type: 'team', name: 'Analysis Team', action: 'started', time: '10 min ago' },
  { type: 'approval', name: 'New Agent Request', action: 'pending', time: '15 min ago' },
];

const quickActions = [
  { icon: '🤖', label: 'New Agent', href: '/agents' },
  { icon: '📋', label: 'New Task', href: '/tasks' },
  { icon: '🔗', label: 'Integrations', href: '/integrations' },
  { icon: '📊', label: 'Reports', href: '/finance' },
];

export default function DashboardPage() {
  const [activity] = useState(recentActivity);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Header />
      
      <div style={{ flex: 1, overflow: 'auto', padding: 24, background: '#F8F9FA' }}>
        {/* Welcome */}
        <div style={{ marginBottom: 24 }}>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: '0 0 4px 0' }}>Good morning, John</h1>
          <p style={{ color: '#6B7280', margin: 0, fontSize: 14 }}>Here's what's happening with your agents today.</p>
        </div>

        {/* Quick Actions */}
        <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
          {quickActions.map(action => (
            <a
              key={action.label}
              href={action.href}
              style={{
                background: '#fff',
                border: '1px solid #E5E5E5',
                borderRadius: 8,
                padding: '12px 16px',
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                textDecoration: 'none',
                color: '#161616',
                fontSize: 13,
                fontWeight: 500,
                cursor: 'pointer',
                transition: 'all 0.15s ease',
              }}
            >
              <span style={{ fontSize: 18 }}>{action.icon}</span>
              {action.label}
            </a>
          ))}
        </div>

        {/* Metrics */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
          {metrics.map(metric => (
            <div key={metric.label} style={{ background: '#fff', borderRadius: 8, padding: 20, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>{metric.label}</div>
              <div style={{ fontSize: 28, fontWeight: 600, marginBottom: 4 }}>{metric.value}</div>
              <div style={{ fontSize: 12, color: metric.trend === 'up' ? '#10B981' : '#DA1E28' }}>
                {metric.change} vs last week
              </div>
            </div>
          ))}
        </div>

        {/* Two Column */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 24 }}>
          {/* Recent Activity */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <div style={{ padding: '16px 20px', borderBottom: '1px solid #E5E5E5', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: 14, fontWeight: 600, margin: 0 }}>Recent Activity</h3>
              <button style={{ fontSize: 12, color: '#0F62FE', background: 'none', border: 'none', cursor: 'pointer' }}>View all</button>
            </div>
            <div>
              {activity.map((item, i) => (
                <div key={i} style={{ padding: '12px 20px', borderBottom: i < activity.length - 1 ? '1px solid #F4F4F4' : 'none', display: 'flex', alignItems: 'center', gap: 12 }}>
                  <div style={{ width: 32, height: 32, borderRadius: 8, background: '#F4F4F4', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    {item.type === 'agent' ? '🤖' : item.type === 'task' ? '📋' : item.type === 'team' ? '👥' : '✅'}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 13, fontWeight: 500 }}>{item.name}</div>
                    <div style={{ fontSize: 12, color: '#6B7280' }}>{item.action}</div>
                  </div>
                  <div style={{ fontSize: 12, color: '#9CA3AF' }}>{item.time}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Agent Status */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <div style={{ padding: '16px 20px', borderBottom: '1px solid #E5E5E5' }}>
              <h3 style={{ fontSize: 14, fontWeight: 600, margin: 0 }}>Agent Status</h3>
            </div>
            <div style={{ padding: 16 }}>
              {[
                { label: 'Active', count: 18, color: '#10B981' },
                { label: 'Idle', count: 4, color: '#6B7280' },
                { label: 'Error', count: 2, color: '#DA1E28' },
              ].map(item => (
                <div key={item.label} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', background: item.color }} />
                    <span style={{ fontSize: 13 }}>{item.label}</span>
                  </div>
                  <span style={{ fontSize: 13, fontWeight: 600 }}>{item.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}