'use client';

import { useState } from 'react';

interface Secret {
  id: string;
  key: string;
  value: string;
  environment: 'development' | 'staging' | 'production';
  project: string;
  lastRotated: string;
}

interface Project {
  id: string;
  name: string;
  environments: number;
  secrets: number;
}

const secrets: Secret[] = [
  { id: 's1', key: 'AWS_ACCESS_KEY_ID', value: '•••••••••••••••', environment: 'production', project: 'agent-platform', lastRotated: '2024-02-01' },
  { id: 's2', key: 'AWS_SECRET_ACCESS_KEY', value: '•••••••••••••••', environment: 'production', project: 'agent-platform', lastRotated: '2024-02-01' },
  { id: 's3', key: 'AZURE_OPENAI_KEY', value: '•••••••••••••••', environment: 'production', project: 'agent-platform', lastRotated: '2024-01-28' },
  { id: 's4', key: 'SURREALDB_URL', value: 'surrealdb://••••••••', environment: 'production', project: 'agent-platform', lastRotated: '2024-01-25' },
  { id: 's5', key: 'STRIPE_API_KEY', value: '•••••••••••••••', environment: 'production', project: 'payments', lastRotated: '2024-01-20' },
  { id: 's6', key: 'JWT_SECRET', value: '•••••••••••••••', environment: 'production', project: 'auth', lastRotated: '2024-01-15' },
];

const projects: Project[] = [
  { id: 'p1', name: 'agent-platform', environments: 3, secrets: 24 },
  { id: 'p2', name: 'payments', environments: 3, secrets: 12 },
  { id: 'p3', name: 'auth', environments: 2, secrets: 8 },
  { id: 'p4', name: 'analytics', environments: 2, secrets: 6 },
];

const keys = 256;
const rotations = 12;
const compliance = 'SOC2';

export default function InfisicalPage() {
  const [activeTab, setActiveTab] = useState<'secrets' | 'projects'>('secrets');
  const [envFilter, setEnvFilter] = useState<'all' | 'production' | 'staging' | 'development'>('all');
  
  const filteredSecrets = envFilter === 'all' 
    ? secrets 
    : secrets.filter(s => s.environment === envFilter);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Infisical Secrets</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Enterprise secrets management</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button style={{ background: '#238636', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 8, fontSize: 13, cursor: 'pointer' }}>
            + Add Secret
          </button>
          <button style={{ background: '#1F2937', color: '#fff', border: '1px solid #374151', padding: '10px 16px', borderRadius: 8, fontSize: 13, cursor: 'pointer' }}>
            CLI
          </button>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{keys}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Secrets</div>
        </div>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{projects.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Projects</div>
        </div>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#0F62FE' }}>{rotations}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Rotations (30d)</div>
        </div>
        <div style={{ background: '#1F2937', padding: 20, borderRadius: 12 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{compliance}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Compliance</div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['secrets', 'projects'] as const).map(t => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            style={{
              background: activeTab === t ? '#1F2937' : 'transparent',
              color: activeTab === t ? '#fff' : '#6B7280',
              border: 'none',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'secrets' ? 'Secrets' : 'Projects'}
          </button>
        ))}
      </div>

      {activeTab === 'secrets' ? (
        <>
          {/* Filters */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            {(['all', 'production', 'staging', 'development'] as const).map(e => (
              <button
                key={e}
                onClick={() => setEnvFilter(e)}
                style={{
                  background: envFilter === e ? '#374151' : 'transparent',
                  color: '#6B7280',
                  border: '1px solid #374151',
                  padding: '6px 12px',
                  borderRadius: 6,
                  fontSize: 11,
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                }}
              >
                {e === 'all' ? 'All' : e}
              </button>
            ))}
          </div>

          {/* Secrets Table */}
          <div style={{ background: '#1F2937', borderRadius: 12, overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#111827' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>SECRET</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>VALUE</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ENVIRONMENT</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>PROJECT</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>LAST ROTATED</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                {filteredSecrets.map(s => (
                  <tr key={s.id} style={{ borderTop: '1px solid #374151' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500, fontFamily: 'monospace' }}>{s.key}</td>
                    <td style={{ padding: '14px 16px', fontFamily: 'monospace', color: '#6B7280' }}>{s.value}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ 
                        background: s.environment === 'production' ? '#DA1E2820' : s.environment === 'staging' ? '#F59E0B20' : '#10B98120',
                        color: s.environment === 'production' ? '#DA1E28' : s.environment === 'staging' ? '#F59E0B' : '#10B981',
                        padding: '4px 8px',
                        borderRadius: 4,
                        fontSize: 11,
                        textTransform: 'capitalize',
                      }}>
                        {s.environment}
                      </span>
                    </td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{s.project}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{s.lastRotated}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <button style={{ background: 'transparent', border: 'none', color: '#0F62FE', fontSize: 12, cursor: 'pointer', marginRight: 12 }}>Copy</button>
                      <button style={{ background: 'transparent', border: 'none', color: '#F59E0B', fontSize: 12, cursor: 'pointer' }}>Rotate</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {projects.map(p => (
            <div key={p.id} style={{ background: '#1F2937', borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>{p.name}</div>
              <div style={{ display: 'flex', gap: 24 }}>
                <div>
                  <div style={{ fontSize: 24, fontWeight: 600, color: '#667EEA' }}>{p.environments}</div>
                  <div style={{ fontSize: 11, color: '#6B7280' }}>Environments</div>
                </div>
                <div>
                  <div style={{ fontSize: 24, fontWeight: 600, color: '#10B981' }}>{p.secrets}</div>
                  <div style={{ fontSize: 11, color: '#6B7280' }}>Secrets</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* SDK Info */}
      <div style={{ marginTop: 24, background: '#1F2937', borderRadius: 12, padding: 20 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>SDK Integration</h3>
        <div style={{ background: '#111827', padding: 16, borderRadius: 8, fontFamily: 'monospace', fontSize: 12 }}>
          <div style={{ color: '#10B981', marginBottom: 8 }}># Install</div>
          <div>npm install @infisical/nextjs</div>
          <div style={{ color: '#10B981', marginBottom: 8, marginTop: 16 }}># Usage</div>
          <div>import &#123; getSecret &#125; from '@infisical/nextjs';</div>
          <div style={{ marginTop: 8 }}>const apiKey = await getSecret('AWS_API_KEY');</div>
          <div style={{ color: '#10B981', marginBottom: 8, marginTop: 16 }}># Environment Variables</div>
          <div>INFISICAL_TOKEN=...</div>
          <div>INFISICAL_PROJECT_ID=...</div>
        </div>
      </div>
    </div>
  );
}
