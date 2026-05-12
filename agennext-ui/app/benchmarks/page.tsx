'use client';

import { useState } from 'react';

interface Benchmark {
  id: string;
  name: string;
  category: 'reasoning' | 'coding' | 'math' | 'language' | 'knowledge';
  description: string;
}

interface Score {
  model: string;
  scores: Record<string, number>;
  average: number;
}

const benchmarks: Benchmark[] = [
  { id: 'mmlu', name: 'MMLU', category: 'knowledge', description: 'Multi-task language understanding' },
  { id: 'humaneval', name: 'HumanEval', category: 'coding', description: 'Code generation' },
  { id: 'gpqa', name: 'GPQA', category: 'reasoning', description: 'Graduate-level science Q&A' },
  { id: 'math', name: 'MATH', category: 'math', description: 'Competition math problems' },
  { id: 'ifeval', name: 'IFEval', category: 'language', description: 'Instruction following' },
  { id: 'mmlu-pro', name: 'MMLU-Pro', category: 'knowledge', description: 'Advanced multi-task' },
];

const scores: Score[] = [
  { model: 'GPT-4o', scores: { mmlu: 87.2, humaneval: 92.0, gpqa: 75.2, math: 78.2, ifeval: 88.5, 'mmlu-pro': 84.1 }, average: 84.2 },
  { model: 'Claude Opus 4', scores: { mmlu: 86.8, humaneval: 84.0, gpqa: 73.1, math: 76.4, ifeval: 89.2, 'mmlu-pro': 82.5 }, average: 82.0 },
  { model: 'Claude Sonnet 4', scores: { mmlu: 85.1, humaneval: 81.5, gpqa: 70.8, math: 72.1, ifeval: 86.4, 'mmlu-pro': 80.2 }, average: 79.4 },
  { model: 'Gemini 1.5 Ultra', scores: { mmlu: 85.4, humaneval: 84.2, gpqa: 71.9, math: 75.8, ifeval: 87.1, 'mmlu-pro': 81.8 }, average: 81.0 },
  { model: 'Gemini 1.5 Pro', scores: { mmlu: 83.2, humaneval: 79.8, gpqa: 68.4, math: 70.2, ifeval: 84.5, 'mmlu-pro': 78.4 }, average: 77.4 },
  { model: 'Claude 3.5 Sonnet', scores: { mmlu: 84.7, humaneval: 82.1, gpqa: 69.8, math: 71.5, ifeval: 85.2, 'mmlu-pro': 79.8 }, average: 78.9 },
  { model: 'Claude 3 Haiku', scores: { mmlu: 75.2, humaneval: 65.4, gpqa: 52.1, math: 55.8, ifeval: 78.4, 'mmlu-pro': 68.2 }, average: 65.9 },
  { model: 'Llama 3.1 405B', scores: { mmlu: 81.5, humaneval: 80.2, gpqa: 62.4, math: 68.5, ifeval: 82.1, 'mmlu-pro': 75.8 }, average: 75.1 },
  { model: 'Llama 3.1 70B', scores: { mmlu: 79.2, humaneval: 75.8, gpqa: 58.2, math: 62.4, ifeval: 79.5, 'mmlu-pro': 72.4 }, average: 71.3 },
  { model: 'GPT-4 Turbo', scores: { mmlu: 81.5, humaneval: 85.4, gpqa: 68.2, math: 72.1, ifeval: 82.5, 'mmlu-pro': 76.8 }, average: 79.4 },
  { model: 'GPT-3.5 Turbo', scores: { mmlu: 68.2, humaneval: 55.4, gpqa: 42.1, math: 48.5, ifeval: 72.1, 'mmlu-pro': 58.2 }, average: 57.4 },
  { model: 'DeepSeek Chat', scores: { mmlu: 75.8, humaneval: 72.1, gpqa: 55.2, math: 60.4, ifeval: 78.2, 'mmlu-pro': 68.5 }, average: 68.4 },
  { model: 'Command R+', scores: { mmlu: 72.4, humaneval: 68.5, gpqa: 48.2, math: 52.1, ifeval: 74.5, 'mmlu-pro': 64.2 }, average: 63.3 },
  { model: 'Grok-2', scores: { mmlu: 78.5, humaneval: 75.2, gpqa: 60.1, math: 65.8, ifeval: 80.2, 'mmlu-pro': 72.1 }, average: 72.0 },
  { model: 'Mistral Large', scores: { mmlu: 80.2, humaneval: 78.4, gpqa: 58.5, math: 64.2, ifeval: 82.1, 'mmlu-pro': 74.5 }, average: 73.0 },
];

