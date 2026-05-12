'use client';

import { useState } from 'react';

interface CostItem {
  id: string;
  category: 'compute' | 'api' | 'storage' | 'seats';
  description: string;
  amount: number;
  period: string;
}

const mockCosts: CostItem[] = [
  { id: 'c1', category: 'compute', description: 'GPU hours', amount: 420, period: 'Feb 2024' },
  { id: 'c2', category: 'api', description: 'OpenAI API', amount: 280, period: 'Feb 2024' },
  { id: 'c3', category: 'api', description: 'Anthropic API', amount: 150, period: 'Feb 2024' },
  { id: 'c4', category: 'storage', description: 'Vector DB', amount: 85, period: 'Feb 2024' },
  { id: 'c5', category: 'seats', description: 'User seats (15)', amount: 450, period: 'Feb 2024' },
];

export default function FinancePage() {
  const [costs] = useState<CostItem[]>(mockCosts);

  const total = costs.reduce((a, c) => a + c.amount, 0);
  const byCategory = {
    compute: costs.filter(c => c.category === 'compute').reduce((a, c) => a + c.amount, 0),
    api: costs.filter(c => c.category === 'api').reduce((a, c) => a + c.amount, 0),
    storage: costs.filter(c => c.category === 'storage').reduce((a, c) => a + c.amount, 0),
    seats: costs.filter(c => c.category === 'seats').reduce((a, c) => a + c.amount, 0),
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Finance</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>${total}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Cost</div>
        </div>
        {Object.entries(byCategory).map(([cat, amt]) => (
          <div key={cat} style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
            <div style={{ fontSize: 28, fontWeight: 600 }}>${amt}</div>
            <div style={{ fontSize: 12, color: '#525252', textTransform: 'capitalize' }}>{cat}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
        <div style={{ background: '#fff', borderRadius: 4 }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr style={{ background: '#F4F4F4' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>CATEGORY</th>
              <th style={{ padding: 12, textAlign: 'left' }}>DESCRIPTION</th>
              <th style={{ padding: 12, textAlign: 'right' }}>AMOUNT</th>
            </tr></thead>
            <tbody>
              {costs.map(c => (
                <tr key={c.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                  <td style={{ padding: 12, textTransform: 'capitalize' }}>{c.category}</td>
                  <td style={{ padding: 12 }}>{c.description}</td>
                  <td style={{ padding: 12, textAlign: 'right', fontWeight: 500 }}>${c.amount}</td>
                </tr>
              ))}
              <tr style={{ background: '#F4F4F4' }}>
                <td style={{ padding: 12, fontWeight: 600 }}>Total</td>
                <td style={{ padding: 12 }}></td>
                <td style={{ padding: 12, textAlign: 'right', fontWeight: 700 }}>${total}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <h3 style={{ fontSize: 14, marginBottom: 16 }}>Budget</h3>
          {Object.entries(byCategory).map(([cat, amt]) => (
            <div key={cat} style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 4 }}>
                <span style={{ textTransform: 'capitalize' }}>{cat}</span>
                <span>${amt}</span>
              </div>
              <div style={{ background: '#E5E5E5', height: 8, borderRadius: 4, overflow: 'hidden' }}>
                <div style={{ width: `${(amt / total) * 100}%`, height: '100%', background: '#0F62FE' }} />
              </div>
            </div>
          ))}
          <button style={{ width: '100%', background: '#0F62FE', color: '#fff', border: 'none', padding: '10px', borderRadius: 4, marginTop: 16, cursor: 'pointer' }}>
            Export Invoice
          </button>
        </div>
      </div>
    </div>
  );
}