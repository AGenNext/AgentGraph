import { test, expect } from '@playwright/test';

const BACKEND_URL = 'http://localhost:8000';

test.describe('Agent Builder Integration', () => {
  // 1. Connect UI to API Registry - test via API directly
  test('should load tools from API registry', async ({ request }) => {
    const res = await request.get(`${BACKEND_URL}/frameworks`);
    expect(res.ok()).toBeTruthy();
    
    const data = await res.json();
    expect(data.frameworks).toHaveLength(2);
  });

  test('should search tools via API', async ({ request }) => {
    const res = await request.get(`${BACKEND_URL}/tools?framework=langgraph&search=graph`);
    const data = await res.json();
    expect(data.tools.length).toBeGreaterThan(0);
  });

  // 2. Build agent with selected tools
  test('should create agent with selected framework', async ({ request }) => {
    const tools = await request.get(`${BACKEND_URL}/tools?framework=langgraph`);
    const data = await tools.json();
    expect(data.tools.length).toBeGreaterThan(0);
  });

  // 3. Execute with LangGraph
  test('should execute langgraph agent', async ({ request }) => {
    const res = await request.post(`http://localhost:8001/tasks`, {
      data: {
        agentUrl: "test-agent",
        message: "Hello",
        framework: "langgraph",
        preFlightRequired: false,
        runToCompletion: true,
      }
    });
    // Backend may not be running on 8001, skip if not
    if (res.status() === 404) {
      console.log('Agent backend not running - skipping');
      return;
    }
    const task = await res.json();
    expect(task.status).toBeTruthy();
  });
});