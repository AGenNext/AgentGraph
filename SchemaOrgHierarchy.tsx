/**
 * Schema.org React xyflow Component
 * 
 * Visualize Schema.org type hierarchy with xyflow.
 * 
 * Install: npm install @xyflow/react
 * Reference: https://reactflow.dev
 */

import React, { useCallback, useMemo, useState } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Panel,
  Node,
  Edge,
  MarkerType,
  BackgroundVariant,
  Connection,
  NodeTypes,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

// ===== SCHEMA.ORG TYPE DATA =====

// Core types as nodes
const CORE_TYPES = [
  { id: 'Thing', label: 'Thing', type: 'input', color: '#E8F5E9' },
  { id: 'Action', label: 'Action', color: '#E3F2FD' },
  { id: 'CreativeWork', label: 'CreativeWork', color: '#FFF3E0' },
  { id: 'Event', label: 'Event', color: '#F3E5F5' },
  { id: 'Intangible', label: 'Intangible', color: '#E0F2F1' },
  { id: 'MedicalEntity', label: 'MedicalEntity', color: '#FFEBEE' },
  { id: 'Organization', label: 'Organization', color: '#E8EAF6' },
  { id: 'Person', label: 'Person', color: '#FCE4EC' },
  { id: 'Place', label: 'Place', color: '#FFF8E1' },
  { id: 'Product', label: 'Product', color: '#F1F8E9' },
  { id: 'StructuredValue', label: 'StructuredValue', color: '#ECEFF1' },
];

// Type hierarchy edges
const TYPE_EDGES = [
  { source: 'Thing', target: 'Action' },
  { source: 'Thing', target: 'CreativeWork' },
  { source: 'Thing', target: 'Event' },
  { source: 'Thing', target: 'Intangible' },
  { source: 'Thing', target: 'MedicalEntity' },
  { source: 'Thing', target: 'Organization' },
  { source: 'Thing', target: 'Person' },
  { source: 'Thing', target: 'Place' },
  { source: 'Thing', target: 'Product' },
  { source: 'Thing', target: 'StructuredValue' },
  
  // Action hierarchy
  { source: 'Action', target: 'AchieveAction' },
  { source: 'Action', target: 'AssessAction' },
  { source: 'Action', target: 'ConsumeAction' },
  { source: 'Action', target: 'ControlAction' },
  
  // CreativeWork hierarchy
  { source: 'CreativeWork', target: 'Book' },
  { source: 'CreativeWork', target: 'Movie' },
  { source: 'CreativeWork', target: 'SoftwareApplication' },
  { source: 'CreativeWork', target: 'WebPage' },
  
  // Organization hierarchy  
  { source: 'Organization', target: 'Corporation' },
  { source: 'Organization', target: 'LocalBusiness' },
  { source: 'Organization', target: 'GovernmentOrganization' },
];

// Sub-types
const SUB_TYPES = [
  // Action sub-types
  { id: 'AchieveAction', label: 'AchieveAction', color: '#E3F2FD' },
  { id: 'AssessAction', label: 'AssessAction', color: '#E3F2FD' },
  { id: 'ConsumeAction', label: 'ConsumeAction', color: '#E3F2FD' },
  { id: 'ControlAction', label: 'ControlAction', color: '#E3F2FD' },
  
  // CreativeWork sub-types
  { id: 'Book', label: 'Book', color: '#FFF3E0' },
  { id: 'Movie', label: 'Movie', color: '#FFF3E0' },
  { id: 'SoftwareApplication', label: 'SoftwareApplication', color: '#FFF3E0' },
  { id: 'WebPage', label: 'WebPage', color: '#FFF3E0' },
  
  // Organization sub-types
  { id: 'Corporation', label: 'Corporation', color: '#E8EAF6' },
  { id: 'LocalBusiness', label: 'LocalBusiness', color: '#E8EAF6' },
  { id: 'GovernmentOrganization', label: 'GovernmentOrganization', color: '#E8EAF6' },
];

