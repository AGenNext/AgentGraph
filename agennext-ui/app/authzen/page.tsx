'use client';

import { useState } from 'react';

interface Policy {
  id: string;
  name: string;
  effect: 'allow' | 'deny';
  principals: string[];
  resources: string[];
  actions: string[];
  conditions: string[];
  status: 'active' | 'draft' | 'disabled';
}

const policies: Policy[] = [
  { id: 'p1', name: 'Admin Full Access', effect: 'allow', principals: ['role:admin'], resources: ['*'], actions: ['*'], conditions: [], status: 'active' },
  { id: 'p2', name: 'Agent Creator', effect: 'allow', principals: ['role:developer'], resources: ['agent:create', 'agent:edit'], actions: ['*'], conditions: [], status: 'active' },
  { id: 'p3', name: 'Viewer Read Only', effect: 'allow', principals: ['role:viewer'], resources: ['*'], actions: ['read'], conditions: [], status: 'active' },
  { id: 'p4', name: 'Deny Production Delete', effect: 'deny', principals: ['*'], resources: ['prod:*'], actions: ['delete'], conditions: ['env:production'], status: 'active' },
  { id: 'p5', name: 'Finance Access', effect: 'allow', principals: ['group:finance'], resources: ['finance:*', 'contracts:*'], actions: ['*'], conditions: [], status: 'draft' },
  { id: 'p6', name: 'External API Key', effect: 'allow', principals: ['api-key:*'], resources: ['api:*'], actions: ['read', 'write'], conditions: ['rate-limit:100'], status: 'active' },
];

const recentDecisions = [
  { id: 'd1', policy: 'Admin Full Access', principal: 'john@company.com', resource: 'agents/*', action: 'read', decision: '✅ Allow', time: '10ms ago' },
  { id: 'd2', policy: 'Viewer Read Only', principal: 'jane@company.com', resource: 'agents/delete', action: 'write', decision: '❌ Deny', time: '10ms ago' },
  { id: 'd3', policy: 'Agent Creator', principal: 'dev@company.com', resource: 'agent:create', action: 'create', decision: '✅ Allow', time: '12ms ago' },
  { id: 'd4', policy: 'Deny Production Delete', principal: 'unknown', resource: 'prod:agents', action: 'delete', decision: '❌ Deny', time: '8ms ago' },
];

const roles = [
  { name: 'Admin', users: 3, permissions: 24, description: 'Full system access' },
  { name: 'Developer', users: 12, permissions: 16, description: 'Create and edit agents' },
  { name: 'Viewer', users: 45, permissions: 8, description: 'Read-only access' },
  { name: 'Finance', users: 5, permissions: 12, description: 'Finance and contracts' },
  { name: 'External API', users: 89, permissions: 4, description: 'Limited API access' },
];

export default function AuthzenPage() {
  const [activeTab, setActiveTab] = useState<'policies' | 'roles' | 'decisions'>('policies');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>AuthZen</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Zero Trust Authorization & Access Control</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + New Policy
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['policies', 'roles', 'decisions'] as const).map(t => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            style={{
              background: activeTab === t ? '#1A1A2E' : '#fff',
              color: activeTab === t ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 20px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {t === 'policies' ? 'Policies' : t === 'roles' ? 'Roles' : 'Decision Log'}
          </button>
        ))}
      </div>

      {activeTab === 'policies' ? (
        <>
          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{policies.length}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Total Policies</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{policies.filter(p => p.status === 'active').length}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Active</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{policies.filter(p => p.status === 'draft').length}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Draft</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>{roles.reduce((a, r) => a + r.users, 0)}</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Bound Principals</div>
            </div>
          </div>

          {/* Policy Table */}
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>POLICY</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>EFFECT</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>PRINCIPALS</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RESOURCES</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTIONS</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                </tr>
              </thead>
              <tbody>
                {policies.map(p => (
                  <tr key={p.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{p.name}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ 
                        color: p.effect === 'allow' ? '#10B981' : '#DA1E28', 
                        fontSize: 12, 
                        fontWeight: 500,
                        textTransform: 'uppercase',
                      }}>
                        {p.effect}
                      </span>
                    </td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{p.principals.join(', ')}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{p.resources.join(', ')}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{p.actions.join(', ')}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ 
                        color: p.status === 'active' ? '#10B981' : p.status === 'draft' ? '#F59E0B' : '#6B7280',
                        fontSize: 12,
                        fontWeight: 500,
                      }}>
                        {p.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : activeTab === 'roles' ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {roles.map(role => (
            <div key={role.name} style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontSize: 18, fontWeight: 600, marginBottom: 4 }}>{role.name}</div>
                  <div style={{ fontSize: 12, color: '#6B7280' }}>{role.description}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: 24, fontWeight: 600, color: '#667EEA' }}>{role.users}</div>
                  <div style={{ fontSize: 11, color: '#6B7280' }}>users</div>
                </div>
              </div>
              <div style={{ marginTop: 16, paddingTop: 16, borderTop: '1px solid #F4F4F4' }}>
                <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 8 }}>Permissions ({role.permissions})</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                  {['read', 'write', 'delete', 'admin'].slice(0, Math.min(4, role.permissions / 4)).map(perm => (
                    <span key={perm} style={{ background: '#F4F4F4', padding: '2px 8px', borderRadius: 4, fontSize: 11, color: '#6B7280' }}>
                      {perm}
                    </span>
                  ))}
                  {role.permissions > 16 && (
                    <span style={{ background: '#F4F4F4', padding: '2px 8px', borderRadius: 4, fontSize: 11, color: '#6B7280' }}>
                      +{role.permissions - 16} more
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>POLICY</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>PRINCIPAL</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RESOURCE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTION</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DECISION</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>LATENCY</th>
              </tr>
            </thead>
            <tbody>
              {recentDecisions.map(d => (
                <tr key={d.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontWeight: 500 }}>{d.policy}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{d.principal}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontFamily: 'monospace' }}>{d.resource}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, textTransform: 'uppercase' }}>{d.action}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontWeight: 500, color: d.decision.includes('Allow') ? '#10B981' : '#DA1E28' }}>
                    {d.decision}
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{d.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}