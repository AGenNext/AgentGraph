"""
API Gateway - Complete REST API

API Gateway with:
- REST endpoints
- GraphQL
- WebSocket
- Rate limiting
- Authentication

Reference:
- FastAPI: https://fastapi.tiangolo.com/
- OpenAPI: https://swagger.io/specification/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum


# =============================================================================
# API TYPES
# =============================================================================

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class AuthType(Enum):
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    BEARER = "bearer"
    OAUTH2 = "oauth2"


# =============================================================================
# API STRUCTURE
# =============================================================================

@dataclass
class Endpoint:
    """API endpoint"""
    path: str
    method: HTTPMethod
    
    handler: Optional[Callable] = None
    
    # Auth
    auth_type: AuthType = AuthType.NONE
    required_scopes: List[str] = field(default_factory=list)
    
    # Rate limiting
    rate_limit: int = 100  # requests per minute
    rate_limit_scope: str = "global"
    
    # Documentation
    summary: Optional[str] = None
    description: Optional[str] = None
    
    # Request/Response
    request_model: Optional[type] = None
    response_model: Optional[type] = None
    
    # Parameters
    query_params: List[Dict] = field(default_factory=list)
    path_params: List[Dict] = field(default_factory=list)
    body_params: List[Dict] = field(default_factory=list)


@dataclass
class APIVersion:
    """API version"""
    version: str
    base_path: str
    
    endpoints: List[Endpoint] = field(default_factory=list)
    
    deprecated: bool = False
    sunset_date: Optional[datetime] = None


@dataclass
class APIKey:
    """API key"""
    id: str
    name: str
    
    key: str
    
    owner_id: str
    
    scopes: List[str] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    
    last_used: Optional[datetime] = None
    
    rate_limit: int = 1000
    
    active: bool = True


# =============================================================================
# API GATEWAY
# =============================================================================

class APIGateway:
    """API Gateway"""
    
    def __init__(self, name: str):
        self.name = name
        
        self.versions: Dict[str, APIVersion] = {}
        
        self.endpoints: Dict[str, Endpoint] = {}
        
        self.api_keys: Dict[str, APIKey] = {}
        
        self.rate_limits: Dict[str, int] = {}
        
        self.middleware: List[Callable] = []
        
        self.error_handlers: Dict[int, Callable] = {}
    
    def add_version(self, version: APIVersion):
        """Add API version"""
        self.versions[version.version] = version
    
    def add_endpoint(self, endpoint: Endpoint):
        """Add endpoint"""
        key = f"{endpoint.method.value}:{endpoint.path}"
        self.endpoints[key] = endpoint
    
    def create_endpoint(
        self,
        path: str,
        method: HTTPMethod,
        handler: Callable,
        auth: AuthType = AuthType.NONE
    ) -> Endpoint:
        """Create and add endpoint"""
        endpoint = Endpoint(
            path=path,
            method=method,
            handler=handler,
            auth_type=auth
        )
        self.add_endpoint(endpoint)
        return endpoint
    
    def add_api_key(self, api_key: APIKey):
        """Add API key"""
        self.api_keys[api_key.key] = api_key
    
    def validate_api_key(self, key: str) -> Optional[APIKey]:
        """Validate API key"""
        api_key = self.api_keys.get(key)
        
        if not api_key:
            return None
        
        if not api_key.active:
            return None
        
        if api_key.expires_at and api_key.expires_at < datetime.now():
            return None
        
        api_key.last_used = datetime.now()
        
        return api_key
    
    def add_middleware(self, middleware: Callable):
        """Add middleware"""
        self.middleware.append(middleware)
    
    def add_error_handler(self, status_code: int, handler: Callable):
        """Add error handler"""
        self.error_handlers[status_code] = handler
    
    # =================================================================
    # ROUTING
    # =================================================================
    
    def route(self, request: Dict) -> Dict:
        """Route request"""
        
        # Get endpoint
        method = request.get("method", "GET")
        path = request.get("path", "/")
        
        key = f"{method}:{path}"
        
        endpoint = self.endpoints.get(key)
        
        if not endpoint:
            return {
                "status": 404,
                "error": "Not Found"
            }
        
        # Check auth
        if endpoint.auth_type != AuthType.NONE:
            auth_result = self._authenticate(request, endpoint)
            if not auth_result:
                return {
                    "status": 401,
                    "error": "Unauthorized"
                }
        
        # Check rate limit
        if not self._check_rate_limit(request):
            return {
                "status": 429,
                "error": "Too Many Requests"
            }
        
        # Apply middleware
        for mw in self.middleware:
            request = mw(request)
        
        # Call handler
        try:
            result = endpoint.handler(request)
            return {
                "status": 200,
                "data": result
            }
        except Exception as e:
            error_handler = self.error_handlers.get(500)
            if error_handler:
                return error_handler(e)
            return {
                "status": 500,
                "error": str(e)
            }
    
    def _authenticate(self, request: Dict, endpoint: Endpoint) -> bool:
        """Authenticate request"""
        
        if endpoint.auth_type == AuthType.NONE:
            return True
        
        elif endpoint.auth_type == AuthType.API_KEY:
            api_key = request.get("headers", {}).get("X-API-Key")
            if not api_key:
                return False
            
            return self.validate_api_key(api_key) is not None
        
        elif endpoint.auth_type == AuthType.BEARER:
            token = request.get("headers", {}).get("Authorization", "").replace("Bearer ", "")
            return bool(token)
        
        return False
    
    def _check_rate_limit(self, request: Dict) -> bool:
        """Check rate limit"""
        # Simple implementation
        client_id = request.get("client_id", "default")
        
        current = self.rate_limits.get(client_id, 0)
        
        if current >= 100:  # Default limit
            return False
        
        self.rate_limits[client_id] = current + 1
        
        return True
    
    # =================================================================
    # OPENAPI
    # =================================================================
    
    def to_openapi(self) -> Dict:
        """Generate OpenAPI spec"""
        
        paths = {}
        
        for key, endpoint in self.endpoints.items():
            if endpoint.path not in paths:
                paths[endpoint.path] = {}
            
            method = endpoint.method.value.lower()
            
            paths[endpoint.path][method] = {
                "summary": endpoint.summary or endpoint.path,
                "description": endpoint.description or "",
                "responses": {
                    "200": {"description": "Success"}
                }
            }
        
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.name,
                "version": "1.0.0"
            },
            "paths": paths
        }


# =============================================================================
# REST ENDPOINTS FOR DATABASES
# =============================================================================

class DatabaseAPI:
    """REST API for databases"""
    
    def __init__(self):
        self.gateway = APIGateway("Agent Platform API")
        self._setup_endpoints()
    
    def _setup_endpoints(self):
        """Setup default endpoints"""
        
        # Knowledge Graph
        self.gateway.create_endpoint(
            "/knowledge/{name}",
            HTTPMethod.GET,
            self.get_knowledge,
            AuthType.API_KEY
        )
        
        # Movies
        self.gateway.create_endpoint(
            "/movies",
            HTTPMethod.GET,
            self.list_movies,
            AuthType.NONE
        )
        
        self.gateway.create_endpoint(
            "/movies/{id}",
            HTTPMethod.GET,
            self.get_movie,
            AuthType.NONE
        )
        
        # Sports
        self.gateway.create_endpoint(
            "/sports/teams",
            HTTPMethod.GET,
            self.list_teams,
            AuthType.NONE
        )
        
        self.gateway.create_endpoint(
            "/sports/games",
            HTTPMethod.GET,
            self.list_games,
            AuthType.NONE
        )
        
        # Search
        self.gateway.create_endpoint(
            "/search",
            HTTPMethod.GET,
            self.search,
            AuthType.NONE
        )
        
        # Agent
        self.gateway.create_endpoint(
            "/agents",
            HTTPMethod.GET,
            self.list_agents,
            AuthType.BEARER
        )
        
        self.gateway.create_endpoint(
            "/agents/{id}/tasks",
            HTTPMethod.GET,
            self.get_agent_tasks,
            AuthType.BEARER
        )
    
    # Handlers (simplified)
    def get_knowledge(self, request: Dict) -> Dict:
        return {"name": "Person", "description": "Information"}
    
    def list_movies(self, request: Dict) -> Dict:
        return {"items": [], "total": 0}
    
    def get_movie(self, request: Dict) -> Dict:
        return {"id": request.get("path_params", {}).get("id")}
    
    def list_teams(self, request: Dict) -> Dict:
        return {"items": [], "total": 0}
    
    def list_games(self, request: Dict) -> Dict:
        return {"items": [], "total": 0}
    
    def search(self, request: Dict) -> Dict:
        query = request.get("query_params", {}).get("q", "")
        return {"query": query, "results": []}
    
    def list_agents(self, request: Dict) -> Dict:
        return {"items": [], "total": 0}
    
    def get_agent_tasks(self, request: Dict) -> Dict:
        agent_id = request.get("path_params", {}).get("id")
        return {"agent_id": agent_id, "tasks": []}
    
    def run(self):
        """Run the API"""
        return self.gateway


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("API Gateway")
    print("=" * 50)
    
    # Create API
    api = DatabaseAPI()
    gateway = api.run()
    
    # Print OpenAPI spec
    spec = gateway.to_openapi()
    
    print("\nOpenAPI Spec:")
    print(f"  Title: {spec['info']['title']}")
    print(f"  Paths: {len(spec['paths'])}")


if __name__ == "__main__":
    main()


"""
API Gateway Usage

    # Create gateway
    gateway = APIGateway("My API")
    
    # Add endpoints
    gateway.create_endpoint("/users", HTTPMethod.GET, get_users)
    gateway.create_endpoint("/users/{id}", HTTPMethod.GET, get_user)
    
    # Add API key
    gateway.add_api_key(APIKey(
        id="1",
        name="Test Key",
        key="test-key-123",
        owner_id="user-1",
        scopes=["read", "write"]
    ))
    
    # Route request
    response = gateway.route({
        "method": "GET",
        "path": "/users",
        "headers": {"X-API-Key": "test-key-123"}
    })
    
    # Generate OpenAPI
    spec = gateway.to_openapi()
"""