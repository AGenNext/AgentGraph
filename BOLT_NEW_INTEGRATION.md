# Bolt.new Vibe Coding Setup

## What is Vibe Coding?

**Vibe coding** = Natural language → Working software

> "Using AI-driven tools like Bolt.new to build apps fast by directing the AI instead of typing every line yourself."

Reference: https://bolt.new

---

## Bolt.new for Schema.org Platform

### Prompt Templates

#### 1. Basic Setup
```
Create a React + TypeScript app for a Schema.org visualization platform.
- Use @xyflow/react for the type hierarchy graph
- Display 11 core Schema.org types with their sub-types
- Use a modern, dark theme

Build this in Bolt.new
```

#### 2. Full Stack
```
Build a full-stack Schema.org implementation platform with:
- Next.js frontend
- SurrealDB database
- REST API for CRUD on Schema.org entities
- React xyflow visualization of type hierarchy
- Time-based search with date filters

Use TypeScript, Tailwind CSS
```

#### 3. With Authentication
```
Create a Schema.org admin dashboard with:
- Next.js 14 App Router
- NextAuth.js authentication
- Dashboard showing type coverage metrics
- CRUD for all Schema.org types
- Graph visualization with interactive nodes
- Search with date/time filters

Include: Sign in with GitHub, protected routes, loading states
```

---

## Schema.org Prompt Components

### Component 1: Type Hierarchy Graph
```
Component: SchemaOrgHierarchy
- 11 core types as nodes (Thing at root)
- Animated edges showing extends relationship
- Click node to show type properties
- MiniMap for navigation
- Use custom node styling with Schema.org colors
```

### Component 2: Type Detail Panel
```
Component: SchemaTypeDetail
- Shows all properties for selected type
- Property name, expected type, description
- Links to sub-types
- Links to parent type
```

### Component 3: Search Component
```
Component: SchemaSearch
- Search by type name
- Filter by properties
- Date range filter (startDate, endDate for Events)
- Results with highlighting
```

### Component 4: CRUD Table
```
Component: SchemaCRUDTable
- List all entities of a type
- Edit/Delete actions per row
- Add new entity form
- Pagination
```

---

## Bolt.new Features We Need

| Feature | Bolt.new Support | Our Implementation |
|---------|-----------------|-----------------|
| **Database** | Document/graph database | SurrealDB |
| **Auth** | NextAuth, Clerk | NextAuth |
| **API** | API Routes | Route Handlers |
| **Hosting** | Auto-deploy | Vercel |
| **AI Agents** | Yes | Prompt engineering |

---

## How to Use Bolt.new

### Step 1: Go to bolt.new
```
https://bolt.new
```

### Step 2: Describe Your Intent
```
"I want to build a Schema.org visualization platform with:
- React xyflow for type hierarchy
- TypeScript throughout
- Clean modern UI
- All 11 core Schema.org types"
```

### Step 3: Iterate with Chat
```
- "Add a detail panel when clicking on types"
- "Add time-based search for Event types"
- "Add CRUD for all entity types"
```

### Step 4: Export
```
- Connect GitHub repository
- Automatic deployment
```

---

## Alternative: Cursor (Similar Vibe Coding)

### Cursor Features
- **Cmd+K**: AI code generation
- **Cmd+L**: Chat with context
- **Cmd+K**: Edit in place
- **Tab**: Autocomplete with AI

### Schema.org Cursor Prompts
```
# Generate Schema.org hierarchy in Cursor

Create a React xyflow component that:
1. Shows Schema.org type hierarchy
2. 11 core types → 100+ sub-types
3. Animated edges
4. Click to see properties

Use TypeScript, custom node components
```

---

## Tools Comparison

| Tool | Best For | Price | Our Choice |
|------|---------|-------|-----------|
| **Bolt.new** | Full-stack, fast | Free/Pro | ✅ |
| **Cursor** | IDE replacement | Free/Pro | ✅ |
| **v0** | UI only | Free | ⚠️ |
| **Lovable** | No-code | Free | ⚠️ |
| **Replit Agent** | Full-stack | $20/mo | ❌ |

---

## Implementation Plan

### Phase 1: Basic Visualizer
```
1. Go to bolt.new
2. Paste: "React xyflow Schema.org type hierarchy"
3. Refine with chat
4. Deploy
```

### Phase 2: Full Platform
```
1. Add database schema
2. Add API routes
3. Add authentication
4. Add CRUD
5. Deploy
```

### Phase 3: Production
```
1. Add tests
2. Add CI/CD
3. Add monitoring
4. Launch
```

---

Reference: https://bolt.new | https://cursor.sh
