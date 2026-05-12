'use client';

import { useState } from 'react';

// AGenNext Kernel - Unifying AURA + Semantic Kernel + Yaala
// Ref: https://metaprise.ai/aura/runtime.html + github.com/microsoft/semantic-kernel

const LAYERS = [
  {
    name: 'Development',
    from: 'Semantic Kernel',
    color: '#0078D4',
    features: ['Kernel Core', 'Planner', 'Function Calling', 'Prompt Pipeline'],
  },
  {
    name: 'Runtime',
    from: 'Yaala Kernel',
    color: '#10B981',
    features: ['Framework Adapters', 'Memory Backend', 'Deployment Profiles'],
  },
  {
    name: 'Trust',
    from: 'AURA/OrgKernel',
    color: '#FF6B35',
    features: ['Agent Identity', 'Execution Token', 'Hash Audit', 'Mission Lifecycle'],
  },
];

const FEATURES = [
  { cat: 'Identity', items: ['Ed25519 Keys', 'CSR', 'Challenge-Response', 'Revocation'] },
  { cat: 'Runtime', items: ['Crash Recovery', 'Checkpoint', 'Retry Policy', 'Saga Compensation'] },
  { cat: 'Security', items: ['Token Scoping', 'Tool Gateway', 'Policy Engine', 'Authority Graph'] },
  { cat: 'Audit', items: ['L1 Business', 'L2 Execution', 'L3 Compliance', 'SHA-256 Chain'] },
];

export default function KernelPage() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div style={{ padding: 32, fontFamily: "'SF Pro Display', -apple-system", background: '#050507', minHeight: '100vh', color: '#F4F4F5' }}>
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h1 style={{ fontSize: 32, fontWeight: 700, margin: 0 }}>AGenNext Kernel</h1>
          <span style={{ background: '#F59E0B20', color: '#F59E0B', padding: '4px 10px', borderRadius: 6, fontSize: 11 }}>AURA + SK + Yaala</span>
        </div>
        <p style={{ color: '#A1A1AA', margin: '8px 0' }}>Unified Kernel combining Metaprise AURA + Microsoft Semantic Kernel + Yaala</p>
      </div>

      {/* Three Layers */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 40 }}>
        {LAYERS.map(l => (
          <div key={l.name} style={{ background: '#0E0E12', borderRadius: 16, padding: 20, border: `1px solid ${l.color}30` }}>
            <div style={{ fontSize: 16, fontWeight: 600, color: l.color, marginBottom: 4 }}>{l.name}</div>
            <div style={{ fontSize: 11, color: '#71717A', marginBottom: 12 }}>From: {l.from}</div>
            <div style={{ fontSize: 11, color: '#A1A1AA' }}>{l.features.join(', ')}</div>
          </div>
        ))}
      </div>

      {/* Feature Categories */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>All Integrated Features</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
          {FEATURES.map(f => (
            <div key={f.cat} style={{ background: '#0E0E12', borderRadius: 12, padding: 16, border: '1px solid #232329' }}>
              <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8 }}>{f.cat}</div>
              {f.items.map(item => (
                <div key={item} style={{ fontSize: 11, color: '#A1A1AA', marginBottom: 4 }}>✓ {item}</div>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* Architecture Flow */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Architecture Flow</h2>
        <div style={{ background: '#0E0E12', borderRadius: 12, padding: 24, border: '1px solid #232329', textAlign: 'center' }}>
          <span style={{ color: '#0078D4' }}>Dev (SK)</span>
          <span style={{ color: '#71717A', margin: '0 12px' }}>→</span>
          <span style={{ color: '#10B981' }}>Runtime (Yaala)</span>
          <span style={{ color: '#71717A', margin: '0 12px' }}>→</span>
          <span style={{ color: '#FF6B35' }}>Trust (AURA)</span>
          <span style={{ color: '#71717A', margin: '0 12px' }}>→</span>
          <span style={{ color: '#10B981' }}>Deploy</span>
        </div>
      </div>
    </div>
  );
}