'use client';

import { useState } from 'react';

interface AgentCapability {
  name: string;
  enabled: boolean;
}

interface AgentCard {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  creator: string;
  version: string;
  created: string;
  updated: string;
  downloads: number;
  rating: number;
  price: number;
  runtime: string;
  model: string;
  context: number;
  capabilities: AgentCapability[];
  tags: string[];
  status: 'active' | 'draft' | 'deprecated';
}

const agentCards: AgentCard[] = [
  {
    id: 'research-agent',
    name: 'Research Agent',
    description: 'Advanced research assistant for academic papers, market analysis, and technical documentation',
    icon: '🔬',
    color: '#667EEA',
    creator: 'AGenNext',
    version: '3.2.0',
    created: '2024-01-15',
    updated: '2024-02-01',
    downloads: 12500,
    rating: 4.8,
    price: 0,
    runtime: 'AWS Bedrock',
    model: 'Claude 3.5 Sonnet',
    context: 200000,
    capabilities: [
      { name: 'web_search', enabled: true },
      { name: 'pdf_analysis', enabled: true },
      { name: 'code_interpretation', enabled: true },
      { name: 'multi_language', enabled: true },
    ],
    tags: ['Research', 'Academic', 'Analysis'],
    status: 'active',
  },
  {
    id: 'writer-agent',
    name: 'Writer Agent',
    description: 'Professional content writer for blogs, marketing copy, and technical documentation',
    icon: '✍️',
    color: '#10B981',
    creator: 'ContentAI',
    version: '2.5.0',
    created: '2024-01-20',
    updated: '2024-01-28',
    downloads: 8900,
    rating: 4.7,
    price: 49,
    runtime: 'Azure OpenAI',
    model: 'GPT-4o',
    context: 128000,
    capabilities: [
      { name: 'seo_optimization', enabled: true },
      { name: 'tone_styling', enabled: true },
      { name: 'multi_language', enabled: true },
      { name: 'plagiarism_check', enabled: false },
    ],
    tags: ['Writing', 'Marketing', 'SEO'],
    status: 'active',
  },
  {
    id: 'analyzer-agent',
    name: 'Data Analyzer',
    description: 'Advanced data analysis with visualization, statistical modeling, and ML insights',
    icon: '📊',
    color: '#F59E0B',
    creator: 'DataScience Pro',
    version: '4.0.0',
    created: '2023-12-10',
    updated: '2024-01-25',
    downloads: 15600,
    rating: 4.9,
    price: 99,
    runtime: 'Google Vertex',
    model: 'Gemini 1.5 Pro',
    context: 2000000,
    capabilities: [
      { name: 'python_execution', enabled: true },
      { name: 'visualization', enabled: true },
      { name: 'ml_insights', enabled: true },
      { name: 'sql_query', enabled: true },
    ],
    tags: ['Data', 'Analytics', 'ML'],
    status: 'active',
  },
  {
    id: 'code-agent',
    name: 'Code Assistant',
    description: 'AI-powered code review, debugging, and engineering assistant',
    icon: '💻',
    color: '#7C3AED',
    creator: 'DevTools Inc',
    version: '1.8.0',
    created: '2024-01-05',
    updated: '2024-01-30',
    downloads: 22400,
    rating: 4.8,
    price: 0,
    runtime: 'AWS Bedrock',
    model: 'Llama 3.1 70B',
    context: 128000,
    capabilities: [
      { name: 'code_completion', enabled: true },
      { name: 'bug_detection', enabled: true },
      { name: 'security_scan', enabled: true },
      { name: 'refactoring', enabled: true },
    ],
    tags: ['Development', 'Code', 'Security'],
    status: 'active',
  },
  {
    id: 'support-agent',
    name: 'Customer Support',
    description: 'Intelligent customer service agent with CRM integration and ticket management',
    icon: '🎧',
    color: '#DA1E28',
    creator: 'SupportTech',
    version: '3.0.0',
    created: '2023-11-20',
    updated: '2024-01-15',
    downloads: 31200,
    rating: 4.6,
    price: 149,
    runtime: 'Azure OpenAI',
    model: 'GPT-4 Turbo',
    context: 128000,
    capabilities: [
      { name: 'crm_integration', enabled: true },
      { name: 'ticket_routing', enabled: true },
      { name: 'sentiment_analysis', enabled: true },
      { name: 'knowledge_base', enabled: true },
    ],
    tags: ['Support', 'CRM', 'Service'],
    status: 'active',
  },
  {
    id: 'legal-agent',
    name: 'Legal Assistant',
    description: 'Legal research, contract analysis, and compliance checking for law professionals',
    icon: '⚖️',
    color: '#0F62FE',
    creator: 'LegalTech',
    version: '2.1.0',
    created: '2024-01-10',
    updated: '2024-01-28',
    downloads: 4500,
    rating: 4.5,
    price: 199,
    runtime: 'Anthropic',
    model: 'Claude Opus 4',
    context: 200000,
    capabilities: [
      { name: 'case_law_search', enabled: true },
      { name: 'contract_review', enabled: true },
      { name: 'compliance_check', enabled: true },
      { name: 'citation_gen', enabled: true },
    ],
    tags: ['Legal', 'Research', 'Compliance'],
    status: 'active',
  },
  {
    id: 'medical-agent',
    name: 'Medical Scribe',
    description: 'Clinical documentation assistant for healthcare providers with HIPAA compliance',
    icon: '🏥',
    color: '#10B981',
    creator: 'HealthAI',
    version: '4.2.0',
    created: '2023-10-15',
    updated: '2024-02-01',
    downloads: 7800,
    rating: 4.9,
    price: 299,
    runtime: 'Google Vertex',
    model: 'Gemini 1.5 Pro',
    context: 2000000,
    capabilities: [
      { name: 'clinical_notes', enabled: true },
      { name: 'hipaa_compliance', enabled: true },
      { name: 'coding_assist', enabled: true },
      { name: 'drug_interaction', enabled: true },
    ],
    tags: ['Healthcare', 'Medical', 'HIPAA'],
    status: 'active',
  },
  {
    id: 'triage-agent',
    name: 'Triage Agent',
    description: 'Intelligent routing and prioritization for support tickets and escalations',
    icon: '📋',
    color: '#F59E0B',
    creator: 'AGenNext',
    version: '1.5.0',
    created: '2023-12-01',
    updated: '2024-01-20',
    downloads: 18900,
    rating: 4.4,
    price: 0,
    runtime: 'AWS Bedrock',
    model: 'Claude 3 Haiku',
    context: 200000,
    capabilities: [
      { name: 'priority_scoring', enabled: true },
      { name: 'auto_routing', enabled: true },
      { name: 'sla_tracking', enabled: true },
    ],
    tags: ['Automation', 'Routing', 'SLA'],
    status: 'active',
  },
  {
    id: 'finance-agent',
    name: 'Financial Analyst',
    description: 'Stock analysis, portfolio management, and market prediction assistant',
    icon: '📈',
    color: '#10B981',
    creator: 'FinTech Pro',
    version: '2.3.0',
    created: '2023-11-10',
    updated: '2024-01-25',
    downloads: 11200,
    rating: 4.7,
    price: 149,
    runtime: 'Cohere',
    model: 'Command R+',
    context: 128000,
    capabilities: [
      { name: 'stock_analysis', enabled: true },
      { name: 'portfolio_opt', enabled: true },
      { name: 'risk_assessment', enabled: true },
      { name: 'market_news', enabled: true },
    ],
    tags: ['Finance', 'Trading', 'Investment'],
    status: 'active',
  },
];

