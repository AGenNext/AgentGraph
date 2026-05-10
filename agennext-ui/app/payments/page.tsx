'use client';

import { useState } from 'react';

interface Transaction {
  id: string;
  agent: string;
  runtime: string;
  tokens: number;
  cost: number;
  status: 'completed' | 'pending' | 'failed';
  timestamp: string;
}

const transactions: Transaction[] = [
  { id: 't1', agent: 'Research Agent', runtime: 'AWS Bedrock', tokens: 125000, cost: 2.45, status: 'completed', timestamp: '2024-02-01 10:30' },
  { id: 't2', agent: 'Writer Agent', runtime: 'Azure AI Foundry', tokens: 89000, cost: 1.78, status: 'completed', timestamp: '2024-02-01 10:15' },
  { id: 't3', agent: 'Analyzer Agent', runtime: 'Vertex AI', tokens: 156000, cost: 3.12, status: 'completed', timestamp: '2024-02-01 09:45' },
  { id: 't4', agent: 'Research Agent', runtime: 'AWS Bedrock', tokens: 45000, cost: 0.89, status: 'pending', timestamp: '2024-02-01 09:30' },
  { id: 't5', agent: 'Triage Agent', runtime: 'LlamaIndex', tokens: 12000, cost: 0.24, status: 'failed', timestamp: '2024-02-01 09:15' },
];

const plans = [
  { name: 'Starter', price: 49, features: ['5 agents', '10K tokens/mo', 'Email support'] },
  { name: 'Pro', price: 199, features: ['25 agents', '100K tokens/mo', 'Priority support', 'API access'] },
  { name: 'Enterprise', price: 'Custom', features: ['Unlimited agents', 'Unlimited tokens', '24/7 support', 'Custom integrations', 'SLA'] },
];

export default function PaymentsPage() {
  const [activeTab, setActiveTab] = useState<'usage' | 'plans' | 'history'>('usage');
  const [selectedPlan, setSelectedPlan] = useState('Pro');
  
  const stats = {
    thisMonth: transactions.reduce((a, t) => a + t.cost, 0).toFixed(2),
    tokens: transactions.reduce((a, t) => a + t.tokens, 0).toLocaleString(),
    agents: 5,
    avgCostPerAgent: (transactions.reduce((a, t) => a + t.cost, 0) / 5).toFixed(2),
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Agent Payment Protocol</h1>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['usage', 'plans', 'history'] as const).map(t => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            style={{
              background: activeTab === t ? '#1A1A2E' : '#fff',
              color: activeTab === t ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'usage' ? 'Usage & Billing' : t === 'plans' ? 'Subscription Plans' : 'Transaction History'}
          </button>
        ))}
      </div>

      {activeTab === 'usage' ? (
        <>
          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>This Month</div>
              <div style={{ fontSize: 28, fontWeight: 600 }}>${stats.thisMonth}</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>Tokens Used</div>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{stats.tokens}</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>Active Agents</div>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{stats.agents}</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 12, color: '#6B7280', marginBottom: 8 }}>Avg Cost/Agent</div>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>${stats.avgCostPerAgent}</div>
            </div>
          </div>

          {/* Runtime Breakdown */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20, marginBottom: 24 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Cost by Runtime</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
              {[
                { runtime: 'AWS Bedrock', cost: 3.34, pct: 45 },
                { runtime: 'Azure AI Foundry', cost: 2.12, pct: 28 },
                { runtime: 'Vertex AI', cost: 1.55, pct: 21 },
                { runtime: 'LlamaIndex', cost: 0.45, pct: 6 },
              ].map(item => (
                <div key={item.runtime} style={{ background: '#F8F9FA', padding: 16, borderRadius: 8 }}>
                  <div style={{ fontSize: 16, fontWeight: 600 }}>${item.cost}</div>
                  <div style={{ fontSize: 12, color: '#6B7280' }}>{item.runtime}</div>
                  <div style={{ fontSize: 11, color: '#10B981' }}>{item.pct}%</div>
                </div>
              ))}
            </div>
          </div>

          {/* Auto-recharge */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Auto-Recharge</h3>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 16, background: '#F8F9FA', borderRadius: 8 }}>
              <div>
                <div style={{ fontSize: 14, fontWeight: 500 }}>Current Balance</div>
                <div style={{ fontSize: 12, color: '#6B7280' }}>Auto-recharge when below $10</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: 20, fontWeight: 600 }}>$45.00</div>
                <button style={{ fontSize: 12, color: '#0F62FE', background: 'none', border: 'none', cursor: 'pointer' }}>Add funds</button>
              </div>
            </div>
          </div>
        </>
      ) : activeTab === 'plans' ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {plans.map(plan => (
            <div 
              key={plan.name}
              style={{ 
                background: '#fff', 
                borderRadius: 12, 
                border: selectedPlan === plan.name ? '2px solid #667EEA' : '1px solid #E5E5E5', 
                padding: 24,
                cursor: 'pointer',
                position: 'relative',
              }}
              onClick={() => setSelectedPlan(plan.name)}
            >
              {plan.name === 'Pro' && (
                <div style={{ position: 'absolute', top: -10, right: 16, background: '#667EEA', color: '#fff', padding: '4px 12px', borderRadius: 12, fontSize: 11 }}>
                  Popular
                </div>
              )}
              <div style={{ fontSize: 20, fontWeight: 600, marginBottom: 8 }}>{plan.name}</div>
              <div style={{ fontSize: 32, fontWeight: 700, marginBottom: 16 }}>
                {plan.price === 'Custom' ? 'Custom' : `$${plan.price}`}
                {plan.price !== 'Custom' && <span style={{ fontSize: 14, fontWeight: 400, color: '#6B7280' }}>/mo</span>}
              </div>
              <ul style={{ padding: 0, margin: '0 0 24px 0', listStyle: 'none' }}>
                {plan.features.map((f, i) => (
                  <li key={i} style={{ padding: '6px 0', fontSize: 13, color: '#6B7280', display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span>✓</span> {f}
                  </li>
                ))}
              </ul>
              <button style={{ 
                width: '100%', 
                background: selectedPlan === plan.name ? '#667EEA' : '#F8F9FA', 
                color: selectedPlan === plan.name ? '#fff' : '#525252',
                border: '1px solid #E5E5E5',
                padding: '12px 0', 
                borderRadius: 8, 
                fontSize: 14, 
                fontWeight: 500,
                cursor: 'pointer',
              }}>
                {plan.price === 'Custom' ? 'Contact Sales' : 'Subscribe'}
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>AGENT</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RUNTIME</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TOKENS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>COST</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TIME</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(t => (
                <tr key={t.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{t.agent}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{t.runtime}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{t.tokens.toLocaleString()}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>${t.cost.toFixed(2)}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: t.status === 'completed' ? '#10B981' : t.status === 'pending' ? '#F59E0B' : '#DA1E28', fontSize: 12, fontWeight: 500 }}>
                      {t.status}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{t.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}