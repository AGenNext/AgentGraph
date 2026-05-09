# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tools-panel.spec.ts >> Agent Builder Integration >> should create agent with selected framework
- Location: e2e/tools-panel.spec.ts:22:7

# Error details

```
SyntaxError: Unexpected token 'I', "Internal S"... is not valid JSON
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | const BACKEND_URL = 'http://localhost:8000';
  4  | 
  5  | test.describe('Agent Builder Integration', () => {
  6  |   // 1. Connect UI to API Registry - test via API directly
  7  |   test('should load tools from API registry', async ({ request }) => {
  8  |     const res = await request.get(`${BACKEND_URL}/frameworks`);
  9  |     expect(res.ok()).toBeTruthy();
  10 |     
  11 |     const data = await res.json();
  12 |     expect(data.frameworks).toHaveLength(2);
  13 |   });
  14 | 
  15 |   test('should search tools via API', async ({ request }) => {
  16 |     const res = await request.get(`${BACKEND_URL}/tools?framework=langgraph&search=graph`);
  17 |     const data = await res.json();
  18 |     expect(data.tools.length).toBeGreaterThan(0);
  19 |   });
  20 | 
  21 |   // 2. Build agent with selected tools
  22 |   test('should create agent with selected framework', async ({ request }) => {
  23 |     const tools = await request.get(`${BACKEND_URL}/tools?framework=langgraph`);
> 24 |     const data = await tools.json();
     |                  ^ SyntaxError: Unexpected token 'I', "Internal S"... is not valid JSON
  25 |     expect(data.tools.length).toBeGreaterThan(0);
  26 |   });
  27 | 
  28 |   // 3. Execute with LangGraph
  29 |   test('should execute langgraph agent', async ({ request }) => {
  30 |     const res = await request.post(`http://localhost:8001/tasks`, {
  31 |       data: {
  32 |         agentUrl: "test-agent",
  33 |         message: "Hello",
  34 |         framework: "langgraph",
  35 |         preFlightRequired: false,
  36 |         runToCompletion: true,
  37 |       }
  38 |     });
  39 |     // Backend may not be running on 8001, skip if not
  40 |     if (res.status() === 404) {
  41 |       console.log('Agent backend not running - skipping');
  42 |       return;
  43 |     }
  44 |     const task = await res.json();
  45 |     expect(task.status).toBeTruthy();
  46 |   });
  47 | });
```