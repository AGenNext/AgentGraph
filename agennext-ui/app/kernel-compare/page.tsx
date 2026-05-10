'use client';

import { useState } from 'react';

// Kernel Comparison: AURA vs SK vs Others

const KERNELS = [
  {
    name: 'Metaprise AURA',
    focus: 'Durable Execution + Trust',
    strength: ['Crash Recovery', 'Hash Audit', 'Ed25519 Identity'],
    best: ['Enterprise', 'Financial', 'Compliance'],
  },
  {
    name: 'Microsoft SK',
    focus: 'Development + Orchestration',
    strength: ['Mature DX', 'Azure', 'Multi-Agent'],
    best: ['Dev', 'Azure Shops', 'Rapid Prototyping'],
  },
  {
    name: 'Yaala Kernel',
    focus: 'Runtime + Execution',
    strength: ['Framework Agnostic', 'Multi-Cloud', 'Memory'],
    best: ['Cross-Framework', 'Multi-Cloud'],
  },
  {
    name: 'LangGraph',
    focus: 'Graph-Based Agents',
    strength: ['DAG Execution', 'State Management', 'Cycles'],
    best: ['Complex Workflows', 'Production'],
  },
];

export default function KernelComparePage() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div style={{ padding: 32, fontFamily: "'SF Pro Display', -apple-system", background: '#050507', minHeight: '100vh', color: '#F4F4F5' }}>
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ fontSize: 32, fontWeight: 700, margin: 0 }}>Kernel Comparison</h1>
        <p style={{ color: '#A1A1AA', margin: '8px 0' }}>AURA vs Semantic Kernel vs Others</p>
      </div>

      {/* Recommendation */}
      <div style={{ background: 'linear-gradient(135deg, #FF6B3510 0%, #0078D410 100%)', borderRadius: 16, padding: 24, marginBottom: 40, border: '1px solid #232329' }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>🎯 Recommendation</h2>
        <p style={{ fontSize: 14, color: '#A1A1AA', lineHeight: 1.7 }}>
          <strong style={{ color: '#fff' }}>For Enterprise:</strong> Use Metaprise AURA - full trust layer with crash recovery, cryptographic identity, and audit.<br/>
          <strong style={{ color: '#fff' }}>For Dev:</strong> Use Semantic Kernel - mature SDK with great developer experience.<br/>
          <strong style={{ color: '#fff' }}>Best of Both:</strong> AURA for runtime + SK for development.
        </p>
      </div>

      {/* Comparison Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16, marginBottom: 40 }}>
        {KERNELS.map(k => (
          <div key={k.name} onClick={() => setSelected(k.name === selected ? null : k.name)}
            style={{ background: '#0E0E12', borderRadius: 16, padding: 20, border: `1px solid ${selected === k.name ? '#10B981' : '#232329'}`, cursor: 'pointer' }}>
            <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>{k.name}</div>
            <div style={{ fontSize: 11, color: '#71717A', marginBottom: 12 }}>{k.focus}</div>
            <div style={{ fontSize: 11, color: '#10B981', marginBottom: 4 }}>Strengths:</div>
            <div style={{ fontSize: 12, color: '#A1A1AA', marginBottom: 12 }}>{k.strength.join(', ')}</div>
            <div style={{ fontSize: 11, color: '#6366F1', marginBottom: 4 }}>Best for:</div>
            <div style={{ fontSize: 12, color: '#A1A1AA' }}>{k.best.join(', ')}</div>
          </div>
        ))}
      </div>

      {/* Feature Matrix */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Feature Matrix</h2>
        <div style={{ background: '#0E0E12', borderRadius: 12, border: '1px solid #232329', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#16161D' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#71717A' }}>Feature</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#FF6B35' }}>AURA</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#0078D4' }}>SK</th>
                <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#10B981' }}>Yaala</th>
              </tr>
            </thead>
            <tbody>
              {[
                { f: 'Crash Recovery', a: '✓', s: '○', y: '○' },
                { f: 'Ed25519 Identity', a: '✓', s: '○', y: '○' },
                { f: 'SHA-256 Audit', a: '✓', s: '○', y: '○' },
                { f: 'Memory/Vector', a: '○', s: '✓', y: '✓' },
                { f: 'Multi-Agent', a: '○', s: '✓', y: '✓' },
                { f: 'Checkpoint', a: '✓', s: '○', y: '○' },
                { f: 'Azure Support', a: '✓', s: '✓', y: '✓' },
                { f: 'Production Ready', a: '✓', s: '✓', y: '○' },
              ].map(row => (
                <tr key={row.f} style={{ borderTop: '1px solid #232329' }}>
                  <td style={{ padding: '12px 16px', fontSize: 12 }}>{row.f}</td>
                  <td style={{ padding: '12px 16px', textAlign: 'center', fontSize: 12, color: row.a === '✓' ? '#10B981' : '#71717A' }}>{row.a}</td>
                  <td style={{ padding: '12px 16px', textAlign: 'center', fontSize: 12, color: row.s === '✓' ? '#10B981' : '#71717A' }}>{row.s}</td>
                  <td style={{ padding: '12px 16px', textAlign: 'center', fontSize: 12, color: row.y === '✓' ? '#10B981' : '#71717A' }}>{row.y}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}