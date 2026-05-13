'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Agent {
  id: string;
  name: string;
  description: string;
  provider: string;
  model: string;
  status: 'active' | 'inactive';
  version: string;
  updated_at: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

const tokens = {
  colors: { primary: '#6366f1', secondary: '#64748b', success: '#22c55e', background: '#f8fafc', card: '#ffffff', text: '#1e293b', textMuted: '#64748b', border: '#e2e8f0' },
  spacing: { xs: '4px', sm: '8px', md: '16px', lg: '24px', xl: '32px' },
  font: { family: 'Inter, system-ui, sans-serif', size: { small: '14px', body: '16px', h3: '20px', h2: '24px' } },
};

export default function AgentListPage() {
  const router = useRouter();
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [sort, setSort] = useState<'name' | 'date' | 'provider'>('name');
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { fetchAgents(); }, []);

  const fetchAgents = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (filter !== 'all') params.set('status', filter);
      if (search) params.set('search', search);
      const response = await fetch(`${API_BASE}/agents?${params}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      setAgents(data.agents || []);
    } catch (err) { setError(err instanceof Error ? err.message : 'Failed'); setAgents([]); }
    finally { setLoading(false); }
  };

  const filteredAgents = agents.sort((a, b) => {
    if (sort === 'name') return a.name.localeCompare(b.name);
    if (sort === 'date') return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
    return a.provider.localeCompare(b.provider);
  });

  return (
    <div style={{ minHeight: '100vh', background: tokens.colors.background, fontFamily: tokens.font.family, color: tokens.colors.text }}>
      <header style={{ background: tokens.colors.card, borderBottom: `1px solid ${tokens.colors.border}`, padding: `${tokens.spacing.md} ${tokens.spacing.xl}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, zIndex: 100 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.md }}>
          <span style={{ fontSize: '24px' }}>🤖</span>
          <h1 style={{ fontSize: tokens.font.size.h2, fontWeight: 600, margin: 0 }}>Agent Registry</h1>
        </div>
        <div style={{ display: 'flex', gap: tokens.spacing.sm }}>
          <Link href="/registry/new" style={{ background: tokens.colors.primary, color: 'white', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, borderRadius: '6px', textDecoration: 'none', fontWeight: 500 }}>+ New Agent</Link>
          <button aria-label="Settings" style={{ background: 'transparent', border: `1px solid ${tokens.colors.border}`, padding: tokens.spacing.sm, borderRadius: '6px', cursor: 'pointer', fontSize: '18px' }}>⚙️</button>
        </div>
      </header>

      <div style={{ padding: `${tokens.spacing.md} ${tokens.spacing.xl}`, display: 'flex', gap: tokens.spacing.md, flexWrap: 'wrap' }}>
        <input type="text" placeholder="Search agents..." value={search} onChange={(e) => setSearch(e.target.value)} style={{ flex: '1', minWidth: '200px', padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, outline: 'none' }} />
        <select value={filter} onChange={(e) => setFilter(e.target.value as typeof filter)} style={{ padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, background: 'white', cursor: 'pointer' }}>
          <option value="all">All</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        <select value={sort} onChange={(e) => setSort(e.target.value as typeof sort)} style={{ padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, border: `1px solid ${tokens.colors.border}`, borderRadius: '6px', fontSize: tokens.font.size.body, background: 'white', cursor: 'pointer' }}>
          <option value="name">Sort: Name</option>
          <option value="date">Sort: Date</option>
          <option value="provider">Sort: Provider</option>
        </select>
      </div>

      <main style={{ padding: `0 ${tokens.spacing.xl} ${tokens.spacing.xl}` }}>
        {loading ? <div style={{ textAlign: 'center', padding: tokens.spacing.xl, color: tokens.colors.textMuted }}>◌ Loading...</div> : error ? <div style={{ textAlign: 'center', padding: tokens.spacing.xl, color: tokens.colors.secondary, background: tokens.colors.card, borderRadius: '8px' }}>⚠️ {error}</div> : filteredAgents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: `${tokens.spacing.xl} * 3`, background: tokens.colors.card, borderRadius: '8px', border: `1px solid ${tokens.colors.border}` }}>
            <div style={{ fontSize: '48px', marginBottom: tokens.spacing.md }}>🔍</div>
            <h2 style={{ margin: `0 0 ${tokens.spacing.sm}` }}>No agents found</h2>
            <p style={{ color: tokens.colors.textMuted, margin: 0 }}>Try adjusting your search or create a new agent.</p>
          </div>
        ) : (
          <>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: tokens.spacing.md }}>
              {filteredAgents.map((agent) => (
                <div key={agent.id} style={{ background: tokens.colors.card, border: `1px solid ${tokens.colors.border}`, borderRadius: '8px', padding: tokens.spacing.md, cursor: 'pointer' }} onClick={() => router.push(`/registry/edit/${agent.id}`)}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: tokens.spacing.sm }}>
                    <h3 style={{ fontSize: tokens.font.size.h3, fontWeight: 600, margin: 0 }}>{agent.name}</h3>
                    <button aria-label="Menu" onClick={(e) => e.stopPropagation()} style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: tokens.spacing.xs, fontSize: '18px' }}>⋮</button>
                  </div>
                  <p style={{ color: tokens.colors.textMuted, fontSize: tokens.font.size.small, margin: `0 0 ${tokens.spacing.sm}` }}>{agent.provider.charAt(0).toUpperCase() + agent.provider.slice(1)} · {agent.model}</p>
                  <div style={{ display: 'flex', alignItems: 'center', gap: tokens.spacing.sm, marginBottom: tokens.spacing.sm }}>
                    <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: agent.status === 'active' ? tokens.colors.success : tokens.colors.secondary }} />
                    <span style={{ fontSize: tokens.font.size.small, color: agent.status === 'active' ? tokens.colors.success : tokens.colors.secondary }}>{agent.status === 'active' ? 'Active' : 'Inactive'}</span>
                    <span style={{ fontSize: tokens.font.size.small, color: tokens.colors.textMuted }}>v{agent.version}</span>
                  </div>
                  <div style={{ fontSize: tokens.font.size.small, color: tokens.colors.textMuted }}><span>Chat</span></div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: tokens.spacing.lg, textAlign: 'center', color: tokens.colors.textMuted, fontSize: tokens.font.size.small }}>Showing {filteredAgents.length} of {agents.length} agents</div>
          </>
        )}
      </main>
    </div>
  );
}