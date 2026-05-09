'use client';

import { useCallback, useState, useEffect } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge,
  Connection,
  BackgroundVariant,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { listFrameworks, listTools, type Tool, type Framework } from '@/lib/api-registry';

const nodeStyles = {
  background: '#1E293B',
  border: '1px solid #3B82F6',
  borderRadius: 8,
  color: '#E2E8F0',
  padding: 12,
  fontSize: 12,
  fontFamily: 'JetBrains Mono, monospace',
};

export function AgentBuilder() {
  const [frameworks, setFrameworks] = useState<Framework[]>([]);
  const [selectedFramework, setSelectedFramework] = useState('langgraph');
  const [tools, setTools] = useState<Tool[]>([]);
  const [search, setSearch] = useState('');
  
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    listFrameworks().then(fws => {
      setFrameworks(fws);
      if (fws.length > 0) setSelectedFramework(fws[0].name);
    });
  }, []);

  useEffect(() => {
    listTools(selectedFramework, search || undefined).then(t => setTools(t));
  }, [selectedFramework, search]);

  const addToolNode = (tool: Tool) => {
    const newNode: Node = {
      id: tool.canonical_id,
      position: { x: Math.random() * 400 + 100, y: Math.random() * 300 + 100 },
      data: { label: tool.name },
      style: nodeStyles,
    };
    setNodes(nds => [...nds, newNode]);
  };

  const onConnect = useCallback(
    (params: Connection) => setEdges(edgs => addEdge(params, edgs)),
    [setEdges],
  );

  return (
    <div style={{ display: 'flex', height: '100%', gap: 16 }}>
      <div style={{ width: 280, background: '#0F172A', padding: 16, borderRadius: 8, overflow: 'auto' }}>
        <h3 style={{ color: '#E2E8F0', marginBottom: 12, fontSize: 14 }}>Tool Registry</h3>
        
        <select
          value={selectedFramework}
          onChange={e => setSelectedFramework(e.target.value)}
          style={{
            width: '100%', padding: 8, marginBottom: 12,
            background: '#1E293B', color: '#E2E8F0',
            border: '1px solid #334155', borderRadius: 6,
          }}
        >
          {frameworks.map(fw => (
            <option key={fw.name} value={fw.name}>
              {fw.name} (v{fw.version})
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Search tools..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{
            width: '100%', padding: 8, marginBottom: 12,
            background: '#1E293B', color: '#E2E8F0',
            border: '1px solid #334155', borderRadius: 6,
          }}
        />

        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {tools.slice(0, 50).map(tool => (
            <div
              key={tool.canonical_id}
              onClick={() => addToolNode(tool)}
              style={{
                padding: '8px 12px',
                background: '#1E293B',
                borderRadius: 4,
                cursor: 'pointer',
                fontSize: 11,
                color: '#94A3B8',
                fontFamily: 'JetBrains Mono, monospace',
              }}
            >
              {tool.name}
            </div>
          ))}
        </div>
      </div>

      <div style={{ flex: 1, background: '#0F172A', borderRadius: 8 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          style={{ background: '#0F172A' }}
        >
          <Controls style={{ background: '#1E293B', color: '#E2E8F0' }} />
          <MiniMap style={{ background: '#1E293B' }} />
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} color="#1E293B" />
        </ReactFlow>
      </div>
    </div>
  );
}