// ===== NODE COMPONENT =====

/** Schema.org Type Node */
const SchemaTypeNode = ({ data }: { data: { label: string; color: string; count?: number } }) => {
  return (
    <div
      style={{
        padding: '12px 20px',
        borderRadius: '8px',
        background: data.color || '#fff',
        border: '2px solid #333',
        minWidth: '140px',
        textAlign: 'center',
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
      }}
    >
      <div style={{ fontWeight: 'bold', fontSize: '14px' }}>{data.label}</div>
      {data.count !== undefined && (
        <div style={{ fontSize: '11px', color: '#666', marginTop: '4px' }}>
          {data.count} properties
        </div>
      )}
    </div>
  );
};

// Register custom node
const nodeTypes: NodeTypes = {
  schemaType: SchemaTypeNode,
};

// ===== INITIAL DATA =====

const getInitialNodes = (): Node[] => {
  const nodes: Node[] = [];
  
  // Core types (root)
  CORE_TYPES.forEach((type, i) => {
    nodes.push({
      id: type.id,
      type: 'schemaType',
      position: { x: 250, y: i * 80 },
      data: { label: type.label, color: type.color },
    });
  });
  
  // Sub-types
  SUB_TYPES.forEach((type, i) => {
    nodes.push({
      id: type.id,
      type: 'schemaType',
      position: { x: 550, y: i * 60 },
      data: { label: type.label, color: type.color },
    });
  });
  
  return nodes;
};

const getInitialEdges = (): Edge[] => {
  return TYPE_EDGES.map((edge, i) => ({
    id: `e${i}`,
    source: edge.source,
    target: edge.target,
    type: 'smoothstep',
    animated: true,
    style: { stroke: '#666', strokeWidth: 2 },
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: '#666',
    },
  })));
};

// ===== MAIN COMPONENT =====

/** Schema.org Hierarchy Visualizer */
export default function SchemaOrgHierarchy() {
  const [nodes, setNodes, onNodesChange] = useNodesState(getInitialNodes());
  const [edges, setEdges, onEdgesChange] = useEdgesState(getInitialEdges());
  const [showMinimap, setShowMinimap] = useState(true);

  const onConnect = useCallback(
    (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    console.log('Clicked node:', node.data);
    alert(`Schema.org Type: ${node.data.label}`);
  }, []);

  // Layout options
  const proOptions = { hideAttribution: true };

  return (
    <div style={{ width: '100%', height: '800px', border: '1px solid #ddd' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        proOptions={proOptions}
        fitView
        attributionPosition="bottom-left"
      >
        <Controls />
        {showMinimap && (
          <MiniMap
            nodeColor={(node) => (node.data as { color: string }).color || '#fff'}
            maskColor="rgba(0,0,0,0.1)"
          />
        )}
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
        
        <Panel position="top-left">
          <div style={{ padding: '12px', background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.15)' }}>
            <h3 style={{ margin: '0 0 8px 0' }}>Schema.org V30.0</h3>
            <p style={{ margin: 0, fontSize: '12px', color: '#666' }}>
              11 Core Types → 100+ Sub-types
            </p>
          </div>
        </Panel>
        
        <Panel position="top-right">
          <button
            onClick={() => setShowMinimap(!showMinimap)}
            style={{ padding: '8px 12px', cursor: 'pointer' }}
          >
            {showMinimap ? 'Hide' : 'Show'} Minimap
          </button>
        </Panel>
      </ReactFlow>
    </div>
  );
}

// ===== EXPORT FOR USE =====

export { SchemaTypeNode, getInitialNodes, getInitialEdges, CORE_TYPES, SUB_TYPES, TYPE_EDGES };

/*
Usage:
  1. Install: npm install @xyflow/react
  2. Import: import SchemaOrgHierarchy from './SchemaOrgHierarchy'
  3. Use: <SchemaOrgHierarchy />
  
References:
  - https://reactflow.dev
  - https://schema.org/docs/full.html
*/