"""
Additional Platform Components

More components:
- Authentication (OAuth, JWT)
- Caching
- Configuration
- Events/Event Bus
- Cache invalidation
- Rate limiting

Dependencies: Standard library only
"""

from __future__ import annotation
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import time


# =============================================================================
# AUTHENTICATION
# =============================================================================

class AuthProvider(Enum):
    OAuth2 = "oauth2"
    JWT = "jwt"
    API_KEY = "api_key"
    BASIC = "basic"


@dataclass
class User:
    """User"""
    id: str
    username: str
    email: str
    
    password_hash: str = ""
    
    roles: List[str] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)
    
    last_login: Optional[datetime] = None
    
    active: bool = True
    
    mfa_enabled: bool = False


@dataclass
class Token:
    """Token"""
    id: str
    
    user_id: str
    
    access_token: str
    
    refresh_token: str
    
    expires_at: datetime
    
    token_type: str = "Bearer"
    
    scopes: List[str] = field(default_factory=list)
    
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


class AuthManager:
    """Authentication Manager"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        
        self.tokens: Dict[str, Token] = {}
        
        self.sessions: Dict[str, Dict] = {}
    
    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        roles: List[str] = None
    ) -> User:
        """Register user"""
        user_id = secrets.token_urlsafe(16)
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            roles=roles or ["user"]
        )
        
        self.users[user_id] = user
        
        return user
    
    def login(self, username: str, password: str) -> Optional[Token]:
        """Login"""
        # Find user
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            return None
        
        # Check password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return None
        
        # Create token
        return self.create_token(user.id)
    
    def create_token(self, user_id: str, expires_hours: int = 24) -> Token:
        """Create token"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        
        token = Token(
            id=secrets.token_urlsafe(16),
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.now() + timedelta(hours=expires_hours),
            scopes=user.roles
        )
        
        self.tokens[access_token] = token
        
        user.last_login = datetime.now()
        
        return token
    
    def verify_token(self, access_token: str) -> Optional[User]:
        """Verify token"""
        token = self.tokens.get(access_token)
        
        if not token or token.is_expired():
            return None
        
        return self.users.get(token.user_id)
    
    def revoke_token(self, access_token: str) -> bool:
        """Revoke token"""
        if access_token in self.tokens:
            del self.tokens[access_token]
            return True
        return False
    
    def has_role(self, user_id: str, role: str) -> bool:
        """Check role"""
        user = self.users.get(user_id)
        if not user:
            return False
        return role in user.roles


# =============================================================================
# CACHING
# =============================================================================

@dataclass
class CacheEntry:
    """Cache entry"""
    key: str
    value: Any
    
    expires_at: Optional[datetime] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    
    hits: int = 0
    
    def is_expired(self) -> bool:
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False
    
    def touch(self):
        self.hits += 1


class Cache:
    """Cache"""
    
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        
        self.entries: Dict[str, CacheEntry] = {}
        
        self.eviction_callbacks: List[Callable] = []
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value"""
        entry = self.entries.get(key)
        
        if not entry:
            return default
        
        if entry.is_expired():
            self.delete(key)
            return default
        
        entry.touch()
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value"""
        ttl = ttl or self.default_ttl
        
        entry = CacheEntry(
            key=key,
            value=value,
            expires_at=datetime.now() + timedelta(seconds=ttl)
        )
        
        self.entries[key] = entry
    
    def delete(self, key: str) -> bool:
        """Delete"""
        if key in self.entries:
            del self.entries[key]
            return True
        return False
    
    def clear(self):
        """Clear all"""
        self.entries.clear()
    
    def has(self, key: str) -> bool:
        """Check exists"""
        entry = self.entries.get(key)
        if not entry:
            return False
        if entry.is_expired():
            self.delete(key)
            return False
        return True
    
    def size(self) -> int:
        return len(self.entries)
    
    def stats(self) -> Dict:
        """Get stats"""
        hits = sum(e.hits for e in self.entries.values())
        return {
            "size": len(self.entries),
            "total_hits": hits,
            "avg_hits": hits / len(self.entries) if self.entries else 0
        }


# =============================================================================
# CONFIGURATION
# =============================================================================

class ConfigManager:
    """Configuration manager"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        
        self.secrets: Dict[str, str] = {}
        
        self.overrides: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any):
        """Set config"""
        self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config"""
        if key in self.overrides:
            return self.overrides[key]
        
        if key in self.config:
            return self.config[key]
        
        return default
    
    def set_secret(self, key: str, value: str):
        """Set secret"""
        self.secrets[key] = value
    
    def get_secret(self, key: str) -> Optional[str]:
        """Get secret"""
        return self.secrets.get(key)
    
    def override(self, key: str, value: Any):
        """Override config (for testing)"""
        self.overrides[key] = value
    
    def load_env(self, prefix: str = "APP_"):
        """Load from environment"""
        import os
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self.config[config_key] = value
    
    def to_dict(self, include_secrets: bool = False) -> Dict:
        """Export config"""
        result = dict(self.config)
        
        if include_secrets:
            result.update(self.secrets)
        
        return result


