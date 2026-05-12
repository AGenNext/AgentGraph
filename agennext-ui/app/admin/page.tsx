'use client';

import { useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'developer' | 'user';
  status: 'active' | 'inactive';
  lastActive: string;
}

// Enterprise Integration
interface Integration {
  id: string;
  name: string;
  type: 'sso' | 'hrms' | 'pam' | 'iga' | 'siem' | 'finance' | 'contracts';
  provider: string;
  status: 'connected' | 'disconnected' | 'error';
  lastSync?: string;
  config: Record<string, string>;
}

const mockUsers: User[] = [
  { id: '1', name: 'Admin User', email: 'admin@agennext.io', role: 'admin', status: 'active', lastActive: '2024-02-01' },
  { id: '2', name: 'Dev User', email: 'dev@agennext.io', role: 'developer', status: 'active', lastActive: '2024-02-01' },
  { id: '3', name: 'Test User', email: 'test@agennext.io', role: 'user', status: 'inactive', lastActive: '2024-01-15' },
];

const mockIntegrations: Integration[] = [
  { id: 'i1', name: 'Azure AD', type: 'sso', provider: 'Microsoft', status: 'connected', lastSync: '2024-02-01 10:00', config: { tenant: 'company.onmicrosoft.com', protocol: 'SAML' } },
  { id: 'i2', name: 'Workday', type: 'hrms', provider: 'Workday', status: 'disconnected', config: {} },
  { id: 'i3', name: 'CyberArk', type: 'pam', provider: 'CyberArk', status: 'disconnected', config: {} },
  { id: 'i4', name: 'SailPoint', type: 'iga', provider: 'SailPoint', status: 'disconnected', config: {} },
  { id: 'i5', name: 'Splunk', type: 'siem', provider: 'Splunk', status: 'connected', lastSync: '2024-02-01 09:30', config: { endpoint: 'splunk.company.com' } },
  { id: 'i6', name: 'Stripe', type: 'finance', provider: 'Stripe', status: 'disconnected', config: {} },
  { id: 'i7', name: 'DocuSign', type: 'contracts', provider: 'DocuSign', status: 'disconnected', config: {} },
];

const typeLabels = { sso: 'SSO / Identity', hrms: 'HRMS', pam: 'Privileged Access', iga: 'Identity Governance', siem: 'SIEM / Logging', finance: 'Finance', contracts: 'Contracts' };
const typeIcons = { sso: '🔐', hrms: '👥', pam: '🛡', iga: '📋', siem: '📊', finance: '💰', contracts: '📜' };

// Enterprise-owned integration options
const integrationOptions = {
  sso: ['Azure AD', 'Okta', 'Auth0', 'Google Workspace', 'Ping Identity'],
  hrms: ['Workday', 'BamboHR', 'Greenhouse', 'Lever', 'Rippling'],
  pam: ['CyberArk', 'HashiCorp Vault', 'AWS Secrets', 'Azure Key Vault', 'Doppler'],
  iga: ['SailPoint', 'Saviynt', 'One Identity', 'Microsoft Entra', 'Okta IGA'],
  siem: ['Splunk', 'Datadog', 'Elastic', 'Sumo Logic', 'Microsoft Sentinel'],
  finance: ['Stripe', 'QuickBooks', 'NetSuite', 'SAP', 'Xero'],
  contracts: ['DocuSign', 'PandaDoc', 'Ironclad', 'Cookie', 'Contractbook'],
};

export default function AdminPage() {
  const [users] = useState<User[]>(mockUsers);
  const [integrations, setIntegrations] = useState<Integration[]>(mockIntegrations);
  const [tab, setTab] = useState<'users' | 'integrations'>('users');
  const [showConfig, setShowConfig] = useState<Integration | null>(null);

  const connect = (id: string) => {
    setIntegrations(integrations.map(i => i.id === id ? { ...i, status: 'connected' as const, lastSync: new Date().toISOString().slice(0, 16).replace('T', ' ') } : i));
  };

  const disconnect = (id: string) => {
    setIntegrations(integrations.map(i => i.id === id ? { ...i, status: 'disconnected' as const, lastSync: undefined } : i));
  };

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 24, fontWeight: 600, marginBottom: 24 }}>Admin</h1>

      <div style={{ marginBottom: 24, background: '#fff', borderRadius: 4, padding: 4, display: 'inline-flex' }}>
        {(['users', 'integrations'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            style={{ background: tab === t ? '#0F62FE' : 'transparent', color: tab === t ? '#fff' : '#161616', border: 'none', padding: '8px 16px', borderRadius: 2, cursor: 'pointer', textTransform: 'capitalize' }}>
            {t}
          </button>
        ))}
      </div>

      {tab === 'users' ? (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{users.length}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Total Users</div>
            </div>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{users.filter(u => u.status === 'active').length}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Active</div>
            </div>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{users.filter(u => u.role === 'admin').length}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Admins</div>
            </div>
          </div>
          <div style={{ background: '#fff', borderRadius: 4 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead><tr style={{ background: '#F4F4F4' }}>
                <th style={{ padding: 12, textAlign: 'left' }}>USER</th>
                <th style={{ padding: 12, textAlign: 'left' }}>ROLE</th>
                <th style={{ padding: 12, textAlign: 'left' }}>STATUS</th>
              </tr></thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                    <td style={{ padding: 12 }}><div style={{ fontWeight: 500 }}>{u.name}</div><div style={{ fontSize: 11, color: '#8C8C8C' }}>{u.email}</div></td>
                    <td style={{ padding: 12 }}><span style={{ background: u.role === 'admin' ? '#DA1E2820' : '#E5E5E5', color: u.role === 'admin' ? '#DA1E28' : '#525252', padding: '4px 8px', borderRadius: 4, fontSize: 12 }}>{u.role}</span></td>
                    <td style={{ padding: 12, color: u.status === 'active' ? '#10B981' : '#8C8C8C' }}>{u.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{integrations.length}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Integrations</div>
            </div>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{integrations.filter(i => i.status === 'connected').length}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Connected</div>
            </div>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{integrations.filter(i => i.status === 'error').length}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Errors</div>
            </div>
            <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{integrations.reduce((a, i) => a + (i.config && Object.keys(i.config).length > 0 ? 1 : 0), 0)}</div>
              <div style={{ fontSize: 12, color: '#525252' }}>Configured</div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16 }}>
            {integrations.map(int => (
              <div key={int.id} style={{ background: '#fff', borderRadius: 4, padding: 16, border: '1px solid #E5E5E5' }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>{typeIcons[int.type]}</div>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>{int.name}</div>
                <div style={{ fontSize: 12, color: '#525252', marginBottom: 8 }}>{typeLabels[int.type]}</div>
                <div style={{ fontSize: 11, color: '#8C8C8C', marginBottom: 12 }}>{int.provider}</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: int.status === 'connected' ? '#10B981' : int.status === 'error' ? '#DA1E28' : '#8C8C8C' }} />
                  <span style={{ fontSize: 12, textTransform: 'capitalize' }}>{int.status}</span>
                </div>
                {int.status === 'connected' ? (
                  <button onClick={() => disconnect(int.id)} style={{ background: '#E5E5E5', border: 'none', padding: '6px 12px', borderRadius: 4, fontSize: 11, cursor: 'pointer', width: '100%' }}>
                    Disconnect
                  </button>
                ) : (
                  <button onClick={() => connect(int.id)} style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: 4, fontSize: 11, cursor: 'pointer', width: '100%' }}>
                    Connect
                  </button>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}