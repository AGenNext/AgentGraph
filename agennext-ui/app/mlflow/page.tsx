'use client';

import { useState } from 'react';

interface Experiment {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'failed';
  metrics: { loss: number; accuracy: number; f1: number };
  runs: number;
  runtime: string;
  updated: string;
}

const experiments: Experiment[] = [
  { id: 'e1', name: 'Research Agent v2', status: 'running', metrics: { loss: 0.23, accuracy: 0.91, f1: 0.89 }, runs: 145, runtime: 'AWS Bedrock', updated: '2 min ago' },
  { id: 'e2', name: 'Writer Agent v1', status: 'completed', metrics: { loss: 0.18, accuracy: 0.94, f1: 0.92 }, runs: 89, runtime: 'Azure AI Foundry', updated: '1 hour ago' },
  { id: 'e3', name: 'Analyzer baseline', status: 'completed', metrics: { loss: 0.32, accuracy: 0.85, f1: 0.83 }, runs: 56, runtime: 'Vertex AI', updated: '3 hours ago' },
  { id: 'e4', name: 'Triage Agent v3', status: 'failed', metrics: { loss: 0.45, accuracy: 0.72, f1: 0.68 }, runs: 12, runtime: 'AWS Bedrock', updated: '5 hours ago' },
];

export default function MLFlowPage() {
  const [exps] = useState<Experiment[]>(experiments);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>MLflow Experiments</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Experiment tracking & model versioning</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + New Experiment
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{exps.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Experiments</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{exps.filter(e => e.status === 'completed').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Completed</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{exps.filter(e => e.status === 'failed').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Failed</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{exps.reduce((a, e) => a + e.runs, 0)}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Runs</div>
        </div>
      </div>

      {/* Experiment List */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F8F9FA' }}>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>EXPERIMENT</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>METRICS</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RUNTIME</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RUNS</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>UPDATED</th>
            </tr>
          </thead>
          <tbody>
            {exps.map(exp => (
              <tr key={exp.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                <td style={{ padding: '14px 16px', fontWeight: 500 }}>{exp.name}</td>
                <td style={{ padding: '14px 16px' }}>
                  <span style={{ color: exp.status === 'completed' ? '#10B981' : exp.status === 'running' ? '#0F62FE' : '#DA1E28', fontSize: 12, fontWeight: 500 }}>
                    {exp.status}
                  </span>
                </td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>
                  <span style={{ marginRight: 12 }}>loss: {exp.metrics.loss}</span>
                  <span style={{ marginRight: 12 }}>acc: {exp.metrics.accuracy}</span>
                  <span>f1: {exp.metrics.f1}</span>
                </td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>{exp.runtime}</td>
                <td style={{ padding: '14px 16px', fontSize: 12 }}>{exp.runs}</td>
                <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{exp.updated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}