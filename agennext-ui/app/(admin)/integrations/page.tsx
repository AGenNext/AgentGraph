'use client';

import { useState } from 'react';

interface Integration {
  id: string;
  name: string;
  type: 'sso' | 'runtime' | 'ocr' | 'image' | 'video' | 'hrms' | 'pam' | 'iga' | 'siem' | 'finance' | 'contracts' | 'policy' | 'agent-trading';
  provider: string;
  status: 'connected' | 'disconnected';
  lastSync?: string;
  data: Record<string, unknown>;
}

const mockIntegrations: Integration[] = [
  { id: 'i1', name: 'Azure AD', type: 'sso', provider: 'Microsoft', status: 'connected', lastSync: '2024-02-01 10:00', data: { users: 45, groups: 12 } },
  { id: 'i2', name: 'AWS Bedrock', type: 'runtime', provider: 'AWS', status: 'connected', lastSync: '2024-02-01 10:00', data: { agents: 5, sessions: 1240, region: 'us-east-1' } },
  { id: 'i3', name: 'Azure AI Foundry', type: 'runtime', provider: 'Microsoft', status: 'connected', lastSync: '2024-02-01 10:00', data: { agents: 8, deployments: 12, region: 'eastus' } },
  { id: 'i4', name: 'Vertex AI', type: 'runtime', provider: 'Google', status: 'disconnected', data: {} },
  { id: 'i5', name: 'LlamaIndex', type: 'ocr', provider: 'LlamaIndex', status: 'connected', lastSync: '2024-02-01 10:00', data: { documents: 1240, pages: 4560, accuracy: 0.97 } },
  { id: 'i6', name: 'ComfyUI', type: 'image', provider: 'ComfyUI', status: 'connected', lastSync: '2024-02-01 10:00', data: { workflows: 24, nodes: 156, queue: 3 } },
  { id: 'i7', name: 'Stable Diffusion', type: 'image', provider: 'Stability AI', status: 'connected', lastSync: '2024-02-01 09:30', data: { models: 12, images: 2450 } },
  { id: 'i8', name: 'Sora', type: 'video', provider: 'OpenAI', status: 'disconnected', data: {} },
  { id: 'i9', name: 'OPA', type: 'policy', provider: 'Styra', status: 'connected', lastSync: '2024-02-01 10:00', data: { policies: 24, decisions: 4560, allowRate: 98.5 } },
  { id: 'i10', name: 'Workday', type: 'hrms', provider: 'Workday', status: 'disconnected', data: {} },
  { id: 'i11', name: 'CyberArk', type: 'pam', provider: 'CyberArk', status: 'disconnected', data: {} },
  { id: 'i12', name: 'SailPoint', type: 'iga', provider: 'SailPoint', status: 'disconnected', data: {} },
  { id: 'i13', name: 'Splunk', type: 'siem', provider: 'Splunk', status: 'connected', lastSync: '2024-02-01 09:30', data: { events: 15420 } },
  { id: 'i14', name: 'Stripe', type: 'finance', provider: 'Stripe', status: 'disconnected', data: {} },
  { id: 'i15', name: 'DocuSign', type: 'contracts', provider: 'DocuSign', status: 'disconnected', data: {} },
];

const configFields = {
  sso: ['Tenant URL', 'Client ID', 'Client Secret', 'Protocol'],
  runtime: ['Region', 'Access Key', 'Secret Key', 'Model IDs'],
  ocr: ['API Key', 'Model', 'Language', 'Confidence Threshold'],
  image: ['Server URL', 'API Key', 'Queue Name', 'Model Path'],
  video: ['API Key', 'Model', 'Max Duration', 'FPS'],
  hrms: ['API Endpoint', 'API Key', 'Auto-provision'],
  pam: ['Vault URL', 'Auth Method', 'Namespace'],
  iga: ['API URL', 'Service Account', 'Connector'],
  siem: ['Splunk URL', 'Token', 'Index'],
  finance: ['API Key', 'Endpoint', 'Currency'],
  policy: ['Server URL', 'Policy Path', 'Decision Mode'],
  'agent-trading': ['Marketplace URL', 'API Key', 'Fee' ],
  contracts: ['Account ID', 'API Key', 'Template'],
};

