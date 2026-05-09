// API Registry Client

const API_REGISTRY_URL = "http://localhost:8000";

export interface Tool {
  canonical_id: string;
  name: string;
  kind: "class" | "function";
  qualifiedName: string;
}

export interface Framework {
  name: string;
  version: string;
  tool_count: number;
}

export async function listFrameworks(): Promise<Framework[]> {
  const res = await fetch(`${API_REGISTRY_URL}/frameworks`);
  const data = await res.json();
  return data.frameworks;
}

export async function listTools(framework?: string, search?: string): Promise<Tool[]> {
  const params = new URLSearchParams();
  if (framework) params.set("framework", framework);
  if (search) params.set("search", search);
  
  const res = await fetch(`${API_REGISTRY_URL}/tools?${params}`);
  const data = await res.json();
  return data.tools;
}

export async function getTool(canonicalId: string): Promise<Tool | null> {
  const res = await fetch(`${API_REGISTRY_URL}/tools/${canonicalId}`);
  if (!res.ok) return null;
  return res.json();
}