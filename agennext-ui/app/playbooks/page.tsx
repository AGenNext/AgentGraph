'use client';

import { useState } from 'react';

interface PlaybookStep {
  id: string;
  instruction: string;
  command?: string;
  optional?: boolean;
}

interface Playbook {
  id: string;
  name: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: string;
  steps: PlaybookStep[];
  tags: string[];
}

const playbooks: Playbook[] = [
  {
    id: 'pb1',
    name: 'Identity Assignment Workflow',
    description: 'Automate user identity assignment and role management with approval gates',
    category: 'IAM',
    difficulty: 'intermediate',
    duration: '15 min',
    tags: ['IAM', 'Automation'],
    steps: [
      { id: 's1', instruction: 'Get user identity from HR system', command: 'GET /api/users/{userId}', optional: false },
      { id: 's2', instruction: 'Check access certification status', command: 'GET /api/certifications/{userId}', optional: false },
      { id: 's3', instruction: 'Request manager approval', command: 'POST /api/approvals', optional: false },
      { id: 's4', instruction: 'Assign role in IdP', command: 'POST /api/roles/assign', optional: false },
      { id: 's5', instruction: 'Provision access', command: 'POST /api/access/provision', optional: false },
    ],
  },
  {
    id: 'pb2',
    name: 'Agent Lifecycle Management',
    description: 'Complete lifecycle workflow from creation to production deployment',
    category: 'MLOps',
    difficulty: 'advanced',
    duration: '30 min',
    tags: ['MLOps', 'Deployment'],
    steps: [
      { id: 's1', instruction: 'Create agent specification', command: 'POST /api/agents/spec', optional: false },
      { id: 's2', instruction: 'Run security scan', command: 'POST /api/security/scan', optional: false },
      { id: 's3', instruction: 'Quality assurance testing', command: 'POST /api/qa/test', optional: false },
      { id: 's4', instruction: 'Performance benchmark', command: 'POST /api/benchmarks/run', optional: false },
      { id: 's5', instruction: 'Staging deployment', command: 'POST /api/deploy/staging', optional: false },
      { id: 's6', instruction: 'Production deployment', command: 'POST /api/deploy/production', optional: true },
    ],
  },
  {
    id: 'pb3',
    name: 'Access Request & Approval',
    description: 'Request and approve resource access with multi-level authorization',
    category: 'Access',
    difficulty: 'beginner',
    duration: '10 min',
    tags: ['Access', 'Approval'],
    steps: [
      { id: 's1', instruction: 'Submit access request', command: 'POST /api/access/request', optional: false },
      { id: 's2', instruction: 'Manager review', command: 'GET /api/approvals/pending', optional: false },
      { id: 's3', instruction: 'Security review', command: 'GET /api/review/security', optional: true },
      { id: 's4', instruction: 'Grant access', command: 'POST /api/access/grant', optional: false },
    ],
  },
  {
    id: 'pb4',
    name: 'Access Review Cycle',
    description: 'Schedule and execute periodic access certifications',
    category: 'Compliance',
    difficulty: 'intermediate',
    duration: '20 min',
    tags: ['Compliance', 'Audit'],
    steps: [
      { id: 's1', instruction: 'Generate access report', command: 'POST /api/reports/access', optional: false },
      { id: 's2', instruction: 'Distribute reviews', command: 'POST /api/reviews/distribute', optional: false },
      { id: 's3', instruction: 'Collect responses', command: 'GET /api/reviews/status', optional: false },
      { id: 's4', instruction: 'Generate exception report', command: 'POST /api/reports/exceptions', optional: false },
      { id: 's5', instruction: 'Revoke non-compliant access', command: 'POST /api/access/revoke', optional: true },
    ],
  },
  {
    id: 'pb5',
    name: 'Security Incident Response',
    description: 'Respond to security incidents with automated containment',
    category: 'Security',
    difficulty: 'advanced',
    duration: '25 min',
    tags: ['Security', 'Incident'],
    steps: [
      { id: 's1', instruction: 'Detect anomaly', command: 'GET /api/detect/anomaly', optional: false },
      { id: 's2', instruction: 'Isolate affected resources', command: 'POST /api/security/isolate', optional: false },
      { id: 's3', instruction: 'Collect forensics', command: 'POST /api/security/forensics', optional: false },
      { id: 's4', instruction: 'Block malicious IPs', command: 'POST /api/firewall/block', optional: false },
      { id: 's5', instruction: 'Notify team', command: 'POST /api/notifications/alert', optional: false },
      { id: 's6', instruction: 'Create incident ticket', command: 'POST /api/tickets/create', optional: false },
    ],
  },
  {
    id: 'pb6',
    name: 'Model Cost Optimization',
    description: 'Automate cost optimization through smart routing and caching',
    category: 'Cost',
    difficulty: 'intermediate',
    duration: '15 min',
    tags: ['Cost', 'Optimization'],
    steps: [
      { id: 's1', instruction: 'Analyze usage patterns', command: 'GET /api/usage/patterns', optional: false },
      { id: 's2', instruction: 'Classify query complexity', command: 'POST /api/classify', optional: false },
      { id: 's3', instruction: 'Route to optimal model', command: 'POST /api/route', optional: false },
      { id: 's4', instruction: 'Check cache', command: 'GET /api/cache/check', optional: false },
      { id: 's5', instruction: 'Cache response', command: 'POST /api/cache/store', optional: true },
    ],
  },
  {
    id: 'pb7',
    name: 'Compliance Report Generation',
    description: 'Generate SOC2, HIPAA, or GDPR compliance reports',
    category: 'Compliance',
    difficulty: 'advanced',
    duration: '45 min',
    tags: ['Compliance', 'Audit'],
    steps: [
      { id: 's1', instruction: 'Gather evidence', command: 'GET /api/compliance/evidence', optional: false },
      { id: 's2', instruction: 'Run security controls', command: 'POST /api/security/controls', optional: false },
      { id: 's3', instruction: 'Generate audit trail', command: 'POST /api/audit/export', optional: false },
      { id: 's4', instruction: 'Risk assessment', command: 'POST /api/risk/assess', optional: false },
      { id: 's5', instruction: 'Generate compliance report', command: 'POST /api/reports/compliance', optional: false },
    ],
  },
  {
    id: 'pb8',
    name: 'Agent Deployment',
    description: 'Deploy new AI agent from registry to production',
    category: 'MLOps',
    difficulty: 'beginner',
    duration: '10 min',
    tags: ['Deployment', 'CI/CD'],
    steps: [
      { id: 's1', instruction: 'Pull agent from registry', command: 'docker pull agennext/agent:latest', optional: false },
      { id: 's2', instruction: 'Validate configuration', command: 'AGENNEXT validate --strict', optional: false },
      { id: 's3', instruction: 'Run tests', command: 'AGENNEXT test --coverage', optional: false },
      { id: 's4', instruction: 'Deploy to staging', command: 'AGENNEXT deploy staging', optional: false },
      { id: 's5', instruction: 'Deploy to production', command: 'AGENNEXT deploy prod', optional: true },
    ],
  },
];

