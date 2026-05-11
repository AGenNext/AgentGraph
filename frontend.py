"""
Agent Platform Frontend

Web frontend for the agent platform:
- HTML/CSS/JS components
- Dashboard UI
- API Explorer
- Agent Console

Reference:
- React-like Components
- Tailwind-like utilities
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


# =============================================================================
# HTML COMPONENTS
# =============================================================================

@dataclass
class Component:
    """Base component"""
    id: str = ""
    class_name: str = ""
    style: Dict[str, str] = field(default_factory=dict)
    
    def to_html(self) -> str:
        return ""


@dataclass
class Button(Component):
    """Button"""
    text: str = "Click"
    variant: str = "primary"  # primary, secondary, danger
    
    def to_html(self) -> str:
        return f'<button class="btn btn-{self.variant}">{self.text}</button>'


@dataclass
class Input(Component):
    """Input"""
    placeholder: str = ""
    value: str = ""
    type: str = "text"
    
    def to_html(self) -> str:
        return f'<input type="{self.type}" placeholder="{self.placeholder}" value="{self.value}" class="{self.class_name}">'


@dataclass
class Card(Component):
    """Card"""
    title: str = ""
    content: str = ""
    
    def to_html(self) -> str:
        return f'''
<div class="card {self.class_name}">
  <div class="card-header">{self.title}</div>
  <div class="card-body">{self.content}</div>
</div>'''


# =============================================================================
# DASHBOARD
# =============================================================================

class DashboardUI:
    """Dashboard UI"""
    
    def __init__(self, title: str = "Agent Platform"):
        self.title = title
        self.components: List[Component] = []
        self.sidebar_items: List[Dict] = []
        self.header_actions: List[Dict] = []
    
    def add_sidebar_item(self, label: str, icon: str = "", href: str = "#"):
        """Add sidebar item"""
        self.sidebar_items.append({"label": label, "icon": icon, "href": href})
    
    def add_header_action(self, label: str, handler: str = ""):
        """Add header action"""
        self.header_actions.append({"label": label, "handler": handler})
    
    def add_component(self, component: Component):
        """Add component"""
        self.components.append(component)
    
    def to_html(self) -> str:
        """Generate full HTML"""
        sidebar = "\n".join([
            f'<a href="{item["href"]}" class="sidebar-item">{item["label"]}</a>'
            for item in self.sidebar_items
        ])
        
        components = "\n".join([c.to_html() for c in self.components])
        
        actions = "\n".join([
            f'<button class="header-action" onclick="{a["handler"]}">{a["label"]}</button>'
            for a in self.header_actions
        ])
        
        return f'''<!DOCTYPE html>
<html>
<head>
  <title>{self.title}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .app {{ display: grid; grid-template-columns: 250px 1fr; grid-template-rows: 60px 1fr; height: 100vh; }}
    .header {{ grid-column: 1 / -1; background: #1a1a2e; color: white; padding: 0 20px; display: flex; align-items: center; justify-content: space-between; }}
    .sidebar {{ background: #16213e; color: white; padding: 20px 0; }}
    .sidebar-item {{ display: block; padding: 12px 20px; color: #a0a0a0; text-decoration: none; }}
    .sidebar-item:hover {{ background: #0f3460; color: white; }}
    .main {{ padding: 20px; background: #f5f5f5; overflow-y: auto; }}
    .card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    .btn {{ padding: 8px 16px; border-radius: 4px; border: none; cursor: pointer; }}
    .btn-primary {{ background: #0f3460; color: white; }}
    .btn-secondary {{ background: #e0e0e0; color: #333; }}
    input {{ padding: 8px; border: 1px solid #ddd; border-radius: 4px; width: 100%; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
  </style>
</head>
<body>
  <div class="app">
    <header class="header">
      <div class="logo">{self.title}</div>
      <div class="actions">{actions}</div>
    </header>
    <aside class="sidebar">{sidebar}</aside>
    <main class="main">{components}</main>
  </div>
</body>
</html>'''


# =============================================================================
# AGENT CONSOLE
# =============================================================================

class AgentConsole:
    """Agent console UI"""
    
    def __init__(self):
        self.agents: List[Dict] = []
        self.conversations: List[Dict] = []
        self.output: List[str] = []
    
    def add_agent(self, id: str, name: str, status: str = "idle"):
        """Add agent"""
        self.agents.append({"id": id, "name": name, "status": status})
    
    def add_message(self, role: str, content: str):
        """Add message"""
        self.conversations.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_output(self, text: str):
        """Add output"""
        self.output.append(text)
    
    def to_html(self) -> str:
        """Generate HTML"""
        agents_html = "\n".join([
            f'<div class="agent-item">{a["name"]} <span class="status">{a["status"]}</span></div>'
            for a in self.agents
        ])
        
        messages_html = "\n".join([
            f'<div class="message {m["role"]}">{m["content"]}</div>'
            for m in self.conversations
        ])
        
        return f'''<!DOCTYPE html>
<html>
<head>
  <title>Agent Console</title>
  <style>
    body {{ font-family: monospace; background: #1e1e1e; color: #d4d4d4; }}
    .console {{ display: grid; grid-template-columns: 200px 1fr 300px; height: 100vh; }}
    .sidebar {{ background: #252526; padding: 10px; }}
    .agent-item {{ padding: 8px; margin: 4px 0; background: #333; border-radius: 4px; }}
    .status {{ float: right; color: #4caf50; }}
    .chat {{ padding: 20px; overflow-y: auto; }}
    .message {{ margin: 8px 0; padding: 8px 12px; border-radius: 8px; max-width: 80%; }}
    .message.user {{ background: #0e639c; margin-left: auto; }}
    .message.assistant {{ background: #333; }}
    .output {{ background: #0c0c0c; padding: 20px; border-left: 1px solid #333; }}
    input {{ background: #333; color: white; border: none; padding: 10px; width: 100%; }}
  </style>
</head>
<body>
  <div class="console">
    <aside class="sidebar">
      <h3>Agents</h3>
      {agents_html}
    </aside>
    <main class="chat">
      {messages_html}
      <input placeholder="Type message...">
    </main>
    <aside class="output">
      <h3>Output</h3>
      <pre>{chr(10).join(self.output)}</pre>
    </aside>
  </div>
</body>
</html>'''


# =============================================================================
# API EXPLORER
# =============================================================================

class APIExplorer:
    """API Explorer UI"""
    
    def __init__(self):
        self.endpoints: List[Dict] = []
        self.selected: Optional[Dict] = None
    
    def add_endpoint(self, method: str, path: str, summary: str = ""):
        """Add endpoint"""
        self.endpoints.append({
            "method": method,
            "path": path,
            "summary": summary
        })
    
    def select(self, path: str):
        """Select endpoint"""
        for ep in self.endpoints:
            if ep["path"] == path:
                self.selected = ep
                break
    
    def to_html(self) -> str:
        """Generate HTML"""
        endpoints = "\n".join([
            f'<div class="endpoint"><span class="method {e["method"]}">{e["method"]}</span> {e["path"]}</div>'
            for e in self.endpoints
        ])
        
        details = ""
        if self.selected:
            details = f'''
<div class="details">
  <h3>{self.selected["path"]}</h3>
  <textarea></textarea>
  <button class="btn-primary">Execute</button>
</div>'''
        
        return f'''<!DOCTYPE html>
<html>
<head>
  <title>API Explorer</title>
  <style>
    body {{ font-family: monospace; background: #f5f5f5; }}
    .explorer {{ display: grid; grid-template-columns: 300px 1fr; height: 100vh; }}
    .endpoints {{ background: white; padding: 10px; overflow-y: auto; }}
    .endpoint {{ padding: 8px; border-bottom: 1px solid #eee; }}
    .method {{ display: inline-block; width: 60px; font-weight: bold; }}
    .method.GET {{ color: #61affe; }}
    .method.POST {{ color: #49cc90; }}
    .method.PUT {{ color: #fca130; }}
    .method.DELETE {{ color: #f93e3e; }}
    .details {{ padding: 20px; }}
    textarea {{ width: 100%; height: 200px; margin: 10px 0; font-family: monospace; }}
  </style>
</head>
<body>
  <div class="explorer">
    <aside class="endpoints">{endpoints}</aside>
    <main class="details">{details}</main>
  </div>
</body>
</html>'''


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Frontend UI")
    print("=" * 50)
    
    # Dashboard
    dashboard = DashboardUI("Agent Platform")
    dashboard.add_sidebar_item("Dashboard", "", "/")
    dashboard.add_sidebar_item("Agents", "", "/agents")
    dashboard.add_sidebar_item("Knowledge Graph", "", "/knowledge")
    dashboard.add_sidebar_item("Databases", "", "/databases")
    dashboard.add_sidebar_item("Monitoring", "", "/monitoring")
    dashboard.add_component(Card(title="Stats", content="Active Agents: 5"))
    dashboard.add_component(Card(title="Recent Activity", content="Task completed: 123"))
    
    print("\nDashboard HTML generated")
    print(f"  Sidebar items: {len(dashboard.sidebar_items)}")
    
    # Console
    console = AgentConsole()
    console.add_agent("agent-001", "Assistant")
    console.add_agent("agent-002", "Researcher")
    console.add_message("user", "Find information about AI")
    console.add_message("assistant", "Searching knowledge base...")
    
    print("\nConsole HTML generated")
    print(f"  Agents: {len(console.agents)}")
    print(f"  Messages: {len(console.conversations)}")
    
    # API Explorer
    explorer = APIExplorer()
    explorer.add_endpoint("GET", "/agents", "List agents")
    explorer.add_endpoint("POST", "/agents", "Create agent")
    explorer.add_endpoint("GET", "/tasks", "List tasks")
    
    print("\nAPI Explorer HTML generated")
    print(f"  Endpoints: {len(explorer.endpoints)}")


if __name__ == "__main__":
    main()


"""
Frontend Usage

    # Dashboard
    dashboard = DashboardUI("Agent Platform")
    dashboard.add_sidebar_item("Dashboard")
    dashboard.add_component(Card(title="Stats", content="Active: 5"))
    print(dashboard.to_html())
    
    # Console
    console = AgentConsole()
    console.add_agent("agent-001", "Assistant")
    console.add_message("user", "Hello")
    print(console.to_html())
    
    # API Explorer
    explorer = APIExplorer()
    explorer.add_endpoint("GET", "/users")
    print(explorer.to_html())
"""