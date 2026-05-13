'use client';

import { useState } from 'react';
import crypto from 'crypto';

interface VerifiableCredential {
  id: string;
  type: string;
  issuer: string;
  subject: string;
  issued: string;
  expires: string;
  status: 'valid' | 'revoked' | 'expired';
  schema: string;
  signature?: string;
}

const initialCredentials: VerifiableCredential[] = [
  { id: 'did:ebsi:zABC123DEF456', type: 'VerifiableID', issuer: 'did:ebsi:z12ABcdefGHI', subject: 'did:agent:user1', issued: '2024-01-15', expires: '2025-01-15', status: 'valid', schema: 'Schema2024', signature: '0x7d5a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4' },
  { id: 'did:ebsi:zDEF789GHI012', type: 'KYC', issuer: 'did:ebsi:z34CDefghJKL', subject: 'did:agent:user2', issued: '2024-02-01', expires: '2025-02-01', status: 'valid', schema: 'KYCSchema', signature: '0x8b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5' },
  { id: 'did:ebsi:zGHI345JKL678', type: 'Employment', issuer: 'did:ebsi:z56EFghijMNO', subject: 'did:agent:user3', issued: '2023-06-01', expires: '2024-06-01', status: 'expired', schema: 'EmploymentSchema', signature: '0x9c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9' },
];

export default function WaltIdPage() {
  const [credentials, setCredentials] = useState<VerifiableCredential[]>(initialCredentials);
  const [selected, setSelected] = useState<string | null>(null);

  const handleVerify = (id: string) => {
    setCredentials(creds => creds.map(c => c.id === id && c.status === 'valid' ? { ...c, status: 'revoked' } : c));
  };

  const handlePresent = (id: string) => {
    alert(`Presented credential ${id} for verification`);
  };

  return (
    <div style={{ padding: 24, background: '#0D1117', minHeight: '100vh', color: '#fff' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h1 style={{ fontSize: 24 }}>Verified Credentials</h1>
        <button style={{ padding: '8px 16px', background: '#238636', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer' }}>+ Issue Credential</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 16 }}>
        {credentials.map(vc => (
          <div key={vc.id} onClick={() => setSelected(vc.id)} style={{
            padding: 16, background: selected === vc.id ? '#30363D' : '#21262D',
            borderRadius: 8, cursor: 'pointer', border: selected === vc.id ? '2px solid #58A6FF' : '2px solid transparent'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <div>
                <strong>{vc.type}</strong>
                <p style={{ color: '#8C8C8C', fontSize: 12, marginTop: 4 }}>{vc.id}</p>
              </div>
              <span style={{
                fontSize: 12, padding: '2px 8px', borderRadius: 4,
                background: vc.status === 'valid' ? '#10B98133' : vc.status === 'revoked' ? '#F8514933' : '#F8514933',
                color: vc.status === 'valid' ? '#10B981' : '#F85149'
              }}>{vc.status}</span>
            </div>
            <p style={{ color: '#8C8C8C', fontSize: 14, margin: '4px 0' }}>Issuer: {vc.issuer}</p>
            <p style={{ color: '#8C8C8C', fontSize: 14, margin: '4px 0' }}>Subject: {vc.subject}</p>
            <p style={{ color: '#8C8C8C', fontSize: 14, margin: '4px 0' }}>Schema: {vc.schema}</p>
            <p style={{ color: '#58A6FF', fontSize: 12, margin: '4px 0', wordBreak: 'break-all' }}>␎ {vc.signature?.slice(0, 20)}...</p>
            <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
              <button onClick={(e) => { e.stopPropagation(); handleVerify(vc.id); }} style={{ flex: 1, padding: 8, background: '#30363D', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', fontSize: 12 }}>Revoke</button>
              <button onClick={(e) => { e.stopPropagation(); handlePresent(vc.id); }} style={{ flex: 1, padding: 8, background: '#238636', border: 'none', borderRadius: 6, color: '#fff', cursor: 'pointer', fontSize: 12 }}>Present</button>
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 24, padding: 16, background: '#21262D', borderRadius: 8 }}>
        <h3 style={{ marginBottom: 12 }}>Credential Statistics</h3>
        <div style={{ display: 'flex', gap: 24 }}>
          <div><span style={{ color: '#10B981' }}>{credentials.filter(c => c.status === 'valid').length}</span> Valid</div>
          <div><span style={{ color: '#F85149' }}>{credentials.filter(c => c.status === 'revoked').length}</span> Revoked</div>
          <div><span style={{ color: '#F85149' }}>{credentials.filter(c => c.status === 'expired').length}</span> Expired</div>
        </div>
      </div>
    </div>
  );
}