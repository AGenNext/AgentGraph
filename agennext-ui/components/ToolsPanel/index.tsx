'use client';

import { useState, useEffect } from 'react';
import { listFrameworks, listTools, type Tool, type Framework } from '@/lib/api-registry';

export function ToolsPanel() {
  const [frameworks, setFrameworks] = useState<Framework[]>([]);
  const [selectedFramework, setSelectedFramework] = useState<string>('');
  const [search, setSearch] = useState('');
  const [tools, setTools] = useState<Tool[]>([]);
  const [selectedTools, setSelectedTools] = useState<Tool[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listFrameworks().then(fws => {
      setFrameworks(fws);
      if (fws.length > 0) setSelectedFramework(fws[0].name);
    });
  }, []);

  useEffect(() => {
    if (!selectedFramework) return;
    setLoading(true);
    listTools(selectedFramework, search || undefined).then(t => {
      setTools(t);
      setLoading(false);
    });
  }, [selectedFramework, search]);

  const toggleTool = (tool: Tool) => {
    if (selectedTools.find(t => t.canonical_id === tool.canonical_id)) {
      setSelectedTools(selectedTools.filter(t => t.canonical_id !== tool.canonical_id));
    } else {
      setSelectedTools([...selectedTools, tool]);
    }
  };

  return (
    <div className="tools-panel">
      <div className="framework-selector">
        <label>Framework:</label>
        <select 
          value={selectedFramework} 
          onChange={e => setSelectedFramework(e.target.value)}
        >
          {frameworks.map(fw => (
            <option key={fw.name} value={fw.name}>
              {fw.name} (v{ fw.version})
            </option>
          ))}
        </select>
      </div>

      <div className="search-box">
        <input
          type="text"
          placeholder="Search tools..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>

      <div className="tools-list">
        {loading ? (
          <div>Loading...</div>
        ) : (
          tools.map(tool => (
            <div 
              key={tool.canonical_id}
              className={`tool-item ${selectedTools.find(t => t.canonical_id === tool.canonical_id) ? 'selected' : ''}`}
              onClick={() => toggleTool(tool)}
            >
              <span className="tool-name">{tool.name}</span>
              <span className="tool-kind">{tool.kind}</span>
            </div>
          ))
        )}
      </div>

      <div className="selected-tools">
        <h3>Selected ({selectedTools.length})</h3>
        {selectedTools.map(tool => (
          <div key={tool.canonical_id} className="selected-tool">
            {tool.name}
          </div>
        ))}
      </div>
    </div>
  );
}