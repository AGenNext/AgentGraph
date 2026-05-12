import { test, expect } from '@playwright/test';

test.describe('API Registry Integration', () => {
  const API_URL = 'http://localhost:8000';

  test('should list frameworks from API', async ({ request }) => {
    const res = await request.get(`${API_URL}/frameworks`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.frameworks).toHaveLength(2);
    expect(data.frameworks[0].name).toBe('langgraph');
    expect(data.frameworks[1].name).toBe('langchain');
  });

  test('should list tools with framework filter', async ({ request }) => {
    const res = await request.get(`${API_URL}/tools?framework=langgraph`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.tools.length).toBeGreaterThan(0);
    expect(data.tools[0].framework).toBe('langgraph');
  });

  test('should search tools by name', async ({ request }) => {
    const res = await request.get(`${API_URL}/tools?framework=langgraph&search=state`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.tools.length).toBeGreaterThan(0);
    data.tools.forEach((t: any) => {
      expect(t.name.toLowerCase()).toContain('state');
    });
  });

  test('should get tool by canonical_id', async ({ request }) => {
    const res = await request.get(`${API_URL}/tools/langgraph:1.1.10:StateGraph`);
    expect(res.ok()).toBeTruthy();
    
    const tool = await res.json();
    expect(tool.name).toBe('StateGraph');
    expect(tool.kind).toBe('class');
  });
});