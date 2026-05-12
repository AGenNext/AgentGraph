'use client';

import { useState } from 'react';

// Identity Assignment Workflow
interface IdentityAssignment {
  id: string;
  userId: string;
  user: string;
  role: string;
  assignedBy: string;
  assignedAt: string;
  status: 'active' | 'pending' | 'revoked';
}

const identityAssignments: IdentityAssignment[] = [
  { id: 'ia1', userId: 'u1', user: 'john.doe@company.com', role: 'Developer', assignedBy: 'admin@company.com', assignedAt: '2024-02-01', status: 'active' },
  { id: 'ia2', userId: 'u2', user: 'jane.smith@company.com', role: 'Viewer', assignedBy: 'admin@company.com', assignedAt: '2024-01-28', status: 'active' },
  { id: 'ia3', userId: 'u3', user: 'bob.wilson@company.com', role: 'Admin', assignedBy: 'admin@company.com', assignedAt: '2024-01-25', status: 'pending' },
];

// Lifecycle Management
interface LifecycleEvent {
  id: string;
  agent: string;
  action: 'created' | 'updated' | 'archived' | 'deployed';
  user: string;
  timestamp: string;
  status: 'completed' | 'in_progress' | 'failed';
}

const lifecycleEvents: LifecycleEvent[] = [
  { id: 'l1', agent: 'Research Agent', action: 'created', user: 'john.doe', timestamp: '2024-02-01 10:30', status: 'completed' },
  { id: 'l2', agent: 'Writer Agent', action: 'deployed', user: 'jane.smith', timestamp: '2024-02-01 09:15', status: 'completed' },
  { id: 'l3', agent: 'Analyzer Agent', action: 'updated', user: 'john.doe', timestamp: '2024-01-31 16:45', status: 'completed' },
  { id: 'l4', agent: 'Legacy Agent', action: 'archived', user: 'admin', timestamp: '2024-01-30 14:20', status: 'completed' },
];

// Access Request
interface AccessRequest {
  id: string;
  requester: string;
  resource: string;
  accessLevel: string;
  reason: string;
  requestedAt: string;
  status: 'approved' | 'pending' | 'denied';
  approver?: string;
}

const accessRequests: AccessRequest[] = [
  { id: 'ar1', requester: 'john.doe', resource: 'Production Agents', accessLevel: 'Write', reason: 'Need to deploy new agent', requestedAt: '2024-02-01', status: 'approved', approver: 'admin' },
  { id: 'ar2', requester: 'jane.smith', resource: 'Finance Dashboard', accessLevel: 'Read', reason: 'Monthly reporting', requestedAt: '2024-01-31', status: 'pending' },
  { id: 'ar3', requester: 'bob.wilson', resource: 'Admin Panel', accessLevel: 'Admin', reason: 'System configuration', requestedAt: '2024-01-30', status: 'denied', approver: 'admin' },
];

// Access Review
interface AccessReview {
  id: string;
  reviewer: string;
  resource: string;
  lastReview: string;
  risk: 'low' | 'medium' | 'high';
  status: 'compliant' | 'non_compliant' | 'pending';
}

const accessReviews: AccessReview[] = [
  { id: 'rv1', reviewer: 'john.doe', resource: 'AWS Console', lastReview: '2024-02-01', risk: 'low', status: 'compliant' },
  { id: 'rv2', reviewer: 'jane.smith', resource: 'Azure Portal', lastReview: '2024-01-28', risk: 'medium', status: 'non_compliant' },
  { id: 'rv3', reviewer: 'admin', resource: 'Database Access', lastReview: '2024-01-25', risk: 'high', status: 'pending' },
];

// Security Audit
interface SecurityAudit {
  id: string;
  check: string;
  category: string;
  passed: boolean;
  findings: number;
  lastRun: string;
}

const securityAudits: SecurityAudit[] = [
  { id: 'sa1', check: 'Password Policy', category: 'IAM', passed: true, findings: 0, lastRun: '2024-02-01' },
  { id: 'sa2', check: 'MFA Enforcement', category: 'IAM', passed: true, findings: 0, lastRun: '2024-02-01' },
  { id: 'sa3', check: 'Session Timeout', category: 'Authentication', passed: false, findings: 12, lastRun: '2024-02-01' },
  { id: 'sa4', check: 'Encryption at Rest', category: 'Data', passed: true, findings: 0, lastRun: '2024-02-01' },
  { id: 'sa5', check: 'API Key Rotation', category: 'Secrets', passed: false, findings: 3, lastRun: '2024-02-01' },
  { id: 'sa6', check: 'Vulnerability Scan', category: 'Infrastructure', passed: true, findings: 0, lastRun: '2024-02-01' },
];

