# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: api-registry.spec.ts >> API Registry Integration >> should search tools by name
- Location: e2e/api-registry.spec.ts:25:7

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('API Registry Integration', () => {
  4  |   const API_URL = 'http://localhost:8000';
  5  | 
  6  |   test('should list frameworks from API', async ({ request }) => {
  7  |     const res = await request.get(`${API_URL}/frameworks`);
  8  |     expect(res.ok()).toBeTruthy();
  9  |     
  10 |     const data = await res.json();
  11 |     expect(data.frameworks).toHaveLength(2);
  12 |     expect(data.frameworks[0].name).toBe('langgraph');
  13 |     expect(data.frameworks[1].name).toBe('langchain');
  14 |   });
  15 | 
  16 |   test('should list tools with framework filter', async ({ request }) => {
  17 |     const res = await request.get(`${API_URL}/tools?framework=langgraph`);
  18 |     expect(res.ok()).toBeTruthy();
  19 |     
  20 |     const data = await res.json();
  21 |     expect(data.tools.length).toBeGreaterThan(0);
  22 |     expect(data.tools[0].framework).toBe('langgraph');
  23 |   });
  24 | 
  25 |   test('should search tools by name', async ({ request }) => {
  26 |     const res = await request.get(`${API_URL}/tools?framework=langgraph&search=state`);
> 27 |     expect(res.ok()).toBeTruthy();
     |                      ^ Error: expect(received).toBeTruthy()
  28 |     
  29 |     const data = await res.json();
  30 |     expect(data.tools.length).toBeGreaterThan(0);
  31 |     data.tools.forEach((t: any) => {
  32 |       expect(t.name.toLowerCase()).toContain('state');
  33 |     });
  34 |   });
  35 | 
  36 |   test('should get tool by canonical_id', async ({ request }) => {
  37 |     const res = await request.get(`${API_URL}/tools/langgraph:1.1.10:StateGraph`);
  38 |     expect(res.ok()).toBeTruthy();
  39 |     
  40 |     const tool = await res.json();
  41 |     expect(tool.name).toBe('StateGraph');
  42 |     expect(tool.kind).toBe('class');
  43 |   });
  44 | });
```