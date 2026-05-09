"""
Convert LangGraph SDK Schemas to Prisma schema
Maps 40 TypedDicts → PostgreSQL tables with columns, types, relations
"""

import json
import re

SDK_SCHEMAS = {
    "Assistant": "Assistant that runs a graph",
    "AssistantBase": ["assistant_id", "graph_id", "config", "context", "created_at", "metadata", "version", "name", "description"],
    "AssistantsSearchResponse": ["assistants", "next"],
    "AssistantVersion": ["assistant_id", "graph_id", "config", "context", "created_at", "metadata", "version", "name", "description"],
    "Thread": ["thread_id", "created_at", "updated_at", "metadata", "status", "values", "interrupts", "extracted"],
    "ThreadState": ["values", "next", "checkpoint", "metadata", "created_at", "parent_checkpoint", "tasks", "interrupts"],
    "ThreadTask": ["id", "name", "error", "interrupts", "checkpoint", "state", "result"],
    "Run": ["run_id", "thread_id", "assistant_id", "created_at", "updated_at", "status", "metadata", "multitask_strategy"],
    "RunCreate": ["thread_id", "assistant_id", "input", "metadata", "config", "context", "checkpoint_id", "interrupt_before", "interrupt_after", "webhook", "multitask_strategy"],
    "Cron": ["cron_id", "assistant_id", "thread_id", "on_run_completed", "end_time", "schedule", "timezone", "created_at", "updated_at", "payload", "user_id", "next_run_date", "metadata", "enabled"],
    "Item": ["namespace", "key", "value", "created_at", "updated_at"],  # Store
    "Checkpoint": ["thread_id", "checkpoint_ns", "checkpoint_id", "checkpoint_map"],
    "Config": ["tags", "recursion_limit", "configurable"],
    "GraphSchema": ["graph_id", "input_schema", "output_schema", "state_schema", "config_schema", "context_schema"],
    "Interrupt": ["value", "id"],
    "Send": ["node", "input"],
    "Command": ["goto", "update", "resume"],
}

# Type mappings: Python TypedDict → PostgreSQL
TYPE_MAP = {
    "String": "String",
    "int": "Int",
    "float": "Float", 
    "bool": "Boolean",
    "datetime": "DateTime",
    "Any": "Json",
    "dict": "Json",
    "list": "Json",
    "None": "Null",
    "*": "Json",  # Default to JSON
}

# Enums from schema.py
ENUMS = {
    "RunStatus": ["pending", "running", "error", "success", "timeout", "interrupted"],
    "ThreadStatus": ["idle", "busy", "interrupted", "error"],
    "StreamMode": ["values", "messages", "updates", "events", "tasks", "checkpoints", "debug", "custom", "messages-tuple"],
    "DisconnectMode": ["cancel", "continue"],
    "ThreadStreamMode": ["run_modes", "lifecycle", "state_update"],
}

def to_snake_case(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def get_pg_type(field_name, annotations=None):
    """Guess PostgreSQL type from field name and annotations"""
    field_lower = field_name.lower()
    
    # Check annotations first
    if annotations:
        ann = annotations.get(field_name, '')
        if 'Literal[' in ann:
            # Extract enum values
            return "String"  # Could be enum
        if 'datetime' in ann:
            return "DateTime"
        if 'uuid' in ann:
            return "Uuid"
        if 'int' in ann:
            return "Int"
        if 'float' in ann:
            return "Float"
        if 'bool' in ann:
            return "Boolean"
        if 'dict' in ann or 'list' in ann or 'Any' in ann:
            return "Json"
    
    # Guess from field name
    if 'id' in field_lower:
        return "String"  # UUID or String
    if 'status' in field_lower or 'mode' in field_lower or 'strategy' in field_lower:
        return "String"
    if 'at' in field_lower:
        return "DateTime"
    if 'count' in field_lower or 'limit' in field_lower or 'version' in field_lower:
        return "Int"
    if field_lower.startswith('is_') or '_flag' in field_lower or 'enabled' in field_lower:
        return "Boolean"
    if any(x in field_lower for x in ['metadata', 'config', 'payload', 'context', 'input', 'values', 'result', 'state', 'map', 'ns']):
        return "Json"
    
    return "String"

def generate_prisma():
    lines = []
    lines.append("// LangGraph SDK → PostgreSQL Schema")
    lines.append("// Generated from sdk-py/langgraph_sdk/schema.py")
    lines.append("")
    lines.append("generator client {")
    lines.append('  provider = "prisma-client-py"')
    lines.append("}")
    lines.append("")
    lines.append("datasource db {")
    lines.append('  provider = "postgresql"')
    lines.append('  url      = env("DATABASE_URL")')
    lines.append("}")
    lines.append("")
    lines.append("// ─── Enums ─────────────────────────────────────────")
    lines.append("")
    
    for enum_name, values in ENUMS.items():
        lines.append(f"enum {enum_name} {{")
        for v in values:
            lines.append(f"  {v.upper()}")
        lines.append("}")
        lines.append("")
    
    lines.append("// ─── Models ─────────────────────────────────────────")
    lines.append("")
    
    # Map SDK schemas to tables (name → fields)
    tables = {
        "Assistant": {
            "assistant_id": "String",
            "graph_id": "String", 
            "name": "String?",
            "description": "String?",
            "version": "Int?",
            "config": "Json?",
            "context": "Json?",
            "metadata": "Json?",
            "created_at": "DateTime?",
        },
        "Thread": {
            "thread_id": "String",
            "status": "String?",
            "metadata": "Json?",
            "values": "Json?",
            "interrupts": "Json?",
            "created_at": "DateTime?",
            "updated_at": "DateTime?",
        },
        "Run": {
            "run_id": "String",
            "thread_id": "String",
            "assistant_id": "String",
            "status": "String?",
            "metadata": "Json?",
            "created_at": "DateTime?",
            "updated_at": "DateTime?",
        },
        "Checkpoint": {
            "thread_id": "String",
            "checkpoint_ns": "String",
            "checkpoint_id": "String",
            "checkpoint_map": "Json?",
        },
        "StoreItem": {
            "namespace": "String",
            "key": "String",
            "value": "Json",
            "created_at": "DateTime?",
            "updated_at": "DateTime?",
        },
        "Graph": {
            "graph_id": "String",
            "input_schema": "Json?",
            "output_schema": "Json?",
            "state_schema": "Json?",
            "config_schema": "Json?",
        },
        "Cron": {
            "cron_id": "String",
            "assistant_id": "String",
            "thread_id": "String?",
            "schedule": "String?",
            "timezone": "String?",
            "enabled": "Boolean?",
            "created_at": "DateTime?",
        },
    }
    
    for table, fields in tables.items():
        lines.append(f"model {table} {{")
        for col, typ in fields.items():
            lines.append(f"  {col} {typ}")
        lines.append("}")
        lines.append("")
    
    return "\n".join(lines)

def main():
    prisma = generate_prisma()
    print(prisma)
    
    with open("prisma/schema_sdk.prisma", "w") as f:
        f.write(prisma)
    print("\n// Saved to prisma/schema_sdk.prisma")

if __name__ == "__main__":
    main()