export default function WorkflowsPage() {
  const [tab, setTab] = useState<'identity' | 'lifecycle' | 'access' | 'review' | 'audit'>('identity');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Enterprise Workflows</h1>
        <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Identity, lifecycle, access & security automation</p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24, flexWrap: 'wrap' }}>
        {[
          { id: 'identity', label: 'Identity Assignment' },
          { id: 'lifecycle', label: 'Lifecycle' },
          { id: 'access', label: 'Access Request' },
          { id: 'review', label: 'Access Reviews' },
          { id: 'audit', label: 'Security Audit' },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id as typeof tab)}
            style={{
              background: tab === t.id ? '#1A1A2E' : '#fff',
              color: tab === t.id ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 16px',
              borderRadius: 8,
              fontSize: 12,
              cursor: 'pointer',
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'identity' ? (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: 600 }}>Identity Assignment</h2>
            <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              + Assign Identity
            </button>
          </div>
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>USER</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ROLE</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ASSIGNED BY</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>DATE</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                </tr>
              </thead>
              <tbody>
                {identityAssignments.map(a => (
                  <tr key={a.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{a.user}</td>
                    <td style={{ padding: '14px 16px' }}>{a.role}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{a.assignedBy}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{a.assignedAt}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ color: a.status === 'active' ? '#10B981' : a.status === 'pending' ? '#F59E0B' : '#DA1E28', fontSize: 12, fontWeight: 500, textTransform: 'capitalize' }}>
                        {a.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : tab === 'lifecycle' ? (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: 600 }}>Lifecycle Management</h2>
            <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              + New Event
            </button>
          </div>
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>AGENT</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTION</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>USER</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>TIMESTAMP</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                </tr>
              </thead>
              <tbody>
                {lifecycleEvents.map(l => (
                  <tr key={l.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{l.agent}</td>
                    <td style={{ padding: '14px 16px', textTransform: 'capitalize', fontSize: 12 }}>{l.action}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{l.user}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{l.timestamp}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ color: l.status === 'completed' ? '#10B981' : l.status === 'in_progress' ? '#F59E0B' : '#DA1E28', fontSize: 12, fontWeight: 500 }}>
                        {l.status === 'completed' ? '✓' : l.status === 'in_progress' ? '⏳' : '✗'} {l.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : tab === 'access' ? (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: 600 }}>Access Request</h2>
            <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              + New Request
            </button>
          </div>
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>REQUESTER</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RESOURCE</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACCESS LEVEL</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>REASON</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                </tr>
              </thead>
              <tbody>
                {accessRequests.map(a => (
                  <tr key={a.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{a.requester}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{a.resource}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{a.accessLevel}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280', maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>{a.reason}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ color: a.status === 'approved' ? '#10B981' : a.status === 'denied' ? '#DA1E28' : '#F59E0B', fontSize: 12, fontWeight: 500, textTransform: 'capitalize' }}>
                        {a.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : tab === 'review' ? (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: 600 }}>Access Reviews</h2>
            <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              + Schedule Review
            </button>
          </div>
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>REVIEWER</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RESOURCE</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>LAST REVIEW</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RISK</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                </tr>
              </thead>
              <tbody>
                {accessReviews.map(a => (
                  <tr key={a.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{a.reviewer}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12 }}>{a.resource}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{a.lastReview}</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ 
                        background: a.risk === 'low' ? '#10B98120' : a.risk === 'medium' ? '#F59E0B20' : '#DA1E2820',
                        color: a.risk === 'low' ? '#10B981' : a.risk === 'medium' ? '#F59E0B' : '#DA1E28',
                        padding: '4px 8px', borderRadius: 4, fontSize: 11, textTransform: 'capitalize',
                      }}>
                        {a.risk}
                      </span>
                    </td>
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ color: a.status === 'compliant' ? '#10B981' : a.status === 'non_compliant' ? '#DA1E28' : '#F59E0B', fontSize: 12, fontWeight: 500, textTransform: 'capitalize' }}>
                        {a.status.replace('_', ' ')}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <h2 style={{ fontSize: 18, fontWeight: 600 }}>Security Audit</h2>
            <button style={{ background: '#DA1E28', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              Run Audit
            </button>
          </div>
          <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#F8F9FA' }}>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>CHECK</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>CATEGORY</th>
                  <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                  <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>FINDINGS</th>
                  <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>LAST RUN</th>
                </tr>
              </thead>
              <tbody>
                {securityAudits.map(s => (
                  <tr key={s.id} style={{ borderTop: '1px solid #F4F4F4' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 500 }}>{s.check}</td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{s.category}</td>
                    <td style={{ padding: '14px 16px', textAlign: 'center' }}>
                      <span style={{ color: s.passed ? '#10B981' : '#DA1E28', fontSize: 18 }}>
                        {s.passed ? '✓' : '✗'}
                      </span>
                    </td>
                    <td style={{ padding: '14px 16px', textAlign: 'center', fontWeight: s.findings > 0 ? 600 : 400, color: s.findings > 0 ? '#DA1E28' : '#6B7280' }}>
                      {s.findings}
                    </td>
                    <td style={{ padding: '14px 16px', fontSize: 12, color: '#6B7280' }}>{s.lastRun}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}