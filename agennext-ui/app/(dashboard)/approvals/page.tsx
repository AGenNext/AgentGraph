'use client';

import { useState } from "react";

interface AgentRequest {
  id: string;
  requester: string;
  name: string;
  framework: string;
  description: string;
  status: 'pending' | 'approved' | 'rejected';
  requestedAt: string;
  approvedAt?: string;
  agentId?: string;
  fields: {
    name: string;
    required: boolean;
    editableByEmployee: boolean;
    value: string;
    approval: 'pending' | 'approved' | 'rejected';
  }[];
}

const mockRequests: AgentRequest[] = [
  { id: 'r1', requester: 'john@company.com', name: 'Data Analyzer', framework: 'langgraph', description: 'Analyze datasets', status: 'pending', requestedAt: '2024-02-01', fields: [
    { name: 'Agent Name', required: true, editableByEmployee: true, value: 'Data Analyzer', approval: 'approved' },
    { name: 'Framework', required: true, editableByEmployee: false, value: 'langgraph', approval: 'approved' },
    { name: 'API Keys', required: true, editableByEmployee: false, value: 'sk-***', approval: 'pending' },
    { name: 'Tools', required: true, editableByEmployee: true, value: 'search,calc', approval: 'approved' },
  ]},
  { id: 'r2', requester: 'jane@company.com', name: 'Report Writer', framework: 'crewai', description: 'Write reports', status: 'pending', requestedAt: '2024-02-01', fields: [
    { name: 'Agent Name', required: true, editableByEmployee: true, value: 'Report Writer', approval: 'approved' },
    { name: 'Memory Limit', required: true, editableByEmployee: false, value: '16GB', approval: 'pending' },
  ]},
];

export default function ApprovalsPage() {
  const [requests, setRequests] = useState<AgentRequest[]>(mockRequests);

  const approve = (id: string) => {
    setRequests(requests.map(r => r.id === id ? { 
      ...r, 
      status: 'approved' as const, 
      approvedAt: new Date().toISOString().split('T')[0],
      agentId: `agent-${Date.now().toString().slice(-6)}`,
    } : r));
  };

  const reject = (id: string) => {
    setRequests(requests.map(r => r.id === id ? { ...r, status: 'rejected' as const } : r));
  };

  const approveField = (reqId: string, fieldName: string) => {
    setRequests(requests.map(r => {
      if (r.id !== reqId) return r;
      return {
        ...r,
        fields: r.fields.map(f => f.name === fieldName ? { ...f, approval: 'approved' as const } : f),
      };
    }));
  };

  return (
    <div style={{ minHeight: "100vh", background: "#F9FAFB", fontFamily: "'DM Sans', sans-serif" }}>
      <nav style={{ background: "white", borderBottom: "1px solid #E5E7EB", padding: "0 32px", height: 56, display: "flex", alignItems: "center", gap: 16 }}>
        <a href="/" style={{ fontSize: 13, color: "#6B7280", textDecoration: "none" }}>← Dashboard</a>
        <span style={{ fontWeight: 600, fontSize: 15 }}>Agent Approvals</span>
        <span style={{ marginLeft: 'auto', background: '#FEF3C7', color: '#D97706', padding: '2px 8px', borderRadius: 999, fontSize: 12 }}>
          {requests.filter(r => r.status === 'pending').length} pending
        </span>
      </nav>

      <div style={{ maxWidth: 800, margin: "0 auto", padding: "40px 24px" }}>
        <h1 style={{ marginBottom: 24, fontSize: 22, fontWeight: 700 }}>Agent Creation Requests</h1>
        <p style={{ marginBottom: 24, color: "#6B7280", fontSize: 14 }}>
          Employees request agents. Approve critical fields (API keys, memory, etc.) separately. Approved agents receive ID immediately.
        </p>

        {requests.filter(r => r.status === 'pending').length === 0 ? (
          <div style={{ padding: 48, textAlign: 'center', border: '2px dashed #E5E7EB', borderRadius: 12, color: '#9CA3AF' }}>
            ✓ No pending requests
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {requests.filter(r => r.status === 'pending').map(req => (
              <div key={req.id} style={{ background: 'white', borderRadius: 12, border: '1px solid #E5E7EB', overflow: 'hidden' }}>
                <div style={{ padding: 16, borderBottom: '1px solid #E5E7EB', background: '#F9FAFB' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 16 }}>{req.name}</div>
                      <div style={{ fontSize: 12, color: '#6B7280' }}>Requested by {req.requester} • {req.requestedAt}</div>
                    </div>
                    <span style={{ background: '#FEF3C7', color: '#D97706', padding: '4px 12px', borderRadius: 999, fontSize: 12, fontWeight: 500 }}>Pending</span>
                  </div>
                </div>

                <div style={{ padding: 16 }}>
                  <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 12 }}>Configuration Fields</div>
                  {req.fields.map(field => (
                    <div key={field.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid #F3F4F6' }}>
                      <div>
                        <span style={{ fontWeight: 500 }}>{field.name}</span>
                        {!field.editableByEmployee && <span style={{ fontSize: 10, marginLeft: 6, color: '#6B7280' }}>(admin only)</span>}
                        <div style={{ fontSize: 12, color: '#6B7280', fontFamily: 'monospace' }}>{field.value}</div>
                      </div>
                      <div>
                        {field.approval === 'approved' ? (
                          <span style={{ color: '#10B981', fontSize: 12 }}>✓ Approved</span>
                        ) : field.approval === 'rejected' ? (
                          <span style={{ color: '#DC2626', fontSize: 12 }}>✗ Rejected</span>
                        ) : field.editableByEmployee ? (
                          <span style={{ color: '#10B981', fontSize: 12 }}>Auto-approved</span>
                        ) : (
                          <button onClick={() => approveField(req.id, field.name)} style={{ background: '#0F62FE', color: 'white', border: 'none', padding: '4px 12px', borderRadius: 4, fontSize: 12, cursor: 'pointer' }}>
                            Approve Field
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                <div style={{ padding: 16, borderTop: '1px solid #E5E7EB', display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
                  <button onClick={() => reject(req.id)} style={{ background: '#DC2626', color: 'white', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
                    Reject
                  </button>
                  <button onClick={() => approve(req.id)} style={{ background: '#10B981', color: 'white', border: 'none', padding: '8px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer', fontWeight: 500 }}>
                    ✓ Approve & Create Agent
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {requests.filter(r => r.status !== 'pending').length > 0 && (
          <div style={{ marginTop: 32 }}>
            <h2 style={{ fontSize: 16, marginBottom: 16 }}>Processed Requests</h2>
            {requests.filter(r => r.status !== 'pending').map(req => (
              <div key={req.id} style={{ padding: 12, background: 'white', borderRadius: 8, marginBottom: 8, border: '1px solid #E5E7EB' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ fontWeight: 500 }}>{req.name}</span>
                  <span style={{ color: req.status === 'approved' ? '#10B981' : '#DC2626', fontSize: 12 }}>{req.status}</span>
                </div>
                {req.agentId && <div style={{ fontSize: 12, color: '#6B7280', marginTop: 4 }}>Agent ID: {req.agentId}</div>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