export default function AgentCardsPage() {
  const [filter, setFilter] = useState<'all' | 'free' | 'paid'>('all');
  const [search, setSearch] = useState('');
  
  const filteredAgents = agentCards.filter(a => {
    if (filter === 'free' && a.price > 0) return false;
    if (filter === 'paid' && a.price === 0) return false;
    if (search && !a.name.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Agent Cards</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Enterprise AI agent marketplace</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + Create Agent
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{agentCards.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Agents</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{agentCards.filter(a => a.price === 0).length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Free</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#F59E0B' }}>{agentCards.reduce((a, b) => a + b.downloads, 0).toLocaleString()}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Downloads</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{(agentCards.reduce((a, b) => a + b.rating, 0) / agentCards.length).toFixed(1)}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Avg Rating</div>
        </div>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
        <input
          placeholder="Search agents..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ flex: 1, padding: '12px 16px', borderRadius: 8, border: '1px solid #E5E5E5', fontSize: 14 }}
        />
        {(['all', 'free', 'paid'] as const).map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              background: filter === f ? '#1A1A2E' : '#fff',
              color: filter === f ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '10px 16px',
              borderRadius: 8,
              fontSize: 13,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {f === 'all' ? 'All' : f === 'free' ? 'Free' : 'Paid'}
          </button>
        ))}
      </div>

      {/* Agent Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
        {filteredAgents.map(agent => (
          <div 
            key={agent.id} 
            style={{ 
              background: '#fff', 
              borderRadius: 12, 
              border: '1px solid #E5E5E5', 
              padding: 20,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12, marginBottom: 12 }}>
              <div 
                style={{ 
                  width: 48, 
                  height: 48, 
                  borderRadius: 12, 
                  background: agent.color + '20', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  fontSize: 24,
                }}
              >
                {agent.icon}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 2 }}>{agent.name}</div>
                <div style={{ fontSize: 12, color: '#6B7280' }}>v{agent.version} by {agent.creator}</div>
              </div>
              {agent.price === 0 ? (
                <span style={{ background: '#10B98120', color: '#10B981', padding: '4px 8px', borderRadius: 6, fontSize: 11, fontWeight: 500 }}>
                  Free
                </span>
              ) : (
                <span style={{ background: '#F59E0B20', color: '#F59E0B', padding: '4px 8px', borderRadius: 6, fontSize: 11, fontWeight: 500 }}>
                  ${agent.price}/mo
                </span>
              )}
            </div>

            <p style={{ fontSize: 13, color: '#6B7280', marginBottom: 12, lineHeight: 1.5 }}>
              {agent.description}
            </p>

            <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
              {agent.tags.map(tag => (
                <span key={tag} style={{ background: '#F4F4F4', padding: '2px 8px', borderRadius: 4, fontSize: 10, color: '#6B7280' }}>
                  {tag}
                </span>
              ))}
            </div>

            {/* Tech Stack */}
            <div style={{ background: '#F8F9FA', padding: 10, borderRadius: 6, marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#6B7280', marginBottom: 4 }}>TECHNICAL</div>
              <div style={{ fontSize: 11, display: 'flex', gap: 12 }}>
                <span style={{ fontFamily: 'monospace' }}>{agent.runtime}</span>
                <span style={{ fontFamily: 'monospace' }}>{agent.model}</span>
                <span style={{ fontFamily: 'monospace' }}>{agent.context.toLocaleString()}k</span>
              </div>
            </div>

            {/* Capabilities */}
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 10, color: '#6B7280', marginBottom: 6 }}>CAPABILITIES</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 4 }}>
                {agent.capabilities.map(cap => (
                  <div key={cap.name} style={{ fontSize: 10, color: cap.enabled ? '#10B981' : '#DA1E28' }}>
                    {cap.enabled ? '✓' : '✗'} {cap.name.replace('_', ' ')}
                  </div>
                ))}
              </div>
            </div>

            {/* Stats */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: 12, borderTop: '1px solid #F4F4F4' }}>
              <div style={{ display: 'flex', gap: 12, fontSize: 11, color: '#6B7280' }}>
                <span>⬇ {agent.downloads.toLocaleString()}</span>
                <span>⭐ {agent.rating}</span>
              </div>
              <div style={{ fontSize: 10, color: '#6B7280' }}>
                Updated {agent.updated}
              </div>
            </div>

            <button style={{ width: '100%', marginTop: 12, background: '#667EEA', color: '#fff', border: 'none', padding: '10px 0', borderRadius: 8, fontSize: 13, cursor: 'pointer', fontWeight: 500 }}>
              Install Agent
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}