'use client';

import { useState } from 'react';

// Three Kernels: Semantic Kernel, Yaala, OrgKernel

const KERNELS = [
  {
    id: 'sk',
    name: 'Semantic Kernel',
    focus: 'Development',
    color: '#0078D4',
    features: ['Kernel', 'Planner', 'Function Calling', 'Memory', 'Multi-Agent'],
  },
  {
    id: 'yaala',
    name: 'Yaala Kernel',
    focus: 'Runtime',
    color: '#10B981',
    features: ['CrewAI', 'LangChain', 'AutoGen', 'Azure', 'Memory'],
  },
  {
    id: 'ok',
    name: 'OrgKernel',
    focus: 'Security',
    color: '#6366F1',
    features: ['Ed25519', 'Token', 'Audit', 'Mission', 'Policy'],
  },
];

const FRAMEWORKS = [
  { name: 'OpenAI', supported: true },
  { name: 'Anthropic', supported: true },
  { name: 'LangChain', supported: true },
  { name: 'CrewAI', supported: true },
  { name: 'AutoGen', supported: true },
  { name: 'Azure AI', supported: true },
  { name: 'Google Gemini', supported: true },
  { name: 'LlamaIndex', supported: true },
];

export default function KernelPage() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div style={{ padding: 32, fontFamily: "'SF Pro Display', -apple-system", background: '#050507', minHeight: '100vh', color: '#F4F4F5' }}>
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h1 style={{ fontSize: 32, fontWeight: 700, margin: 0 }}>AGenNext Kernel</h1>
          <span style={{ background: '#10B98120', color: '#10B981', padding: '4px 10px', borderRadius: 6, fontSize: 11 }}>3 KERNELS</span>
        </div>
        <p style={{ color: '#A1A1AA', margin: '8px 0 0' }}>Integration: SK + Yaala + OrgKernel</p>
      </div>

      {/* Kernels */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 40 }}>
        {KERNELS.map(k => (
          <div key={k.id} style={{ background: '#0E0E12', borderRadius: 16, padding: 20, border: `1px solid ${k.color}30` }}>
            <div style={{ fontSize: 16, fontWeight: 600, color: k.color, marginBottom: 8 }}>{k.name}</div>
            <div style={{ fontSize: 11, color: '#71717A', marginBottom: 12 }}>{k.focus}</div>
            <div style={{ fontSize: 11, color: '#A1A1AA' }}>{k.features.join(', ')}</div>
          </div>
        ))}
      </div>

      {/* Supported Frameworks */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Runtime Supported Frameworks</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
          {FRAMEWORKS.map(f => (
            <div key={f.name} style={{ background: '#0E0E12', borderRadius: 8, padding: 12, border: '1px solid #232329' }}>
              <span style={{ color: f.supported ? '#10B981' : '#EF4444', marginRight: 8 }}>{f.supported ? '✓' : '✗'}</span>
              <span style={{ fontSize: 13 }}>{f.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Architecture</h2>
        <div style={{ background: '#0E0E12', borderRadius: 12, padding: 24, border: '1px solid #232329', textAlign: 'center' }}>
          <span style={{ color: '#0078D4' }}>User → Kernel (SK) → Runtime (Yaala) → Security (OrgKernel) → Deploy</span>
        </div>
      </div>
    </div>
  );
}