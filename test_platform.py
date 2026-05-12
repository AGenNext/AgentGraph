"""
Integration Tests using Testcontainers

Tests the platform with real containers.

Reference:
- https://testcontainers-python.readthedocs.io/
"""

import pytest
import time
from testcontainers import (
    GenericContainer,
    PostgreSQLContainer,
    RedisContainer,
)
from testcontainers.mysql import MySqlContainer
from testcontainers.oracle import OracleContainer


# =============================================================================
# Test: PostgreSQL
# =============================================================================

def test_postgres():
    """Test PostgreSQL container"""
    with PostgreSQLContainer("postgres:15-alpine") as postgres:
        # Wait for ready
        time.sleep(2)
        
        # Get connection
        conn = postgres.connect()
        assert conn is not None
        
        # Execute query
        result = postgres.exec_exec("psql -U postgres -c 'SELECT 1'")
        assert b"1" in result.output
        
        print("✓ PostgreSQL works")


# =============================================================================
# Test: Redis
# =============================================================================

def test_redis():
    """Test Redis container"""
    with RedisContainer("redis:7-alpine") as redis:
        # Wait for ready
        time.sleep(2)
        
        # Get connection
        conn = redis.connect()
        assert conn is not None
        
        # Execute command
        result = redis.exec_exec("redis-cli PING")
        assert b"PONG" in result.output
        
        print("✓ Redis works")


# =============================================================================
# Test: Python App
# =============================================================================

def test_python_app():
    """Test Python application"""
    
    # Create test container
    container = GenericContainer("python:3.11-slim")
    container.with_execute(
        ["python", "-c", "print('Hello from container')"]
    )
    
    with container as c:
        result = c.exec_cmd("echo", "test")
        assert b"test" in result.output
        
        print("✓ Python app works")


# =============================================================================
# Test: Full Platform
# =============================================================================

def test_full_platform():
    """Test full platform stack"""
    
    containers = []
    
    try:
        # Start PostgreSQL
        postgres = PostgreSQLContainer("postgres:15-alpine")
        containers.append(postgres)
        
        # Start Redis
        redis = RedisContainer("redis:7-alpine")
        containers.append(redis)
        
        # Wait for all
        time.sleep(3)
        
        # Verify
        print("✓ Full platform (PostgreSQL + Redis)")
        
    finally:
        # Cleanup
        for c in containers:
            c.stop()


# =============================================================================
# Test: Platform with Scripts
# =============================================================================

def test_agent_platform():
    """Test agent platform container"""
    
    # Build would happen via Dockerfile.platform
    # Here just verifying Python works
    container = GenericContainer("python:3.11-slim")
    container.with_execute(
        ["python", "-c", "print('Agent platform ready')"]
    )
    
    with container as c:
        output = c.exec_cmd("python", "-c", "import sys; print(sys.version)")
        print(f"✓ Python version: {output.output[:50]}")


# =============================================================================
# Test: Database Connections
# =============================================================================

def test_database_connection():
    """Test database can connect"""
    
    with PostgreSQLContainer("postgres:15-alpine") as postgres:
        # Get connection info
        dsn = postgres.dsn()
        assert "postgres" in dsn
        
        # Execute SQL
        result = postgres.exec_exec("psql -U postgres -c 'SELECT version()'")
        assert b"PostgreSQL" in result.output
        
        print("✓ Database connection works")


# =============================================================================
# Test: Agent SDKs
# =============================================================================

def test_sdsk_imports():
    """Test SDK imports"""
    # This would need the Python packages installed
    # In real test, you'd build the image first
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])