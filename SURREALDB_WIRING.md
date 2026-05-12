# SurrealDB Schema.org Wiring

## Overview

SurrealDB is an embedded in-memory graph database that can be used as a drop-in replacement for PostgreSQL, MySQL, Redis, and more.

Reference: https://surrealdb.com

## SurrealDB → Schema.org

| SurrealDB Feature | Schema.org Type | Database |
|------------------|-----------------|----------|
| Thing records | Thing | All types |
| Graph relations | Action | Relationships |
| Tables | CreativeWork | Datasets |
| Live queries | Action | Real-time |
| Schemas | PropertyValue | Type definitions |

## Implementation

```python
from surrealdb import AsyncSurreal

@dataclass
class SurrealDBConnection:
    # Connection
    host: str = "localhost"
    port: int = 8000
    namespace: str = "test"
    database: str = "test"
    username: str = "root"
    password: str = "root"
    
    # Schema.org
    additional_type: str = "WebAPI"

# Schema.org Type to SurrealDB Table Mapping
SCHEMA_TO_TABLE = {
    "Person": "persons",
    "Organization": "organizations", 
    "Place": "places",
    "Product": "products",
    "Event": "events",
    "CreativeWork": "creative_works",
    "Action": "actions",
    "Intangible": "intangibles",
    "MedicalEntity": "medical_entities",
}

# Example: Schema.org Person in SurrealDB
PERSON_SCHEMA = """
DEFINE TABLE persons SCHEMAFULL;
DEFINE FIELD name ON TABLE persons TYPE string;
DEFINE FIELD description ON TABLE persons TYPE string;
DEFINE FIELD url ON TABLE persons TYPE string;
DEFINE FIELD image ON TABLE persons TYPE string;
DEFINE FIELD jobTitle ON TABLE persons TYPE string;
DEFINE FIELD birthDate ON TABLE persons TYPE datetime;
DEFINE FIELD address ON TABLE persons TYPE option<object>;
DEFINE FIELD email ON TABLE persons TYPE option<string>;
DEFINE FIELD telephone ON TABLE persons TYPE option<string>;

DEFINE INDEX idx_name ON TABLE persons FIELDS name SEARCH ANALYZER ascii BM25;
"""
```

## Live Queries (Schema.org Action)

```python
# Real-time updates using SurrealDB Live Queries
LIVE_QUERY_ACTION = """
LIVE SELECT * FROM persons WHERE jobTitle = 'Engineer';
"""
# Maps to Schema.org Action: ViewAction with real-time result
```

## Graph Relations

```python
# SurrealDB graph relations → Schema.org Action
RELATION_QUERIES = {
    "person_works_for_org": """
        RELATE person:john->works_for->organization:acme
        RETURN { role: 'Engineer', since: '2020-01-01' }
    """,
    # Maps to Schema.org: Organization > employee
    "person_member_of": """
        RELATE person:jane->member_of->organization:acme
        RETURN { role: 'Admin' }
    """,
    # Maps to Schema.org: Organization > member
    "follows": """
        RELATE person:alice->follows->person:bob
    """,
    # Maps to Schema.org: FollowAction
    "authored": """
        RELATE author:john->authored->creative_work:book1
    """,
    # Maps to Schema.org: CreativeWork > author
}
```

## Schema.org Type Definitions

```python
# Define all Schema.org types in SurrealDB
SCHEMA_DEFINITIONS = {
    # Core types
    "Thing": """
        DEFINE TABLE things SCHEMAFULL;
        DEFINE FIELD name ON things TYPE string;
        DEFINE FIELD description ON things TYPE option<string>;
        DEFINE FIELD url ON things TYPE option<string>;
        DEFINE FIELD image ON things TYPE option<string>;
    """,
    "Person": "DEFINE TABLE persons SCHEMAFULL; ...",
    "Organization": "DEFINE TABLE organizations SCHEMAFULL; ...",
    "Place": "DEFINE TABLE places SCHEMAFULL; ...",
    "Product": "DEFINE TABLE products SCHEMAFULL; ...",
    "Event": "DEFINE TABLE events SCHEMAFULL; ...",
    "CreativeWork": "DEFINE TABLE creative_works SCHEMAFULL; ...",
    "Action": "DEFINE TABLE actions SCHEMAFULL; ...",
    "Intangible": "DEFINE TABLE intangibles SCHEMAFULL; ...",
}
```

## SurrealDB ORM Integration

```python
# Maps Python dataclasses to SurrealDB
class SchemaOrgORM:
    """Map Schema.org types to SurrealDB"""
    
    def define_schema(self, schema_type: str) -> str:
        """Generate SurrealDB DEFINE statement"""
        return SCHEMA_DEFINITIONS.get(schema_type, "")
    
    def to_table(self, schema_type: str) -> str:
        """Get table name for Schema.org type"""
        return SCHEMA_TO_TABLE.get(schema_type, schema_type.lower())
```

## Database Integration

```python
# Alternative database backends
DATABASE_BACKENDS = {
    "surrealdb": "Embedded, in-memory, graph",
    "postgresql": "Relational",
    "mysql": "Relational", 
    "redis": "Key-value",
    "mongodb": "Document",
}
```

Reference: https://surrealdb.com/docs | https://schema.org/docs/full.html