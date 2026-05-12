'use client';

import { useState } from 'react';

interface Model {
  id: string;
  name: string;
  base: string;
  status: 'training' | 'ready' | 'failed';
  epoch: number;
  loss: number;
  accuracy: number;
  created: string;
  cost: string;
}

const models: Model[] = [
  { id: 'm1', name: 'research-agent-v3', base: 'gpt-4o', status: 'training', epoch: 45, loss: 0.23, accuracy: 0.89, created: '2024-02-01', cost: '$245' },
  { id: 'm2', name: 'writer-v2', base: 'claude-3', status: 'ready', epoch: 100, loss: 0.15, accuracy: 0.94, created: '2024-01-28', cost: '$180' },
  { id: 'm3', name: 'triage-v1', base: 'gpt-4-turbo', status: 'ready', epoch: 80, loss: 0.28, accuracy: 0.86, created: '2024-01-15', cost: '$120' },
  { id: 'm4', name: 'analyzer-custom', base: 'llama-3', status: 'failed', epoch: 12, loss: 0.65, accuracy: 0.54, created: '2024-01-10', cost: '$45' },
];

const datasets = [
  { id: 'd1', name: 'research-corpus-10k', samples: 10000, source: 'Manual Upload', added: '2024-01-28' },
  { id: 'd2', name: 'customer-support-logs', samples: 45000, source: 'Zendesk', added: '2024-01-20' },
  { id: 'd3', name: 'product-descriptions', samples: 8200, source: 'CRM', added: '2024-01-15' },
];

export default function FinetunePage() {
  const [selectedTab, setSelectedTab] = useState<'models' | 'datasets' | 'training'>('models');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Fine-tuning</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Custom model training & evaluation</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + Create Training Job
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['models', 'datasets', 'training'] as const).map(t => (
          <button
            key={t}
            onClick={() => setSelectedTab(t)}
            style={{
              background: selectedTab === t ? '#1A1A2E' : '#fff',
              color: selectedTab === t ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'models' ? 'Custom Models' : t === 'datasets' ? 'Datasets' : 'Training Jobs'}
          </button>
        ))}
      </div>

      {selectedTab === 'models' ? (
        <>
          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{models.length}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Custom Models</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{models.filter(m => m.status === 'ready').length}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Ready to Use</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{models.filter(m => m.status === 'training').length}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Training</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{models.reduce((a, m) => a + Number(m.cost.replace('$', '')), 0)}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Total Spent</div>
            </div>
          </div>

          {/* Model Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
            {models.map(model => (
              <div key={model.id} style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 600 }}>{model.name}</div>
                    <div style={{ fontSize: 12, color: '#6B7280', marginTop: 4 }}>Base: {model.base}</div>
                  </div>
                  <span style={{ 
                    background: model.status === 'ready' ? '#10B98120' : model.status === 'training' ? '#F59E0B20' : '#DA1E2820',
                    color: model.status === 'ready' ? '#10B981' : model.status === 'training' ? '#F59E0B' : '#DA1E28',
                    padding: '4px 10px',
                    borderRadius: 12,
                    fontSize: 11,
                    fontWeight: 500,
                  }}>
                    {model.status === 'ready' ? '● Ready' : model.status === 'training' ? 'Training' : 'Failed'}
                  </span>
                </div>
                
                {/* Progress bar for training */}
                {model.status === 'training' && (
                  <div style={{ marginBottom: 16 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: '#6B7280', marginBottom: 4 }}>
                      <span>Epoch {model.epoch}/100</span>
                      <span>{(model.epoch / 100 * 100).toFixed(0)}%</span>
                    </div>
                    <div style={{ height: 6, background: '#F4F4F4', borderRadius: 3 }}>
                      <div style={{ height: '100%', width: `${model.epoch}%`, background: '#F59E0B', borderRadius: 3 }} />
                    </div>
                  </div>
                )}

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 16 }}>
                  <div>
                    <div style={{ fontSize: 11, color: '#6B7280' }}>Loss</div>
                    <div style={{ fontSize: 16, fontWeight: 600, fontFamily: 'monospace' }}>{model.loss}</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 11, color: '#6B7280' }}>Accuracy</div>
                    <div style={{ fontSize: 16, fontWeight: 600, fontFamily: 'monospace' }}>{(model.accuracy * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div style={{ fontSize: 11, color: '#6B7280' }}>Cost</div>
                    <div style={{ fontSize: 16, fontWeight: 600, fontFamily: 'monospace' }}>{model.cost}</div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: 8 }}>
                  {model.status === 'ready' && (
                    <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 14px', borderRadius: 6, fontSize: 12, cursor: 'pointer', flex: 1 }}>
                      Use Model
                    </button>
                  )}
                  <button style={{ background: 'transparent', border: '1px solid #E5E5E5', padding: '8px 14px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
                    View
                  </button>
                  <button style={{ background: 'transparent', border: '1px solid #E5E5E5', padding: '8px 14px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      ) : selectedTab === 'datasets' ? (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DATASET</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>SAMPLES</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>SOURCE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ADDED</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              {datasets.map(d => (
                <tr key={d.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{d.name}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{d.samples.toLocaleString()}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{d.source}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{d.added}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <button style={{ background: 'transparent', border: '1px solid #E5E5E5', padding: '4px 10px', borderRadius: 4, fontSize: 11, cursor: 'pointer', marginRight: 8 }}>
                      Edit
                    </button>
                    <button style={{ background: 'transparent', border: '1px solid #E5E5E5', padding: '4px 10px', borderRadius: 4, fontSize: 11, cursor: 'pointer' }}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', padding: 40, textAlign: 'center' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>🚀</div>
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 8 }}>No active training jobs</h2>
          <p style={{ color: '#6B7280', marginBottom: 20 }}>Start training a custom model using your data</p>
          <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '12px 24px', borderRadius: 6, fontSize: 14, cursor: 'pointer' }}>
            Start Training Job
          </button>
        </div>
      )}
    </div>
  );
}