const categoryColors = {
  reasoning: '#667EEA',
  coding: '#10B981',
  math: '#F59E0B',
  language: '#DA1E28',
  knowledge: '#0F62FE',
};

export default function BenchmarksPage() {
  const [category, setCategory] = useState<string>('all');
  const [metric, setMetric] = useState<'rank' | 'mmlu' | 'humaneval' | 'math'>('rank');
  
  const sortedScores = [...scores].sort((a, b) => {
    if (metric === 'rank') return b.average - a.average;
    return b.scores[metric] - a.scores[metric];
  });

  return (
    <div style={{ padding: 24, fontFamily: 'IBM Plex Sans, sans-serif', background: '#F8F9FA', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 600, margin: 0 }}>LLM Benchmarks</h1>
          <p style={{ color: '#6B7280', margin: '4px 0 0 0', fontSize: 14 }}>Model evaluation & leaderboard</p>
        </div>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
        <select 
          value={category}
          onChange={e => setCategory(e.target.value)}
          style={{ padding: '10px 14px', borderRadius: 8, border: '1px solid #E5E5E5', background: '#fff' }}
        >
          <option value="all">All Categories</option>
          <option value="reasoning">Reasoning</option>
          <option value="coding">Coding</option>
          <option value="math">Math</option>
          <option value="language">Language</option>
          <option value="knowledge">Knowledge</option>
        </select>
        
        <select 
          value={metric}
          onChange={e => setMetric(e.target.value as typeof metric)}
          style={{ padding: '10px 14px', borderRadius: 8, border: '1px solid #E5E5E5', background: '#fff' }}
        >
          <option value="rank">Overall Rank</option>
          <option value="mmlu">MMLU</option>
          <option value="humaneval">HumanEval</option>
          <option value="math">Math</option>
        </select>
      </div>

      {/* Categories */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 12, marginBottom: 24 }}>
        {benchmarks.map(b => (
          <div 
            key={b.id} 
            style={{ 
              background: '#fff', 
              padding: 16, 
              borderRadius: 8, 
              border: '1px solid #E5E5E5',
              borderLeft: `4px solid ${categoryColors[b.category as keyof typeof categoryColors]}`,
            }}
          >
            <div style={{ fontSize: 14, fontWeight: 600 }}>{b.name}</div>
            <div style={{ fontSize: 11, color: '#6B7280' }}>{b.category}</div>
          </div>
        ))}
      </div>

      {/* Leaderboard */}
      <div style={{ background: '#fff', borderRadius: 8, border: '1px solid #E5E5E5', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#F8F9FA' }}>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>RANK</th>
              <th style={{ padding: '12px 16px', textAlign: 'left', fontSize: 11, color: '#6B7280' }}>MODEL</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>AVERAGE</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>MMLU</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>HUMANEVAL</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>GPQA</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>MATH</th>
              <th style={{ padding: '12px 16px', textAlign: 'center', fontSize: 11, color: '#6B7280' }}>IFEVAL</th>
            </tr>
          </thead>
          <tbody>
            {sortedScores.map((s, i) => (
              <tr key={s.model} style={{ borderTop: '1px solid #F4F4F4', 
                background: i < 3 ? '#667EEA08' : 'transparent' 
              }}>
                <td style={{ padding: '14px 16px', fontWeight: 600, color: i < 3 ? '#667EEA' : '#6B7280' }}>
                  {i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${i + 1}`}
                </td>
                <td style={{ padding: '14px 16px', fontWeight: 500 }}>{s.model}</td>
                <td style={{ padding: '14px 16px', textAlign: 'center', fontWeight: 600, color: '#667EEA' }}>{s.average.toFixed(1)}</td>
                <td style={{ padding: '14px 16px', textAlign: 'center', fontSize: 12 }}>{s.scores.mmlu?.toFixed(1)}</td>
                <td style={{ padding: '14px 16px', textAlign: 'center', fontSize: 12 }}>{s.scores.humaneval?.toFixed(1)}</td>
                <td style={{ padding: '14px 16px', textAlign: 'center', fontSize: 12 }}>{s.scores.gpqa?.toFixed(1)}</td>
                <td style={{ padding: '14px 16px', textAlign: 'center', fontSize: 12 }}>{s.scores.math?.toFixed(1)}</td>
                <td style={{ padding: '14px 16px', textAlign: 'center', fontSize: 12 }}>{s.scores.ifeval?.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}