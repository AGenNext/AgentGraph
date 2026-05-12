'use client';

import { useState } from 'react';

interface KnowledgeBase {
  id: string;
  name: string;
  documents: number;
  chunkSize: number;
  embedding: string;
  lastUpdated: string;
}

const mockKBs: KnowledgeBase[] = [
  { id: 'kb1', name: 'Product Docs', documents: 150, chunkSize: 512, embedding: 'text-embedding-3-small', lastUpdated: '2024-02-01' },
  { id: 'kb2', name: 'API Reference', documents: 80, chunkSize: 1024, embedding: 'text-embedding-3-small', lastUpdated: '2024-01-28' },
  { id: 'kb3', name: 'Support Articles', documents: 200, chunkSize: 256, embedding: 'ada-002', lastUpdated: '2024-01-15' },
];

export default function RAGPage() {
  const [kbs] = useState<KnowledgeBase[]>(mockKBs);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F4F4F4', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600 }}>RAG Knowledge Base</h1>
          <p style={{ color: '#525252' }}>Configure retrieval-augmented generation</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 4, cursor: 'pointer' }}>
          + New Knowledge Base
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{kbs.length}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Knowledge Bases</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{kbs.reduce((a, kb) => a + kb.documents, 0)}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Documents</div>
        </div>
        <div style={{ background: '#fff', padding: 16, borderRadius: 4 }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{kbs.reduce((a, kb) => a + kb.documents * kb.chunkSize, 0).toLocaleString()}</div>
          <div style={{ fontSize: 12, color: '#525252' }}>Total Tokens</div>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 4 }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F4F4F4' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>NAME</th>
              <th style={{ padding: 12, textAlign: 'left' }}>DOCUMENTS</th>
              <th style={{ padding: 12, textAlign: 'left' }}>CHUNK SIZE</th>
              <th style={{ padding: 12, textAlign: 'left' }}>EMBEDDING</th>
              <th style={{ padding: 12, textAlign: 'left' }}>UPDATED</th>
            </tr>
          </thead>
          <tbody>
            {kbs.map(kb => (
              <tr key={kb.id} style={{ borderBottom: '1px solid #E5E5E5', cursor: 'pointer' }}>
                <td style={{ padding: 12, fontWeight: 500 }}>{kb.name}</td>
                <td style={{ padding: 12 }}>{kb.documents}</td>
                <td style={{ padding: 12, fontFamily: 'monospace', fontSize: 12 }}>{kb.chunkSize}</td>
                <td style={{ padding: 12, fontSize: 12 }}>{kb.embedding}</td>
                <td style={{ padding: 12, fontSize: 12, color: '#525252' }}>{kb.lastUpdated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}