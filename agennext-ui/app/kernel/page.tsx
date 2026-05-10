'use client';

import { useState } from 'react';

// Metaprise AURA Runtime Integration
// Ref: https://metaprise.ai/aura/runtime.html

const KERNELS = [
  {
    id: 'aura',
    name: 'AURA Runtime',
    focus: 'Durable Execution',
    color: '#FF6B35',
    desc: 'Durable execution engine guaranteeing task completion',
    features: ['Execution', 'Durability', 'Recovery', 'Checkpoints'],
  },
  {
    id: 'orgkernel',
    name: 'OrgKernel',
    focus: 'Trust Layer',
    color: '#6366F1',
    desc: 'Ed25519 identity, execution tokens, SHA-256 audit',
    features: ['Identity', 'Token', 'Audit', 'Mission', 'Policy'],
  },
  {
    id: 'sk',
    name: 'Semantic Kernel',
    focus: 'Development',
    color: '#0078D4',
    desc: 'Microsoft SDK for AI agent orchestration',
    features: ['Kernel', 'Planner', 'Memory', 'Multi-Agent'],
  },
];

const RUNTIME_LAYERS = [
  { layer: 'Execution', desc: 'Agent task execution with retry logic' },
  { layer: 'Durability', desc: 'Crash recovery, saga compensation' },
  { layer: 'Monitoring', desc: 'Full-chain tracing and observability' },
];

export default function KernelPage() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div style={{ padding: 32, fontFamily: "'SF Pro Display', -apple-system", background: '#050507', minHeight: '100vh', color: '#F4F4F5' }}>
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h1 style={{ fontSize: 32, fontWeight: 700, margin: 0 }}>Metaprise AURA</h1>
          <span style={{ background: '#FF6B3520', color: '#FF6B35', padding: '4px 10px', borderRadius: 6, fontSize: 11 }}>Runtime + Kernel</span>
        </div>
        <p style={{ color: '#A1A1AA', margin: '8px 0' }}>Durable Execution Engine + Trust Layer</p>
        <p style={{ color: '#FF6B35', fontSize: 12 }}>Ref: <a href="https://metaprise.ai/aura/runtime.html" target="_blank" style={{ color: '#FF6B35' }}>metaprise.ai/aura/runtime.html</a></p>
      </div>

      {/* AURA Runtime Layers */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>AURA Runtime Layers</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {RUNTIME_LAYERS.map(l => (
            <div key={l.layer} style={{ background: '#0E0E12', borderRadius: 12, padding: 20, border: '1px solid #FF6B3530' }}>
              <div style={{ fontSize: 16, fontWeight: 600, color: '#FF6B35', marginBottom: 8 }}>{l.layer}</div>
              <div style={{ fontSize: 12, color: '#A1A1AA' }}>{l.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Kernels */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Integrated Kernels</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {KERNELS.map(k => (
            <div key={k.id} style={{ background: '#0E0E12', borderRadius: 16, padding: 20, border: `1px solid ${k.color}30` }}>
              <div style={{ fontSize: 16, fontWeight: 600, color: k.color, marginBottom: 4 }}>{k.name}</div>
              <div style={{ fontSize: 11, color: '#71717A', marginBottom: 8 }}>{k.focus}</div>
              <p style={{ fontSize: 12, color: '#A1A1AA', marginBottom: 12 }}>{k.desc}</p>
              <div style={{ fontSize: 10, color: '#71717A' }}>{k.features.join(', ')}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div>
        <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16 }}>Production Features</h2>
        <div style={{ background: '#0E0E12', borderRadius: 12, padding: 20, border: '1px solid #232329' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
            {[
              'Crash Recovery', 'Saga Compensation', 'Checkpoint Persistence', 'Retry Policy',
              'Namespace Isolation', 'Multi-Region', 'Workflow Versioning', 'Canary Deploys',
              'SSO/SAML', 'SCIM User Sync', 'Full-Chain Tracing', 'LLM-as-Judge',
            ].map(f => (
              <div key={f} style={{ fontSize: 12 }}>✓ {f}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}