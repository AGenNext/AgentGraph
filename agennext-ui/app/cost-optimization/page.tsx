'use client';

import { useState } from 'react';

interface CostOptimizer {
  id: string;
  name: string;
  type: 'routing' | 'caching' | 'batch' | 'quantization' | 'prompt';
  description: string;
  potentialSavings: number;
  implementation: 'automatic' | 'manual';
  status: 'active' | 'available' | 'planned';
}

const costOptimizers: CostOptimizer[] = [
  { id: 'c1', name: 'Smart Model Routing', type: 'routing', description: 'Route simple queries to cheaper models', potentialSavings: 45, implementation: 'automatic', status: 'active' },
  { id: 'c2', name: 'Response Caching', type: 'caching', description: 'Cache repeated queries', potentialSavings: 35, implementation: 'automatic', status: 'active' },
  { id: 'c3', name: 'Batch Processing', type: 'batch', description: 'Process requests in batches', potentialSavings: 28, implementation: 'automatic', status: 'available' },
  { id: 'c4', name: 'Prompt Compression', type: 'prompt', description: 'Reduce token usage', potentialSavings: 22, implementation: 'manual', status: 'active' },
  { id: 'c5', name: 'Model Quantization', type: 'quantization', description: 'Use quantized models', potentialSavings: 40, implementation: 'automatic', status: 'planned' },
  { id: 'c6', name: 'Streaming Optimization', type: 'routing', description: 'Early token streaming', potentialSavings: 15, implementation: 'automatic', status: 'active' },
];

interface CostSaving {
  id: string;
  strategy: string;
  saved: number;
  percentage: number;
  trend: number[];
}

const costSavings: CostSaving[] = [
  { id: 'cs1', strategy: 'Smart Routing', saved: 2450, percentage: 38, trend: [20, 25, 30, 35, 38] },
  { id: 'cs2', strategy: 'Response Caching', saved: 1820, percentage: 28, trend: [10, 15, 20, 25, 28] },
  { id: 'cs3', strategy: 'Prompt Compression', saved: 890, percentage: 14, trend: [5, 8, 10, 12, 14] },
  { id: 'cs4', strategy: 'Streaming', saved: 420, percentage: 6, trend: [2, 3, 4, 5, 6] },
];

const usageByModel = [
  { model: 'GPT-4o', input: 45000000, output: 125000000, cost: 2250 },
  { model: 'Claude 3.5 Sonnet', input: 28000000, output: 84000000, cost: 1120 },
  { model: 'Gemini 1.5 Pro', input: 15000000, output: 45000000, cost: 375 },
  { model: 'Claude 3 Haiku', input: 8000000, output: 24000000, cost: 120 },
  { model: 'Llama 3.1 70B', input: 5000000, output: 15000000, cost: 85 },
];

