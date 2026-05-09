# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: agent-builder.spec.ts >> AgentBuilder UI >> should search tools by name
- Location: e2e/agent-builder.spec.ts:36:7

# Error details

```
SyntaxError: Unexpected token 'I', "Internal S"... is not valid JSON
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | const API = 'http://localhost:8000';
  4  | 
  5  | test.describe('AgentBuilder UI', () => {
  6  |   test('should load frameworks from API', async ({ request }) => {
  7  |     const res = await request.get(`${API}/frameworks`);
  8  |     const data = await res.json();
  9  |     
  10 |     expect(data.frameworks).toHaveLength(2);
  11 |     expect(data.frameworks.map((f: any) => f.name)).toContain('langgraph');
  12 |     expect(data.frameworks.map((f: any) => f.name)).toContain('langchain');
  13 |   });
  14 | 
  15 |   test('should load all 314 tools', async ({ request }) => {
  16 |     const res = await request.get(`${API}/tools`);
  17 |     const data = await res.json();
  18 |     
  19 |     expect(data.tools.length).toBe(314);
  20 |   });
  21 | 
  22 |   test('should filter langgraph tools', async ({ request }) => {
  23 |     const res = await request.get(`${API}/tools?framework=langgraph`);
  24 |     const data = await res.json();
  25 |     
  26 |     expect(data.tools.length).toBe(232);
  27 |   });
  28 | 
  29 |   test('should filter langchain tools', async ({ request }) => {
  30 |     const res = await request.get(`${API}/tools?framework=langchain`);
  31 |     const data = await res.json();
  32 |     
  33 |     expect(data.tools.length).toBe(82);
  34 |   });
  35 | 
  36 |   test('should search tools by name', async ({ request }) => {
  37 |     const res = await request.get(`${API}/tools?framework=langgraph&search=state`);
> 38 |     const data = await res.json();
     |                  ^ SyntaxError: Unexpected token 'I', "Internal S"... is not valid JSON
  39 |     
  40 |     expect(data.tools.length).toBeGreaterThan(0);
  41 |     data.tools.forEach((t: any) => {
  42 |       expect(t.name.toLowerCase()).toContain('state');
  43 |     });
  44 |   });
  45 | 
  46 |   test('should get tool by canonical_id', async ({ request }) => {
  47 |     const res = await request.get(`${API}/tools/langgraph:1.1.10:StateGraph`);
  48 |     const tool = await res.json();
  49 |     
  50 |     expect(tool.name).toBe('StateGraph');
  51 |     expect(tool.kind).toBe('class');
  52 |     expect(tool.framework).toBe('langgraph');
  53 |   });
  54 | });
```