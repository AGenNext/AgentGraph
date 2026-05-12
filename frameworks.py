"""
Agent Platform Frameworks

Frameworks for running the agent platform:
- Web Framework (FastAPI-like)
- Agent Framework
- Database Framework (ORM-like)
- CLI Framework

Dependencies: All standard library
"""

from __future__ import annotationss
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable, Type
from datetime import datetime
from enum import Enum
import json
import re


# =============================================================================
# WEB FRAMEWORK
# =============================================================================

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Request:
    """HTTP Request"""
    method: str
    path: str
    query_params: Dict[str, str] = field(default_factory=dict)
    path_params: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    json: Dict = field(default_factory=dict)


@dataclass
class Response:
    """HTTP Response"""
    status: int = 200
    body: Any = None
    json: Dict = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "status": self.status,
            "body": self.body,
            "json": self.json,
            "headers": self.headers
        }


@dataclass
class Route:
    """Route"""
    path: str
    method: HTTPMethod
    handler: Callable
    
    summary: str = ""
    request_model: Optional[Type] = None
    response_model: Optional[Type] = None
    
    middleware: List[Callable] = field(default_factory=list)


class WebFramework:
    """Web Framework (FastAPI-like)"""
    
    def __init__(self, title: str = "API", version: str = "1.0.0"):
        self.title = title
        self.version = version
        
        self.routes: List[Route] = []
        
        self.middleware: List[Callable] = []
        
        self.exception_handlers: Dict[Type, Callable] = {}
    
    def get(self, path: str, **kwargs):
        return self._route(path, HTTPMethod.GET, **kwargs)
    
    def post(self, path: str, **kwargs):
        return self._route(path, HTTPMethod.POST, **kwargs)
    
    def put(self, path: str, **kwargs):
        return self._route(path, HTTPMethod.PUT, **kwargs)
    
    def delete(self, path: str, **kwargs):
        return self._route(path, HTTPMethod.DELETE, **kwargs)
    
    def _route(self, path: str, method: HTTPMethod, handler: Callable = None):
        """Decorator for routes"""
        def decorator(func: Callable):
            route = Route(
                path=path,
                method=method,
                handler=func,
                summary=func.__doc__ or ""
            )
            self.routes.append(route)
            return func
        return decorator(handler if handler else decorator)
    
    def add_middleware(self, middleware: Callable):
        self.middleware.append(middleware)
    
    def add_exception_handler(self, exc_type: Type, handler: Callable):
        self.exception_handlers[exc_type] = handler
    
    def _match_route(self, path: str, method: str) -> Optional[Route]:
        """Match route to path"""
        for route in self.routes:
            # Exact match
            if route.path == path and route.method.value == method:
                return route
            
            # Pattern match
            pattern = route.path.replace("{", "(?P<").replace("}", ">[^/]+)")
            match = re.match(f"^{pattern}$", path)
            if match:
                return route
        
        return None
    
    def handle(self, request: Request) -> Response:
        """Handle request"""
        route = self._match_route(request.path, request.method)
        
        if not route:
            return Response(status=404, json={"error": "Not Found"})
        
        # Apply middleware
        for mw in self.middleware:
            request = mw(request)
        
        # Call handler
        try:
            result = route.handler(request)
            return Response(status=200, json=result if isinstance(result, dict) else {"data": result})
        except Exception as e:
            exc_type = type(e)
            if exc_type in self.exception_handlers:
                return self.exception_handlers[exc_type](e)
            return Response(status=500, json={"error": str(e)})
    
    def openapi(self) -> Dict:
        """Generate OpenAPI spec"""
        paths = {}
        
        for route in self.routes:
            if route.path not in paths:
                paths[route.path] = {}
            
            method = route.method.value.lower()
            paths[route.path][method] = {
                "summary": route.summary,
                "responses": {"200": {"description": "OK"}}
        
        return {
            "openapi": "3.0.0",
            "info": {"title": self.title, "version": self.version},
            "paths": paths
        }
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the server"""
        print(f"Running {self.title} v{self.version} on {host}:{port}")


# =============================================================================
# AGENT FRAMEWORK
# =============================================================================

@dataclass
class Agent:
    """Agent"""
    id: str
    name: str
    
    description: str = ""
    
    skills: List[str] = field(default_factory=list)
    
    tools: List[str] = field(default_factory=list)
    
    instructions: str = ""
    
    model: str = "gpt-4"
    
    temperature: float = 0.7
    
    max_tokens: int = 2000
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "skills": self.skills,
            "tools": self.tools
        }


@dataclass
class Task:
    """Task"""
    id: str
    
    description: str
    
    status: str = "pending"  # pending, running, completed, failed
    
    result: Any = None
    
    error: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    
    completed_at: Optional[datetime] = None
    
    memory: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at.isoformat()
        }


class AgentFramework:
    """Agent Framework"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        
        self.tasks: Dict[str, Task] = {}
        
        self.tool_handlers: Dict[str, Callable] = {}
        
        self.memory: Dict[str, List[Dict]] = {}
    
    def create_agent(
        self,
        name: str,
        description: str = "",
        skills: List[str] = None,
        tools: List[str] = None
    ) -> Agent:
        """Create agent"""
        agent = Agent(
            id=name,
            name=name,
            description=description,
            skills=skills or [],
            tools=tools or []
        )
        self.agents[name] = agent
        return agent
    
    def register_tool(self, name: str, handler: Callable):
        """Register tool"""
        self.tool_handlers[name] = handler
    
    def execute_task(self, agent_id: str, description: str, context: Dict = None) -> Task:
        """Execute task"""
        agent = self.agents.get(agent_id)
        
        if not agent:
            task = Task(id=description, description=description)
            task.status = "failed"
            task.error = "Agent not found"
            return task
        
        # Create task
        task = Task(id=description, description=description)
        task.status = "running"
        self.tasks[task.id] = task
        
        # Execute with tools
        result = self._execute(agent, description, context or {}, task)
        
        task.status = "completed"
        task.result = result
        task.completed_at = datetime.now()
        
        return task
    
    def _execute(self, agent: Agent, description: str, context: Dict, task: Task) -> Any:
        """Execute with tools"""
        results = []
        
        # Check each tool
        for tool in agent.tools:
            if tool in self.tool_handlers:
                result = self.tool_handlers[tool](description, context)
                results.append(result)
                task.memory[tool] = result
        
        return results if results else {"message": "No tools available"}
    
    def get_memory(self, agent_id: str) -> List[Dict]:
        """Get agent memory"""
        return self.memory.get(agent_id, [])
    
    def list_agents(self) -> List[Dict]:
        return [a.to_dict() for a in self.agents.values()]
    
    def list_tasks(self, agent_id: str = None) -> List[Dict]:
        tasks = self.tasks.values()
        if agent_id:
            tasks = [t for t in tasks if t.id.startswith(agent_id)]
        return [t.to_dict() for t in tasks]


# =============================================================================
# ORM FRAMEWORK
# =============================================================================

@dataclass
class Model:
    """ORM Model"""
    id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        result = {}
        for field in self.__dataclass_fields__.values():
            value = getattr(self, field.name, None)
            if value:
                result[field.name] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class QuerySet:
    """QuerySet"""
    
    def __init__(self, model_class: Type[Model], data: List[Dict]):
        self.model_class = model_class
        self.data = data
        self._filters: List[Callable] = []
    
    def filter(self, **kwargs) -> QuerySet:
        """Filter results"""
        def filter_fn(item):
            for key, value in kwargs.items():
                if key not in item or item[key] != value:
                    return False
            return True
        
        return QuerySet(self.model_class, [d for d in self.data if filter_fn(d)])
    
    def exclude(self, **kwargs) -> QuerySet:
        """Exclude results"""
        def filter_fn(item):
            for key, value in kwargs.items():
                if key in item and item[key] == value:
                    return False
            return True
        
        return QuerySet(self.model_class, [d for d in self.data if filter_fn(d)])
    
    def order_by(self, field: str) -> QuerySet:
        """Order results"""
        return QuerySet(
            self.model_class,
            sorted(self.data, key=lambda d: d.get(field, ""))
    
    def first(self) -> Optional[Model]:
        """Get first"""
        if not self.data:
            return None
        return self.model_class.from_dict(self.data[0])
    
    def all(self) -> List[Model]:
        """Get all"""
        return [self.model_class.from_dict(d) for d in self.data]
    
    def count(self) -> int:
        return len(self.data)


class ORMFramework:
    """ORM Framework"""
    
    def __init__(self):
        self.models: Dict[str, Type[Model]] = {}
        self.data: Dict[str, List[Dict]] = {}
    
    def register(self, model_class: Type[Model], table_name: str):
        """Register model"""
        self.models[table_name] = model_class
        self.data[table_name] = []
    
    def create(self, table_name: str, **data) -> Model:
        """Create record"""
        model_class = self.models.get(table_name)
        if not model_class:
            raise ValueError(f"Model {table_name} not found")
        
        model = model_class(**data)
        self.data[table_name].append(model.to_dict())
        return model
    
    def get(self, table_name: str, id: str) -> Optional[Model]:
        """Get by ID"""
        model_class = self.models.get(table_name)
        if not model_class:
            return None
        
        for item in self.data.get(table_name, []):
            if item.get("id") == id:
                return model_class.from_dict(item)
        return None
    
    def filter(self, table_name: str, **kwargs) -> QuerySet:
        """Filter"""
        return QuerySet(self.models.get(table_name), self.data.get(table_name, [])).filter(**kwargs)
    
    def all(self, table_name: str) -> List[Model]:
        """Get all"""
        model_class = self.models.get(table_name)
        if not model_class:
            return []
        return [model_class.from_dict(d) for d in self.data.get(table_name, [])]
    
    def delete(self, table_name: str, id: str) -> bool:
        """Delete"""
        data = self.data.get(table_name, [])
        for i, item in enumerate(data):
            if item.get("id") == id:
                del data[i]
                return True
        return False


# =============================================================================
# CLI FRAMEWORK
# =============================================================================

@dataclass
class Command:
    """CLI Command"""
    name: str
    handler: Callable
    
    description: str = ""
    aliases: List[str] = field(default_factory=list)
    
    options: List[Dict] = field(default_factory=list)


class CLIFramework:
    """CLI Framework"""
    
    def __init__(self, name: str = "cli"):
        self.name = name
        self.commands: Dict[str, Command] = {}
        self.global_options: Dict[str, Any] = {}
    
    def command(self, name: str, description: str = "", aliases: List[str] = None):
        """Decorator for commands"""
        def decorator(func: Callable):
            cmd = Command(
                name=name,
                handler=func,
                description=description,
                aliases=aliases or []
            )
            self.commands[name] = cmd
            return func
        return decorator
    
    def add_option(self, name: str, value: Any):
        """Add global option"""
        self.global_options[name] = value
    
    def parse(self, args: List[str]) -> tuple:
        """Parse arguments"""
        if not args:
            return None, {}
        
        command = args[0] if args[0] in self.commands else None
        
        options = {}
        i = 1
        while i < len(args):
            if args[i].startswith("--"):
                key = args[i][2:]
                if i + 1 < len(args):
                    options[key] = args[i + 1]
                i += 2
            else:
                i += 1
        
        return command, options
    
    def run(self, args: List[str] = None) -> Any:
        """Run command"""
        if args is None:
            args = []
        
        command_name, options = self.parse(args)
        
        if not command_name:
            print(f"Available commands: {', '.join(self.commands.keys())}")
            return
        
        command = self.commands.get(command_name)
        if not command:
            print(f"Unknown command: {command_name}")
            return
        
        return command.handler(**options)
    
    def help(self):
        """Print help"""
        print(f"\n{self.name}")
        print("Commands:")
        for cmd in self.commands.values():
            print(f"  {cmd.name}: {cmd.description}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example - Frameworks"""
    
    print("=" * 50)
    print("Frameworks")
    print("=" * 50)
    
    # Web
    print("\n1. Web Framework")
    app = WebFramework("My API", "1.0.0")
    
    @app.get("/users")
    def get_users(req):
        return [{"id": 1, "name": "John"}]
    
    print(f"   Routes: {len(app.routes)}")
    print(f"   OpenAPI: {bool(app.openapi())")
    
    # Agent
    print("\n2. Agent Framework")
    af = AgentFramework()
    
    agent = af.create_agent("assistant", "Helpful assistant", skills=["search", "compute"])
    af.register_tool("search", lambda q, ctx: {"results": []})
    
    task = af.execute_task("assistant", "Find information")
    print(f"   Agent: {agent.name}")
    print(f"   Task: {task.status}")
    
    # ORM
    print("\n3. ORM Framework")
    orm = ORMFramework()
    
    @dataclass
    class User(Model):
        name: str = ""
        email: str = ""
    
    orm.register(User, "users")
    orm.create("users", name="John", email="john@example.com")
    
    users = orm.all("users")
    print(f"   Users: {len(users)}")
    
    # CLI
    print("\n4. CLI Framework")
    cli = CLIFramework("myapp")
    
    @cli.command("greet", description="Greet user")
    def greet(name: str = "World"):
        print(f"Hello, {name}!")
    
    cli.run(["greet", "--name", "Alice"])


if __name__ == "__main__":
    main()


"""
Framework Usage

    # Web Framework
    app = WebFramework("API")
    @app.get("/items")
    def get_items(req): return []
    app.run()
    
    # Agent Framework
    af = AgentFramework()
    af.create_agent("assistant", skills=["search"])
    task = af.execute_task("assistant", "task")
    
    # ORM Framework
    orm = ORMFramework()
    orm.register(User, "users")
    orm.create("users", name="John")
    users = orm.all("users")
    
    # CLI Framework
    cli = CLIFramework()
    @cli.command("hello")
    def hello(name="World"): print(f"Hello {name}")
    cli.run(["hello", "--name", "World"])
"""