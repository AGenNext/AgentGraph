'use client';

import { useState } from 'react';

interface Contract {
  id: string;
  name: string;
  type: 'nda' | 'sla' | 'msa' | 'dpa';
  parties: string;
  status: 'active' | 'expiring' | 'expired';
  startDate: string;
  endDate: string;
}

const mockContracts: Contract[] = [
  { id: 'c1', name: 'Vendor NDA', type: 'nda', parties: 'Vendor Inc', status: 'active', startDate: '2024-01-01', endDate: '2025-01-01' },
  { id: 'c2', name: 'Service SLA', type: 'sla', parties: 'Cloud Provider', status: 'expiring', startDate: '2023-06-01', endDate: '2024-06-01' },
  { id: 'c3', name: 'Data Processing', type: 'dpa', parties: 'AI Services', status: 'active', startDate: '2024-01-15', endDate: '2025-01-15' },
  { id: 'c4', name: 'Master Agreement', type: 'msa', parties: 'Enterprise Corp', status: 'active', startDate: '2023-01-01', endDate: '2026-01-01' },
  { id: 'c5', name: 'Old NDA', type: 'nda', parties: 'Old Vendor', status: 'expired', startDate: '2022-01-01', endDate: '2023-01-01' },
];

export default function ContractsPage() {
  const [contracts] = useState<Contract[]>(mockContracts);

  const getLabel = (type: string) => ({ nda: 'NDA', sla: 'SLA', msa: 'MSA', dpa: 'DPA' }[type] || type);
  const getColor = (type: string) => ({ nda: '#7C3AED', sla: '#0F62FE', msa: '#10B981', dpa: '#F59E0B' }[type] || '#666');

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600 }}>Contracts</h1>
          <p style={{ color: '#525252' }}>Legal agreements & compliance</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 4, cursor: 'pointer' }}>
          + New Contract
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{contracts.length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{contracts.filter(c => c.status === 'active').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Active</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{contracts.filter(c => c.status === 'expiring').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Expiring</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{contracts.filter(c => c.status === 'expired').length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Expired</div>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead><tr style={{ background: '#F4F4F4' }}>
            <th style={{ padding: 12, textAlign: 'left' }}>CONTRACT</th>
            <th style={{ padding: 12, textAlign: 'left' }}>TYPE</th>
            <th style={{ padding: 12, textAlign: 'left' }}>PARTIES</th>
            <th style={{ padding: 12, textAlign: 'left' }}>START</th>
            <th style={{ padding: 12, textAlign: 'left' }}>END</th>
            <th style={{ padding: 12, textAlign: 'left' }}>STATUS</th>
          </tr></thead>
          <tbody>
            {contracts.map(c => (
              <tr key={c.id} style={{ borderBottom: '1px solid #E5E5E5' }}>
                <td style={{ padding: 12, fontWeight: 500 }}>{c.name}</td>
                <td style={{ padding: 12 }}>
                  <span style={{ background: getColor(c.type) + '20', color: getColor(c.type), padding: '4px 8px', borderRadius: 4, fontSize: 11 }}>
                    {getLabel(c.type)}
                  </span>
                </td>
                <td style={{ padding: 12, fontSize: 12 }}>{c.parties}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{c.startDate}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{c.endDate}</td>
                <td style={{ padding: 12, color: c.status === 'active' ? '#10B981' : c.status === 'expiring' ? '#F59E0B' : '#DA1E28', fontWeight: 500, fontSize: 12 }}>
                  {c.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}