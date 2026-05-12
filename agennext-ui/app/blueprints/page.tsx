'use client';

import { useState } from 'react';

interface Blueprint {
  id: string;
  name: string;
  provider: string;
  description: string;
  icon: string;
  category: string;
  tier: 'starter' | 'professional' | 'enterprise';
  features: string[];
  pricing?: string;
  code?: string;
  popularity: number;
  trending: boolean;
}

const blueprints: Blueprint[] = [
  {
    id: 'lc1',
    name: 'LangChain Deep Research',
    provider: 'LangChain AI',
    description: 'Advanced research agent with Tavily search, reflection, and human feedback loops for enterprise-grade research',
    icon: '🔗',
    category: 'Research',
    tier: 'professional',
    features: ['Deep Research', 'Tavily Search', 'Reflection', 'Human Feedback', 'Multi-step'],
    pricing: 'Free',
    popularity: 94,
    trending: true,
  },
  {
    id: 'sf1',
    name: 'Salesforce Service Agent',
    provider: 'Salesforce',
    description: 'Enterprise customer service agent with full CRM integration, case management, and knowledge base',
    icon: '☁️',
    category: 'CRM',
    tier: 'enterprise',
    features: ['Service Cloud', 'Case Management', 'Knowledge Base', 'Live Agent', 'Email'],
    pricing: '$2,500/mo',
    popularity: 98,
    trending: true,
  },
  {
    id: 'ggl1',
    name: 'Google Workspace Agent',
    provider: 'Google Cloud',
    description: 'Unified productivity agent with Gmail, Calendar, Drive, Meet, and enterprise search',
    icon: '📧',
    category: 'Productivity',
    tier: 'enterprise',
    features: ['Gmail', 'Calendar', 'Drive', 'Meet', 'Search'],
    pricing: '$1,800/mo',
    popularity: 96,
    trending: false,
  },
  {
    id: 'aws1',
    name: 'AWS Bedrock Guardrail',
    provider: 'AWS',
    description: 'Production Bedrock agent with content safety, guardrails, and enterprise security controls',
    icon: '🛡️',
    category: 'Security',
    tier: 'enterprise',
    features: ['Content Filter', 'PII Redaction', 'Topic Control', 'Guardrails', 'Audit'],
    pricing: '$3,000/mo',
    popularity: 92,
    trending: false,
  },
  {
    id: 'az1',
    name: 'Azure AI Foundry',
    provider: 'Microsoft',
    description: 'Multi-agent orchestration with MCP/A2A protocols, Entra ID, and enterprise governance',
    icon: '🏭',
    category: 'Orchestration',
    tier: 'enterprise',
    features: ['MCP Protocol', 'A2A Protocol', 'Entra ID', 'Governance', 'Semantic Kernel'],
    pricing: '$2,800/mo',
    popularity: 95,
    trending: true,
  },
  {
    id: 'op1',
    name: 'OpenAI Responses Agent',
    provider: 'OpenAI',
    description: 'Modern agent with computer use, file search, web search, and function calling',
    icon: '⚡',
    category: 'AI',
    tier: 'professional',
    features: ['Computer Use', 'File Search', 'Web Search', 'Vision', 'Functions'],
    pricing: '$500/mo',
    popularity: 99,
    trending: true,
  },
  {
    id: 'an1',
    name: 'Anthropic Computer Use',
    provider: 'Anthropic',
    description: 'Claude automation with computer use, bash, browser, and screenshot analysis',
    icon: '💻',
    category: 'Automation',
    tier: 'professional',
    features: ['Computer Use', 'Bash', 'Browser', 'Screenshots', 'Vision'],
    pricing: '$600/mo',
    popularity: 91,
    trending: false,
  },
  {
    id: 'cr1',
    name: 'CrewAI Enterprise',
    provider: 'CrewAI',
    description: 'Multi-agent orchestration with sequential, hierarchical, and parallel processes',
    icon: '👥',
    category: 'Orchestration',
    tier: 'professional',
    features: ['Sequential', 'Hierarchical', 'Custom Tools', 'Memory', 'Tasks'],
    pricing: 'Free',
    popularity: 88,
    trending: false,
  },
  {
    id: 'ms1',
    name: 'Copilot Studio',
    provider: 'Microsoft',
    description: 'Enterprise copilot with M365, Power Automate, Teams, and SharePoint integration',
    icon: '📎',
    category: 'Enterprise',
    tier: 'enterprise',
    features: ['M365', 'Power Automate', 'Teams', 'SharePoint', 'Dataverse'],
    pricing: '$1,200/mo',
    popularity: 93,
    trending: false,
  },
  {
    id: 'v1',
    name: 'Vertex AI Agent Builder',
    provider: 'Google Cloud',
    description: 'Enterprise agent with Gemini, Vertex Search, grounding, and knowledge engine',
    icon: '☁️',
    category: 'Enterprise',
    tier: 'enterprise',
    features: ['Gemini', 'Vertex Search', 'Grounding', 'Knowledge', 'AutoML'],
    pricing: '$2,500/mo',
    popularity: 90,
    trending: false,
  },
  {
    id: 'dt1',
    name: 'Dify Enterprise',
    provider: 'Dify',
    description: 'Open-source LLM app framework with visual workflow, agent builder, and RAG pipeline',
    icon: '🔧',
    category: 'Platform',
    tier: 'starter',
    features: ['Visual Workflow', 'Agent Builder', 'RAG', 'API Gateway', 'Observability'],
    pricing: 'Free',
    popularity: 85,
    trending: true,
  },
  {
    id: 'lm1',
    name: 'LlamaIndex Agent',
    provider: 'LlamaIndex',
    description: 'Data-augmented agent with advanced RAG, query engines, and 100+ data connectors',
    icon: '📚',
    category: 'Data',
    tier: 'professional',
    features: ['Advanced RAG', 'Query Engines', '100+ Connectors', 'Sub-question', 'Parsing'],
    pricing: 'Free',
    popularity: 89,
    trending: false,
  },
];