export default function CostOptimizationPage() {
  const [tab, setTab] = useState<'overview' | 'optimizers' | 'savings'>('overview');
  
  const totalSavings = costSavings.reduce((a, c) => a + c.saved, 0);
  const savingsPercentage = ((totalSavings / (totalSavings + 4580)) * 100).toFixed(1);
  const potentialSavings = costOptimizers.filter(c => c.status !== 'active').reduce((a, c) => a + c.potentialSavings, 0);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>LLM Cost Optimization</h1>
        <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Reduce AI spend by up to 65%</p>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>${totalSavings.toLocaleString()}</div>
          <div style={{ fontSize: 12, color: '#10B981' }}>Monthly Savings</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{savingsPercentage}%</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Savings Rate</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>${potentialSavings}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Potential</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>${(4580 - totalSavings).toLocaleString()}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Net Cost</div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['overview', 'optimizers', 'savings'] as const).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              background: tab === t ? '#1A1A2E' : '#fff',
              color: tab === t ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'overview' ? 'Overview' : t === 'optimizers' ? 'Optimizers' : 'Savings Breakdown'}
          </button>
        ))}
      </div>

      {tab === 'overview' ? (
        <>
          {/* Savings Trend */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20, marginBottom: 24 }}>
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 16 }}>Savings Trend (Last 5 Months)</h3>
            <div style={{ height: 150, display: 'flex', alignItems: 'flex-end', gap: 32, padding: '0 20px' }}>
              {['Jan', 'Feb', 'Mar', 'Apr', 'May'].map((month, i) => (
                <div key={month} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ height: 100, width: '100%', display: 'flex', alignItems: 'flex-end', justifyContent: 'center', gap: 4 }}>
                    {costSavings.map(s => (
                      <div 
                        key={s.id} 
                        style={{ 
                          width: 16, 
                          height: s.trend[i] * 3, 
                          background: s.id === 'cs1' ? '#667EEA' : s.id === 'cs2' ? '#10B981' : s.id === 'cs3' ? '#F59E0B' : '#DA1E28',
                          borderRadius: '2px 2px 0 0',
                        }} 
                      />
                    ))}
                  </div>
                  <div style={{ fontSize: 11, color: '#6B7280', marginTop: 8 }}>{month}</div>
                </div>
              ))}
            </div>
            <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginTop: 12 }}>
              {costSavings.map(s => (
                <div key={s.id} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 10 }}>
                  <span style={{ width: 8, height: 8, borderRadius: 2, background: s.id === 'cs1' ? '#667EEA' : s.id === 'cs2' ? '#10B981' : s.id === 'cs3' ? '#F59E0B' : '#DA1E28' }} />
                  {s.strategy}
                </div>
              ))}
            </div>
          </div>

          {/* Usage by Model */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>MODEL</th>
                  <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: 11, color: '#6B7280' }}>INPUT TOKENS</th>
                  <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: 11, color: '#6B7280' }}>OUTPUT TOKENS</th>
                  <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: 11, color: '#6B7280' }}>COST ($)</th>
                </tr>
              </thead>
              <tbody>
                {usageByModel.map(m => (
                  <tr key={m.model} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{m.model}</td>
                    <td style={{ padding: '14px 16px', textAlign: 'right', fontSize: 12, fontFamily: 'monospace' }}>{(m.input / 1000000).toFixed(1)}M</td>
                    <td style={{ padding: '14px 16px', textAlign: 'right', fontSize: 12, fontFamily: 'monospace' }}>{(m.output / 1000000).toFixed(1)}M</td>
                    <td style={{ padding: '14px 16px', textAlign: 'right', fontWeight: 600 }}>${m.cost}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : tab === 'optimizers' ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {costOptimizers.map(opt => (
            <div key={opt.id} style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                <div>
                  <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>{opt.name}</div>
                  <div style={{ fontSize: 12, color: '#6B7280' }}>{opt.description}</div>
                </div>
                <span style={{ 
                  background: opt.status === 'active' ? '#10B98120' : opt.status === 'available' ? '#F59E0B20' : '#6B728020',
                  color: opt.status === 'active' ? '#10B981' : opt.status === 'available' ? '#F59E0B' : '#6B7280',
                  padding: '4px 10px',
                  borderRadius: 6,
                  fontSize: 11,
                  fontWeight: 500,
                  textTransform: 'capitalize',
                }}>
                  {opt.status}
                </span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', gap: 16 }}>
                  <div>
                    <div style={{ fontSize: 11, color: '#6B7280' }}>Savings</div>
                    <div style={{ fontSize: 20, fontWeight: 600, color: '#10B981' }}>{opt.potentialSavings}%</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 11, color: '#6B7280' }}>Type</div>
                    <div style={{ fontSize: 12, textTransform: 'capitalize' }}>{opt.type}</div>
                  </div>
                </div>
                <div>
                  <span style={{ fontSize: 10, color: '#6B7280' }}>
                    {opt.implementation === 'automatic' ? '⚡ Auto' : '👤 Manual'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STRATEGY</th>
                <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: 11, color: '#6B7280' }}>SAVED ($)</th>
                <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: 11, color: '#6B7280' }}>PERCENTAGE</th>
                <th style={{ padding: '12px 16px', textAlign: 'right', fontSize: 11, color: '#6B7280' }}>TREND</th>
              </tr>
            </thead>
            <tbody>
              {costSavings.map(s => (
                <tr key={s.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{s.strategy}</td>
                  <td style={{ padding: '14px 16px', textAlign: 'right', fontWeight: 600, color: '#10B981' }}>${s.saved}</td>
                  <td style={{ padding: '14px 16px', textAlign: 'right', fontSize: 12 }}>{s.percentage}%</td>
                  <td style={{ padding: '14px 16px', textAlign: 'right', fontSize: 12 }}>
                    <span style={{ color: s.trend[s.trend.length - 1] > s.trend[0] ? '#10B981' : '#DA1E28' }}>
                      {s.trend[s.trend.length - 1] > s.trend[0] ? '↑' : '↓'} {s.trend[s.trend.length - 1] - s.trend[0]}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Recommendations */}
      <div style={{ marginTop: 24, background: 'linear-gradient(135deg, #667EEA20 0%, #764BA220 100%)', borderRadius: 12, padding: 24 }}>
        <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 16 }}>💡 Recommendations for Additional Savings</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          <div style={{ background: 'rgba(255,255,255,0.8)', padding: 16, borderRadius: 8 }}>
            <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Enable Batch Processing</div>
            <div style={{ fontSize: 12, color: '#6B7280' }}>Process non-urgent requests in batches for 28% savings</div>
            <div style={{ fontSize: 20, fontWeight: 600, color: '#10B981', marginTop: 8 }}>+$1,120/mo</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.8)', padding: 16, borderRadius: 8 }}>
            <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Switch to Haiku for Simple Tasks</div>
            <div style={{ fontSize: 12, color: '#6B7280' }}>Route 40% of queries to cheaper model</div>
            <div style={{ fontSize: 20, fontWeight: 600, color: '#10B981', marginTop: 8 }}>+$800/mo</div>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.8)', padding: 16, borderRadius: 8 }}>
            <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 8 }}>Tighten Cache TTL</div>
            <div style={{ fontSize: 12, color: '#6B7280' }}>Reduce duplicate response storage</div>
            <div style={{ fontSize: 20, fontWeight: 600, color: '#10B981', marginTop: 8 }}>+$320/mo</div>
          </div>
        </div>
      </div>
    </div>
  );
}