const typeIcons = { sso: '🔐', runtime: '🧠', ocr: '📖', image: '🎨', video: '🎬', hrms: '👥', pam: '🛡', iga: '📋', siem: '📊', finance: '💰', contracts: '📜', policy: '🛡', 'agent-trading': '🤝' };
const typeLabels = { sso: 'SSO / Identity', runtime: 'Runtime', ocr: 'OCR / Document', image: 'Image Gen', video: 'Video Gen', hrms: 'HRMS', pam: 'Privileged Access', iga: 'Identity Governance', siem: 'SIEM', finance: 'Finance', contracts: 'Contracts', policy: 'Policy Engine', 'agent-trading': 'Agent Marketplace' };

export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<Integration[]>(mockIntegrations);
  const [selected, setSelected] = useState<Integration | null>(null);

  const sync = (id: string) => {
    setIntegrations(integrations.map(i => i.id === id ? { ...i, lastSync: new Date().toISOString().slice(0, 16).replace('T', ' ') } : i));
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Integrations</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
        <div>
          <h2 style={{ fontSize: 14, marginBottom: 16 }}>Enterprise Integrations</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
            {integrations.map(int => (
              <div key={int.id} 
                onClick={() => setSelected(int)}
                style={{ 
                  background: selected?.id === int.id ? '#0F62FE' : '#fff', 
                  color: selected?.id === int.id ? '#fff' : '#161616',
                  borderRadius: 8, 
                  padding: 16, 
                  cursor: 'pointer',
                  border: selected?.id === int.id ? 'none' : '1px solid #E5E5E5',
                }}>
                <div style={{ fontSize: 24, marginBottom: 8, opacity: selected?.id === int.id ? 1 : 0.7 }}>{typeIcons[int.type]}</div>
                <div style={{ fontWeight: 600, fontSize: 13 }}>{int.name}</div>
                <div style={{ fontSize: 11, opacity: 0.7, textTransform: 'capitalize' }}>{typeLabels[int.type]}</div>
                <div style={{ fontSize: 10, marginTop: 8, display: 'flex', alignItems: 'center', gap: 4 }}>
                  <span style={{ width: 6, height: 6, borderRadius: '50%', background: int.status === 'connected' ? '#10B981' : '#8C8C8C' }} />
                  <span>{int.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          {selected ? (
            <div style={{ background: '#fff', borderRadius: 8, padding: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                <div>
                  <h2 style={{ fontSize: 18, fontWeight: 600 }}>{selected.name}</h2>
                  <p style={{ fontSize: 12, color: '#525252' }}>{typeLabels[selected.type]} • {selected.provider}</p>
                </div>
                <span style={{ background: selected.status === 'connected' ? '#10B98120' : '#E5E5E5', color: selected.status === 'connected' ? '#10B981' : '#525252', padding: '4px 12px', borderRadius: 999, fontSize: 12 }}>
                  {selected.status}
                </span>
              </div>

              {selected.status === 'connected' ? (
                <div>
                  <div style={{ marginBottom: 16 }}>
                    <div style={{ fontSize: 12, color: '#525252', marginBottom: 4 }}>Synced Data</div>
                    <pre style={{ background: '#F4F4F4', padding: 12, borderRadius: 4, fontSize: 11, fontFamily: 'monospace', maxHeight: 150, overflow: 'auto' }}>
                      {JSON.stringify(selected.data, null, 2)}
                    </pre>
                  </div>
                  <div style={{ fontSize: 11, color: '#8C8C8C', marginBottom: 16 }}>Last sync: {selected.lastSync}</div>
                  <button onClick={() => sync(selected.id)} style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 4, cursor: 'pointer' }}>
                    Sync Now
                  </button>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: 12, color: '#525252', marginBottom: 12 }}>Configuration (click to edit)</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {(configFields[selected.type as keyof typeof configFields] || []).map(field => (
                      <input key={field} placeholder={field} style={{ padding: 8, border: '1px solid #E5E5E5', borderRadius: 4, fontSize: 12 }} />
                    ))}
                  </div>
                  <button style={{ background: '#10B981', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 4, marginTop: 16, cursor: 'pointer', width: '100%' }}>
                    Connect
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div style={{ background: '#fff', borderRadius: 8, padding: 32, textAlign: 'center', color: '#8C8C8C' }}>
              Select an integration
            </div>
          )}
        </div>
      </div>
    </div>
  );
}