const categories = [...new Set(blueprints.map(bp => bp.category))];
const providers = [...new Set(blueprints.map(bp => bp.provider))];

const colors = {
  background: '#050507',
  surface: '#0E0E12',
  surfaceElevated: '#16161D',
  border: '#232329',
  borderHover: '#2E2E3A',
  primary: '#6366F1',
  primaryLight: '#818CF8',
  primaryDark: '#4F46E5',
  accent: '#22D3EE',
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  text: '#F4F4F5',
  textSecondary: '#A1A1AA',
  textMuted: '#71717A',
};

export default function BlueprintsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedProvider, setSelectedProvider] = useState<string>('all');
  const [selectedBlueprint, setSelectedBlueprint] = useState<Blueprint | null>(null);
  
  const filtered = blueprints.filter(bp => {
    if (selectedCategory !== 'all' && bp.category !== selectedCategory) return false;
    if (selectedProvider !== 'all' && bp.provider !== selectedProvider) return false;
    return true;
  });

  return (
    <div style={{ 
      padding: 32, 
      fontFamily: "'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
      background: colors.background, 
      minHeight: '100vh',
      color: colors.text,
    }}>
      {/* Hero Header */}
      <div style={{ 
        background: `linear-gradient(135deg, ${colors.primary}15 0%, ${colors.accent}10 100%)`, 
        borderRadius: 24, 
        padding: 40, 
        marginBottom: 40,
        border: `1px solid ${colors.border}`,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
          <div style={{ 
            width: 72, 
            height: 72, 
            borderRadius: 20, 
            background: `linear-gradient(135deg, ${colors.primary}, ${colors.primaryDark})`,
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            boxShadow: `0 8px 32px ${colors.primary}40`,
          }}>
            <span style={{ fontSize: 36 }}>⚡</span>
          </div>
          <div>
            <h1 style={{ fontSize: 36, fontWeight: 700, margin: 0, letterSpacing: '-0.02em' }}>Agent Blueprints</h1>
            <p style={{ color: colors.textSecondary, margin: '8px 0 0 0', fontSize: 16 }}>Enterprise-grade agent templates from the world's leading AI providers</p>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 40 }}>
        {[
          { label: 'Total Blueprints', value: blueprints.length, icon: '📦' },
          { label: 'Providers', value: providers.length, icon: '🏢' },
          { label: 'Categories', value: categories.length, icon: '🏷️' },
          { label: 'Enterprise Ready', value: blueprints.filter(b => b.tier === 'enterprise').length, icon: '🏆' },
        ].map(stat => (
          <div key={stat.label} style={{ 
            background: colors.surface, 
            borderRadius: 16, 
            padding: 24, 
            border: `1px solid ${colors.border}`,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
              <span style={{ fontSize: 20 }}>{stat.icon}</span>
              <div style={{ fontSize: 32, fontWeight: 700, color: colors.primary }}>{stat.value}</div>
            </div>
            <div style={{ fontSize: 13, color: colors.textMuted }}>{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 32, marginBottom: 32 }}>
        <div>
          <div style={{ fontSize: 11, color: colors.textMuted, marginBottom: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Category</div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <button onClick={() => setSelectedCategory('all')} style={{
              background: selectedCategory === 'all' ? colors.primary : colors.surface,
              color: selectedCategory === 'all' ? '#fff' : colors.textSecondary,
              border: `1px solid ${selectedCategory === 'all' ? colors.primary : colors.border}`,
              padding: '10px 18px', borderRadius: 10, fontSize: 13, cursor: 'pointer',
            }}>All</button>
            {categories.map(cat => (
              <button key={cat} onClick={() => setSelectedCategory(cat)} style={{
                background: selectedCategory === cat ? colors.primary : colors.surface,
                color: selectedCategory === cat ? '#fff' : colors.textSecondary,
                border: `1px solid ${selectedCategory === cat ? colors.primary : colors.border}`,
                padding: '10px 18px', borderRadius: 10, fontSize: 13, cursor: 'pointer',
              }}>{cat}</button>
            ))}
          </div>
        </div>
        <div>
          <div style={{ fontSize: 11, color: colors.textMuted, marginBottom: 12, textTransform: 'uppercase', letterSpacing: 1 }}>Provider</div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <button onClick={() => setSelectedProvider('all')} style={{
              background: selectedProvider === 'all' ? colors.primary : colors.surface,
              color: selectedProvider === 'all' ? '#fff' : colors.textSecondary,
              border: `1px solid ${selectedProvider === 'all' ? colors.primary : colors.border}`,
              padding: '10px 18px', borderRadius: 10, fontSize: 13, cursor: 'pointer',
            }}>All</button>
            {providers.map(p => (
              <button key={p} onClick={() => setSelectedProvider(p)} style={{
                background: selectedProvider === p ? colors.primary : colors.surface,
                color: selectedProvider === p ? '#fff' : colors.textSecondary,
                border: `1px solid ${selectedProvider === p ? colors.primary : colors.border}`,
                padding: '10px 18px', borderRadius: 10, fontSize: 13, cursor: 'pointer',
              }}>{p}</button>
            ))}
          </div>
        </div>
      </div>

      {/* Blueprints Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }}>
        {filtered.map(bp => (
          <div key={bp.id} style={{
            background: colors.surface,
            borderRadius: 20,
            border: `1px solid ${colors.border}`,
            padding: 24,
            cursor: 'pointer',
            transition: 'all 0.25s ease',
          }}
            onClick={() => setSelectedBlueprint(bp)}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = colors.primary;
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = `0 20px 40px ${colors.primary}20`;
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = colors.border;
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                <div style={{ 
                  width: 52, 
                  height: 52, 
                  borderRadius: 14, 
                  background: `linear-gradient(135deg, ${colors.primary}20, ${colors.accent}10)`,
                  border: `1px solid ${colors.border}`,
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  fontSize: 26 
                }}>
                  {bp.icon}
                </div>
                <div>
                  <div style={{ fontSize: 17, fontWeight: 600, color: colors.text }}>{bp.name}</div>
                  <div style={{ fontSize: 12, color: colors.primary, marginTop: 2 }}>{bp.provider}</div>
                </div>
              </div>
              {bp.trending && (
                <span style={{ 
                  background: `${colors.warning}20`, 
                  color: colors.warning,
                  padding: '4px 10px', 
                  borderRadius: 6, 
                  fontSize: 10, 
                  fontWeight: 600,
                }}>
                  TRENDING
                </span>
              )}
            </div>
            
            <p style={{ fontSize: 13, color: colors.textSecondary, marginBottom: 16, lineHeight: 1.6, minHeight: 52 }}>
              {bp.description}
            </p>
            
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 16 }}>
              {bp.features.slice(0, 3).map(f => (
                <span key={f} style={{ 
                  background: colors.surfaceElevated, 
                  color: colors.textSecondary, 
                  padding: '6px 12px', 
                  borderRadius: 8, 
                  fontSize: 11 
                }}>
                  {f}
                </span>
              ))}
              {bp.features.length > 3 && (
                <span style={{ color: colors.primary, fontSize: 11, padding: '6px 0' }}>+{bp.features.length - 3}</span>
              )}
            </div>
            
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center', 
              paddingTop: 16, 
              borderTop: `1px solid ${colors.border}`,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ color: colors.warning, fontSize: 14 }}>★</span>
                <span style={{ color: colors.textSecondary, fontSize: 13 }}>{bp.popularity}%</span>
              </div>
              <div style={{ 
                fontSize: 15, 
                fontWeight: 600, 
                color: bp.tier === 'enterprise' ? colors.warning : bp.tier === 'professional' ? colors.primary : colors.success,
              }}>
                {bp.pricing}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Blueprint Detail Modal */}
      {selectedBlueprint && (
        <div style={{
          position: 'fixed', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0,
          background: 'rgba(0,0,0,0.85)',
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          zIndex: 1000,
          backdropFilter: 'blur(12px)',
        }}>
          <div style={{ 
            background: colors.surface, 
            borderRadius: 24, 
            padding: 36, 
            maxWidth: 680, 
            maxHeight: '90vh', 
            overflow: 'auto',
            border: `1px solid ${colors.border}`,
            boxShadow: `0 40px 80px ${colors.primary}20`,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
                <div style={{ 
                  width: 72, 
                  height: 72, 
                  borderRadius: 18, 
                  background: `linear-gradient(135deg, ${colors.primary}30, ${colors.accent}20)`,
                  border: `1px solid ${colors.border}`,
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  fontSize: 36 
                }}>
                  {selectedBlueprint.icon}
                </div>
                <div>
                  <h2 style={{ fontSize: 24, fontWeight: 700, margin: 0 }}>{selectedBlueprint.name}</h2>
                  <div style={{ fontSize: 14, color: colors.primary, marginTop: 4 }}>{selectedBlueprint.provider}</div>
                </div>
              </div>
              <button 
                onClick={() => setSelectedBlueprint(null)} 
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  fontSize: 28, 
                  color: colors.textMuted, 
                  cursor: 'pointer',
                  padding: 4,
                }}
              >
                ✕
              </button>
            </div>

            <span style={{ 
              background: selectedBlueprint.tier === 'enterprise' ? `${colors.warning}20` : selectedBlueprint.tier === 'professional' ? `${colors.primary}20` : `${colors.success}20`,
              color: selectedBlueprint.tier === 'enterprise' ? colors.warning : selectedBlueprint.tier === 'professional' ? colors.primary : colors.success,
              padding: '8px 16px', 
              borderRadius: 10, 
              fontSize: 12, 
              fontWeight: 600, 
              textTransform: 'uppercase',
              display: 'inline-block', 
              marginBottom: 20,
            }}>
              {selectedBlueprint.tier} Tier
            </span>

            <p style={{ fontSize: 15, color: colors.textSecondary, lineHeight: 1.7, marginBottom: 28 }}>
              {selectedBlueprint.description}
            </p>

            <div style={{ marginBottom: 28 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: colors.text, marginBottom: 14, textTransform: 'uppercase', letterSpacing: 1 }}>Capabilities</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
                {selectedBlueprint.features.map(f => (
                  <span key={f} style={{ 
                    background: `${colors.primary}15`, 
                    color: colors.primaryLight, 
                    padding: '10px 16px', 
                    borderRadius: 10, 
                    fontSize: 13,
                    border: `1px solid ${colors.primary}30`,
                  }}>
                    {f}
                  </span>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', gap: 14 }}>
              <button style={{ 
                flex: 1, 
                background: colors.primary, 
                color: '#fff', 
                border: 'none', 
                padding: '16px 28px', 
                borderRadius: 12, 
                fontSize: 15, 
                fontWeight: 600, 
                cursor: 'pointer',
                boxShadow: `0 8px 24px ${colors.primary}40`,
              }}>
                Deploy Blueprint
              </button>
              <button style={{ 
                background: colors.surfaceElevated, 
                color: colors.text, 
                border: `1px solid ${colors.border}`,
                padding: '16px 28px', 
                borderRadius: 12, 
                fontSize: 15, 
                cursor: 'pointer' 
              }}>
                View Docs
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}