const categories = [...new Set(playbooks.map(p => p.category))];
const difficultyColors = { beginner: '#10B981', intermediate: '#F59E0B', advanced: '#DA1E28' };

export default function PlaybooksPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedPlaybook, setSelectedPlaybook] = useState<Playbook | null>(null);
  
  const filteredPlaybooks = selectedCategory === 'all' 
    ? playbooks 
    : playbooks.filter(p => p.category === selectedCategory);

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>Playbooks</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Workflow automation & runbooks</p>
        </div>
        <button style={{ background: '#0F62FE', color: '#fff', border: 'none', padding: '10px 16px', borderRadius: 6, fontSize: 13, cursor: 'pointer' }}>
          + Create Playbook
        </button>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '1px solid #E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600 }}>{playbooks.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Total Playbooks</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#667EEA' }}>{categories.length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Categories</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#10B981' }}>{playbooks.filter(p => p.difficulty === 'beginner').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Beginner</div>
        </div>
        <div style={{ background: '#fff', padding: 20, borderRadius: 8, border: '#E5E5E5' }}>
          <div style={{ fontSize: 28, fontWeight: 600, color: '#DA1E28' }}>{playbooks.filter(p => p.difficulty === 'advanced').length}</div>
          <div style={{ fontSize: 12, color: '#6B7280' }}>Advanced</div>
        </div>
      </div>

      {/* Category Filter */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        <button
          onClick={() => setSelectedCategory('all')}
          style={{
            background: selectedCategory === 'all' ? '#1A1A2E' : '#fff',
            color: selectedCategory === 'all' ? '#fff' : '#525252',
            border: '1px solid #E5E5E5',
            padding: '8px 16px',
            borderRadius: 6,
            fontSize: 12,
            cursor: 'pointer',
          }}
        >
          All
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            style={{
              background: selectedCategory === cat ? '#1A1A2E' : '#fff',
              color: selectedCategory === cat ? '#fff' : '#525252',
              border: '1px solid #E5E5E5',
              padding: '8px 16px',
              borderRadius: 6,
              fontSize: 12,
              cursor: 'pointer',
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Playbooks Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
        {filteredPlaybooks.map(pb => (
          <div 
            key={pb.id} 
            style={{ 
              background: '#fff', 
              borderRadius: 12, 
              border: '1px solid #E5E5E5', 
              padding: 20,
              cursor: 'pointer',
            }}
            onClick={() => setSelectedPlaybook(pb)}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 12 }}>
              <div>
                <div style={{ fontSize: 16, fontWeight: 600, marginBottom: 4 }}>{pb.name}</div>
                <div style={{ fontSize: 12, color: '#6B7280' }}>{pb.description}</div>
              </div>
              <span style={{ 
                background: difficultyColors[pb.difficulty] + '20',
                color: difficultyColors[pb.difficulty],
                padding: '4px 8px',
                borderRadius: 4,
                fontSize: 10,
                textTransform: 'capitalize',
              }}>
                {pb.difficulty}
              </span>
            </div>
            <div style={{ display: 'flex', gap: 12, fontSize: 11, color: '#6B7280' }}>
              <span>⏱ {pb.duration}</span>
              <span>📋 {pb.steps.length} steps</span>
              <span>{pb.category}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Playbook Detail Modal */}
      {selectedPlaybook && (
        <div style={{ 
          position: 'fixed', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0, 
          background: 'rgba(0,0,0,0.5)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div style={{ background: '#fff', borderRadius: 12, padding: 24, maxWidth: 600, maxHeight: '80vh', overflow: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 20 }}>
              <h2 style={{ fontSize: 20, fontWeight: 600, margin: 0 }}>{selectedPlaybook.name}</h2>
              <button 
                onClick={() => setSelectedPlaybook(null)}
                style={{ background: 'none', border: 'none', fontSize: 20, cursor: 'pointer' }}
              >
                ✕
              </button>
            </div>
            <div style={{ fontSize: 13, color: '#6B7280', marginBottom: 20 }}>{selectedPlaybook.description}</div>
            
            <div style={{ marginBottom: 20 }}>
              <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 8 }}>Steps</div>
              {selectedPlaybook.steps.map((step, i) => (
                <div 
                  key={step.id} 
                  style={{ 
                    background: '#F8F9FA', 
                    padding: 12, 
                    borderRadius: 8, 
                    marginBottom: 8,
                    borderLeft: `3px solid ${step.optional ? '#F59E0B' : '#667EEA'}`,
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                    <span style={{ width: 20, height: 20, borderRadius: 10, background: '#667EEA', color: '#fff', fontSize: 11, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      {i + 1}
                    </span>
                    <span style={{ fontSize: 13, fontWeight: 500 }}>{step.instruction}</span>
                    {step.optional && <span style={{ fontSize: 10, color: '#F59E0B' }}>Optional</span>}
                  </div>
                  {step.command && (
                    <code style={{ fontSize: 11, fontFamily: 'monospace', background: '#1A1A2E', color: '#fff', padding: '4px 8px', borderRadius: 4 }}>
                      {step.command}
                    </code>
                  )}
                </div>
              ))}
            </div>

            <div style={{ display: 'flex', gap: 8 }}>
              {selectedPlaybook.tags.map(tag => (
                <span key={tag} style={{ background: '#F4F4F4', padding: '4px 10px', borderRadius: 6, fontSize: 11, color: '#6B7280' }}>
                  {tag}
                </span>
              ))}
            </div>

            <button style={{ width: '100%', marginTop: 20, background: '#667EEA', color: '#fff', border: 'none', padding: '12px 0', borderRadius: 8, fontSize: 14, cursor: 'pointer', fontWeight: 500 }}>
              ▶ Run Playbook
            </button>
          </div>
        </div>
      )}
    </div>
  );
}