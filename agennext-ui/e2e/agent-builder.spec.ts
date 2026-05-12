import { test, expect } from '@playwright/test';

const API = 'http://localhost:8000';

test.describe('AgentBuilder UI', () => {
  test('should load frameworks from API', async ({ request }) => {
    const res = await request.get(`${API}/frameworks`);
    const data = await res.json();
    
    expect(data.frameworks).toHaveLength(2);
    expect(data.frameworks.map((f: any) => f.name)).toContain('langgraph');
    expect(data.frameworks.map((f: any) => f.name)).toContain('langchain');
  });

  test('should load all 314 tools', async ({ request }) => {
    const res = await request.get(`${API}/tools`);
    const data = await res.json();
    
    expect(data.tools.length).toBe(314);
  });

  test('should filter langgraph tools', async ({ request }) => {
    const res = await request.get(`${API}/tools?framework=langgraph`);
    const data = await res.json();
    
    expect(data.tools.length).toBe(232);
  });

  test('should filter langchain tools', async ({ request }) => {
    const res = await request.get(`${API}/tools?framework=langchain`);
    const data = await res.json();
    
    expect(data.tools.length).toBe(82);
  });

  test('should search tools by name', async ({ request }) => {
    const res = await request.get(`${API}/tools?framework=langgraph&search=state`);
    const data = await res.json();
    
    expect(data.tools.length).toBeGreaterThan(0);
    data.tools.forEach((t: any) => {
      expect(t.name.toLowerCase()).toContain('state');
    });
  });

  test('should get tool by canonical_id', async ({ request }) => {
    const res = await request.get(`${API}/tools/langgraph:1.1.10:StateGraph`);
    const tool = await res.json();
    
    expect(tool.name).toBe('StateGraph');
    expect(tool.kind).toBe('class');
    expect(tool.framework).toBe('langgraph');
  });
});