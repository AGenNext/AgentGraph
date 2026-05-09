"""Database models and connection tests."""
import os
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor

# Test database URL
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://agent:agent@host.docker.internal:5432/agent"
)

class TestDatabaseConnection:
    """Test PostgreSQL connection."""
    
    def test_can_connect(self):
        """Test database connection."""
        conn = psycopg2.connect(TEST_DATABASE_URL)
        c = conn.cursor()
        c.execute("SELECT 1 as test")
        result = c.fetchone()
        conn.close()
        assert result[0] == 1
    
    def test_tables_exist(self):
        """Test tasks table exists."""
        conn = psycopg2.connect(TEST_DATABASE_URL, cursor_factory=RealDictCursor)
        c = conn.cursor()
        c.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'tasks'
        """)
        result = c.fetchone()
        conn.close()
        assert result is not None, "tasks table should exist"

class TestCRUDOperations:
    """Test CRUD operations."""
    
    def test_create_task(self):
        """Test creating a task."""
        task_id = f"test-{pytest.timestamp}"
        conn = psycopg2.connect(TEST_DATABASE_URL)
        c = conn.cursor()
        c.execute("""
            INSERT INTO tasks (id, status, framework, submission, created_at)
            VALUES (%s, 'pending', 'test', '{}', NOW())
            ON CONFLICT (id) DO UPDATE SET status = 'pending'
        """, (task_id,))
        conn.commit()
        
        c.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        result = c.fetchone()
        conn.close()
        
        assert result is not None
        assert result[1] == 'pending'
    
    def test_read_task(self):
        """Test reading a task."""
        conn = psycopg2.connect(TEST_DATABASE_URL, cursor_factory=RealDictCursor)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks LIMIT 1")
        result = c.fetchall()
        conn.close()
        assert isinstance(result, list)
    
    def test_update_task(self):
        """Test updating a task."""
        task_id = f"test-update-{pytest.timestamp}"
        conn = psycopg2.connect(TEST_DATABASE_URL)
        c = conn.cursor()
        c.execute("""
            INSERT INTO tasks (id, status, framework, submission, created_at)
            VALUES (%s, 'pending', 'test', '{}', NOW())
        """, (task_id,))
        conn.commit()
        
        c.execute("UPDATE tasks SET status = 'completed' WHERE id = %s", (task_id,))
        conn.commit()
        
        c.execute("SELECT status FROM tasks WHERE id = %s", (task_id,))
        result = c.fetchone()
        conn.close()
        
        assert result[0] == 'completed'
    
    def test_delete_task(self):
        """Test deleting a task."""
        task_id = f"test-delete-{pytest.timestamp}"
        conn = psycopg2.connect(TEST_DATABASE_URL)
        c = conn.cursor()
        c.execute("""
            INSERT INTO tasks (id, status, framework, submission, created_at)
            VALUES (%s, 'pending', 'test', '{}', NOW())
        """, (task_id,))
        conn.commit()
        
        c.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        
        c.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        result = c.fetchone()
        conn.close()
        
        assert result is None

# Add timestamp for unique test IDs
pytest.timestamp = "1700000000"