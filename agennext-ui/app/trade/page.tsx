'use client';

import { useState } from 'react';

interface AgentListing {
  id: string;
  name: string;
  description: string;
  creator: string;
  rating: number;
  sales: number;
  price: number;
  tags: string[];
}

const featuredAgents: AgentListing[] = [
  { id: 'a1', name: 'Legal Research Pro', description: 'Advanced legal document analysis and case law search', creator: 'LegalTech Inc', rating: 4.8, sales: 245, price: 199, tags: ['Legal', 'Research'] },
  { id: 'a2', name: 'Medical Scribe', description: 'Automated medical notes and clinical documentation', creator: 'HealthAI', rating: 4.9, sales: 189, price: 299, tags: ['Healthcare', 'Documentation'] },
  { id: 'a3', name: 'Financial Analyst', description: 'Stock analysis, portfolio management, and predictions', creator: 'FinTech Pro', rating: 4.7, sales: 156, price: 249, tags: ['Finance', 'Analysis'] },
  { id: 'a4', name: 'Code Reviewer', description: 'Automated code review with best practices enforcement', creator: 'DevTools Co', rating: 4.6, sales: 312, price: 149, tags: ['Development', 'Code'] },
  { id: 'a5', name: 'Customer Support Pro', description: 'AI-powered customer service with CRM integration', creator: 'SupportTech', rating: 4.8, sales: 428, price: 349, tags: ['Support', 'CRM'] },
  { id: 'a6', name: 'Content Writer Pro', description: 'SEO-optimized content generation for marketing', creator: 'MarketingAI', rating: 4.5, sales: 198, price: 179, tags: ['Marketing', 'Content'] },
];

const myListings = [
  { name: 'Research Assistant v2', status: 'active', views: 156, purchases: 12, revenue: 2388 },
  { name: 'Data Analyzer', status: 'active', views: 89, purchases: 5, revenue: 1245 },
];

export default function TradePage() {
  const [activeTab, setActiveTab] = useState<'discover' | 'my-agents' | 'publish'>('discover');
  const [search, setSearch] = useState('');
  
  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Agent Trade Protocol</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Discover, buy, and sell custom AI agents</p>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {(['discover', 'my-agents', 'publish'] as const).map(t => (
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
            {t === 'discover' ? 'Discover Agents' : t === 'my-agents' ? 'My Listings' : 'Publish Agent'}
          </button>
        ))}
      </div>

      {activeTab === 'discover' ? (
        <>
          {/* Search */}
          <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
            <input
              placeholder="Search agents..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ flex: 1, padding: '12px 16px', borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14 }}
            />
            <select style={{ padding: '12px 16px', borderRadius: 8, border: '1px solid #E5E5E5', background: '#fff' }}>
              <option>All Categories</option>
              <option>Development</option>
              <option>Finance</option>
              <option>Legal</option>
              <option>Healthcare</option>
              <option>Marketing</option>
            </select>
            <select style={{ padding: '12px 16px', borderRadius: 8, border: '1px solid #E5E5E5', background: '#fff' }}>
              <option>Sort: Popular</option>
              <option>Sort: Newest</option>
              <option>Sort: Price Low</option>
              <option>Sort: Price High</option>
            </select>
          </div>

          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600 }}>1,247</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Total Agents</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>342</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Creators</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>$89K</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Total Sales</div>
            </div>
            <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
              <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>4.7</div>
              <div style={{ fontSize: 12, color: '#6B7280' }}>Avg Rating</div>
            </div>
          </div>

          {/* Agent Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
            {featuredAgents.map(agent => (
              <div key={agent.id} style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 20 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
                  <div style={{ fontSize: 16, fontWeight: 600 }}>{agent.name}</div>
                  <div style={{ fontSize: 18, fontWeight: 700, color: '#10B981' }}>${agent.price}</div>
                </div>
                <p style={{ fontSize: 13, color: '#6B7280', marginBottom: 12, lineHeight: 1.5 }}>{agent.description}</p>
                
                <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
                  {agent.tags.map(tag => (
                    <span key={tag} style={{ background: '#F4F4F4', padding: '2px 8px', borderRadius: 4, fontSize: 11, color: '#6B7280' }}>
                      {tag}
                    </span>
                  ))}
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <div style={{ fontSize: 12, color: '#6B7280' }}>by {agent.creator}</div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                    <span>⭐ {agent.rating}</span>
                    <span style={{ color: '#6B7280', fontSize: 12 }}>({agent.sales})</span>
                  </div>
                </div>

                <button style={{ width: '100%', background: '#667EEA', color: '#fff', border: 'none', padding: '10px 0', borderRadius: 8, fontSize: 13, cursor: 'pointer' }}>
                  Purchase Agent
                </button>
              </div>
            ))}
          </div>
        </>
      ) : activeTab === 'my-agents' ? (
        <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#F8F9FA' }}>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>AGENT</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>STATUS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>VIEWS</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>PURCHASES</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>REVENUE</th>
                <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>ACTIONS</th>
              </tr>
            </thead>
            <tbody>
              {myListings.map((agent, i) => (
                <tr key={i} style={{ borderTop: '1px solid #F4F4F4' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 500 }}>{agent.name}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{ color: '#10B981', fontSize: 12, fontWeight: 500 }}>● Active</span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{agent.views}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12 }}>{agent.purchases}</td>
                  <td style={{ padding: '14px 16px', fontSize: 12, fontWeight: 600 }}>${agent.revenue}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <button style={{ background: 'transparent', border: '1px solid #E5E5E5', padding: '4px 10px', borderRadius: 4, fontSize: 11, cursor: 'pointer', marginRight: 8 }}>Edit</button>
                    <button style={{ background: 'transparent', border: '1px solid #E5E5E5', padding: '4px 10px', borderRadius: 4, fontSize: 11, cursor: 'pointer' }}>Delist</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ background: '#fff', borderRadius: 12, border: '1px solid #E5E5E5', padding: 32, maxWidth: 600, margin: '0 auto' }}>
          <h3 style={{ fontSize: 18, fontWeight: 600, marginBottom: 24, textAlign: 'center' }}>Publish Your Agent</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div>
              <label style={{ fontSize: 12, color: '#6B7280', display: 'block', marginBottom: 6 }}>Agent Name</label>
              <input placeholder="e.g., Legal Research Pro" style={{ width: '100%', padding: 12, borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14 }} />
            </div>
            <div>
              <label style={{ fontSize: 12, color: '#6B7280', display: 'block', marginBottom: 6 }}>Description</label>
              <textarea placeholder="Describe what your agent does..." rows={4} style={{ width: '100%', padding: 12, borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14, resize: 'vertical' }} />
            </div>
            <div>
              <label style={{ fontSize: 12, color: '#6B7280', display: 'block', marginBottom: 6 }}>Price ($)</label>
              <input type="number" placeholder="199" style={{ width: '100%', padding: 12, borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14 }} />
            </div>
            <div>
              <label style={{ fontSize: 12, color: '#6B7280', display: 'block', marginBottom: 6 }}>Category</label>
              <select style={{ width: '100%', padding: 12, borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14 }}>
                <option>Development</option>
                <option>Finance</option>
                <option>Legal</option>
                <option>Healthcare</option>
                <option>Marketing</option>
                <option>Support</option>
              </select>
            </div>
            <button style={{ background: '#667EEA', color: '#fff', border: 'none', padding: '14px 0', borderRadius: 8, fontSize: 14, fontWeight: 500, cursor: 'pointer', marginTop: 8 }}>
              Publish Agent
            </button>
          </div>
        </div>
      )}
    </div>
  );
}