# =============================================================================
# EVENT BUS
# =============================================================================

class Event:
    """Event"""
    
    def __init__(self, type: str, data: Dict = None):
        self.type = type
        self.data = data or {}
        self.timestamp = datetime.now()


class EventBus:
    """Event bus"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        
        self.event_history: List[Event] = []
        
        self.max_history: int = 1000
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to event"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        
        self.listeners[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe"""
        if event_type in self.listeners:
            if handler in self.listeners[event_type]:
                self.listeners[event_type].remove(handler)
    
    def publish(self, event: Event):
        """Publish event"""
        # Store in history
        self.event_history.append(event)
        
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        # Notify listeners
        handlers = self.listeners.get(event.type, [])
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Event handler error: {e}")
    
    def on(self, event_type: str):
        """Decorator for events"""
        def decorator(func: Callable):
            self.subscribe(event_type, func)
            return func
        return decorator
    
    def get_history(self, event_type: str = None) -> List[Event]:
        """Get event history"""
        if event_type:
            return [e for e in self.event_history if e.type == event_type]
        return list(self.event_history)


# =============================================================================
# RATE LIMITER
# =============================================================================

class RateLimiter:
    """Rate limiter"""
    
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        
        self.clients: Dict[str, List[datetime]] = {}
    
    def check(self, client_id: str) -> bool:
        """Check if allowed"""
        now = datetime.now()
        
        if client_id not in self.clients:
            self.clients[client_id] = []
        
        # Clean old requests
        self.clients[client_id] = [
            t for t in self.clients[client_id]
            if (now - t).total_seconds() < self.window
        ]
        
        # Check limit
        if len(self.clients[client_id]) >= self.requests:
            return False
        
        # Add request
        self.clients[client_id].append(now)
        
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests"""
        if client_id not in self.clients:
            return self.requests
        
        now = datetime.now()
        
        self.clients[client_id] = [
            t for t in self.clients[client_id]
            if (now - t).total_seconds() < self.window
        ]
        
        return max(0, self.requests - len(self.clients[client_id]))
    
    def reset(self, client_id: str):
        """Reset for client"""
        if client_id in self.clients:
            del self.clients[client_id]


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Authentication & Caching")
    print("=" * 50)
    
    # Auth
    print("\n1. Authentication")
    auth = AuthManager()
    
    user = auth.register_user("john", "john@example.com", "password123", ["admin"])
    print(f"   User registered: {user.username}")
    
    token = auth.login("john", "password123")
    print(f"   Token created: {token.access_token[:20]}...")
    
    verified = auth.verify_token(token.access_token)
    print(f"   Verified: {verified.username if verified else 'Invalid'}")
    
    # Cache
    print("\n2. Cache")
    cache = Cache(default_ttl=60)
    
    cache.set("key1", "value1")
    print(f"   Get: {cache.get('key1')}")
    print(f"   Has: {cache.has('key1')}")
    print(f"   Stats: {cache.stats()}")
    
    # Config
    print("\n3. Configuration")
    config = ConfigManager()
    
    config.set("database", "postgresql")
    config.set_secret("db_password", "secret123")
    config.override("debug", True)
    
    print(f"   Database: {config.get('database')}")
    print(f"   Debug: {config.get('debug')}")
    print(f"   Secret: {config.get_secret('db_password')}")
    
    # Event Bus
    print("\n4. Event Bus")
    events = EventBus()
    
    @events.on("user.created")
    def handle_user_created(event):
        print(f"   Event: {event.type}, {event.data}")
    
    events.publish(Event("user.created", {"user_id": "123"}))
    
    # Rate Limiter
    print("\n5. Rate Limiter")
    limiter = RateLimiter(requests=10, window=60)
    
    for i in range(5):
        print(f"   Check {i}: {limiter.check('client1')}")
    
    print(f"   Remaining: {limiter.get_remaining('client1')}")


if __name__ == "__main__":
    main()


"""
Usage

    # Auth
    auth = AuthManager()
    user = auth.register_user("john", "john@example.com", "password")
    token = auth.login("john", "password")
    auth.verify_token(token.access_token)
    
    # Cache
    cache = Cache()
    cache.set("key", "value")
    cache.get("key")
    
    # Config
    config = ConfigManager()
    config.set("key", "value")
    config.get("key")
    
    # Event Bus
    events = EventBus()
    events.subscribe("event", handler)
    events.publish(Event("event", {}))
    
    # Rate Limiter
    limiter = RateLimiter()
    limiter.check("client")
"""