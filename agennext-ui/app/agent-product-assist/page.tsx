'use client';

import { useState } from 'react';

interface ProductAgent {
  id: string;
  name: string;
  product: string;
  role: 'sales' | 'support' | 'onboarding' | 'billing';
  status: 'deployed' | 'training' | 'paused';
  chats: number;
  satisfaction: number;
}

const agents: ProductAgent[] = [
  { id: '1', name: 'Sales Assistant', product: 'Cloud Pro', role: 'sales', status: 'deployed', chats: 1250, satisfaction: 94 },
  { id: '2', name: 'Tech Support', product: 'Enterprise', role: 'support', status: 'deployed', chats: 3420, satisfaction: 89 },
  { id: '3', name: 'Onboarding Guide', product: 'Startup', role: 'onboarding', status: 'training', chats: 0, satisfaction: 0 },
  { id: '4', name: 'Billing Helper', product: 'All Products', role: 'billing', status: 'deployed', chats: 890, satisfaction: 92 },
  { id: '5', name: 'Sales Assistant', product: 'Enterprise', role: 'sales', status: 'deployed', chats: 780, satisfaction: 91 },
  { id: '6', name: 'Support Bot', product: 'Cloud Pro', role: 'support', status: 'paused', chats: 450, satisfaction: 85 },
];

export default function AgentProductAssistPage() {
  const [filter, setFilter] = useState<string>('all');

  const filtered = filter === 'all' ? agents : agents.filter(a => a.product.toLowerCase().includes(filter.toLowerCase()) || a.role === filter);
  const deployed = agents.filter(a => a.status === 'deployed').length;
  const totalChats = agents.reduce((a, a2) => a + a2.chats, 0);

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <h1 style={{ fontSize: 24, marginBottom: 20 }}>Agent Product Assist</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#10B981' }}>{deployed}</div>
          <div style={{ color: '#8C8C8C' }}>Deployed</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#58A6FF' }}>{totalChats.toLocaleString()}</div>
          <div style={{ color: '#8C8C8C' }}>Total Chats</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#D29922' }}>{Math.round(agents.reduce((a, a2) => a + a2.satisfaction, 0)/agents.filter(a=>a.satisfaction>0).length)}%</div>
          <div style={{ color: '#8C8C8C' }}>Avg Satisfaction</div>
        </div>
        <div style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
          <div style={{ fontSize: 32, color: '#8C8C8C' }}>{agents.length}</div>
          <div style={{ color: '#8C8C8C' }}>Agents</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {['all', 'sales', 'support', 'onboarding', 'billing', 'Cloud Pro', 'Enterprise'].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            padding: '8px 16px', background: filter === f ? '#238636' : '#21262D',
            border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer'
          }}>
            {f}
          </button>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
        {filtered.map(a => (
          <div key={a.id} style={{ padding: 16, background: '#21262D', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <strong>{a.name}</strong>
              <span style={{ color: a.status === 'deployed' ? '#10B981' : a.status === 'training' ? '#58A6FF' : '#8C8C8C' }}>
                {a.status}
              </span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 12 }}>{a.product}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: 12 }}>
              <span style={{ color: '#8C8C8C' }}>💬 {a.chats.toLocaleString()}</span>
              <span style={{ color: a.satisfaction >= 90 ? '#10B981' : a.satisfaction > 0 ? '#D29922' : '#8C8C8C' }}>
                {a.satisfaction > 0 ? `★ ${a.satisfaction}%` : '-'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}