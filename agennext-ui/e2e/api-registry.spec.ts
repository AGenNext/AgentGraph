import { test, expect } from '@playwright/test';

test.describe('API Registry Integration', () => {
  const API_URL = 'http://localhost:8000';

  test('should list frameworks from API', async ({ request }) => {
    const res = await request.get(`${API_URL}/frameworks`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.frameworks).toHaveLength(4);
    expect(data.frameworks.map((f: any) => f.id)).toContain('langgraph');
    expect(data.frameworks.map((f: any) => f.id)).toContain('langchain');
  });

  test('should list tools with framework filter', async ({ request }) => {
    const res = await request.get(`${API_URL}/tools?framework=langgraph`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.tools.length).toBeGreaterThan(0);
    expect(data.tools[0].framework).toBe('langgraph');
  });

  test('should search tools by name', async ({ request }) => {
    const res = await request.get(`${API_URL}/tools?search=state`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.tools.length).toBeGreaterThan(0);
    data.tools.forEach((t: any) => {
      expect(t.name.toLowerCase()).toContain('state');
    });
  });

  test('should get tool by id', async ({ request }) => {
    const res = await request.get(`${API_URL}/tools/langgraph:1`);
    expect(res.ok()).toBeTruthy();
    
    const tool = await res.json();
    expect(tool.tool.name).toBe('StateGraph');
  });
});