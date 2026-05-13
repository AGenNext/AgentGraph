import { test, expect } from '@playwright/test';

const API = 'http://localhost:8000';

test.describe('AgentBuilder UI', () => {
  test('should load frameworks from API', async ({ request }) => {
    const res = await request.get(`${API}/frameworks`);
    const data = await res.json();
    
    expect(data.frameworks).toHaveLength(4);
    expect(data.frameworks.map((f: any) => f.id)).toContain('langgraph');
    expect(data.frameworks.map((f: any) => f.id)).toContain('langchain');
  });

  test('should load tools from API', async ({ request }) => {
    const res = await request.get(`${API}/tools`);
    const data = await res.json();
    
    expect(data.total).toBe(6);
  });

  test('should filter langgraph tools', async ({ request }) => {
    const res = await request.get(`${API}/tools?framework=langgraph`);
    const data = await res.json();
    
    expect(data.tools.length).toBe(2);
  });

  test('should filter langchain tools', async ({ request }) => {
    const res = await request.get(`${API}/tools?framework=langchain`);
    const data = await res.json();
    
    expect(data.tools.length).toBe(2);
  });

  test('should search tools by name', async ({ request }) => {
    const res = await request.get(`${API}/tools?search=state`);
    const data = await res.json();
    
    expect(data.tools.length).toBeGreaterThan(0);
    data.tools.forEach((t: any) => {
      expect(t.name.toLowerCase()).toContain('state');
    });
  });

  test('should get tool by id', async ({ request }) => {
    const res = await request.get(`${API}/tools/langgraph:1`);
    const data = await res.json();
    
    expect(data.tool.name).toBe('StateGraph');
  });
});