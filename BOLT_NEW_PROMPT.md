# Ready-to-Use Bolt.new Prompt

## Prompt to Build Schema.org UI

### Copy and paste this entire prompt into bolt.new:

---

```
# Build a Schema.org Visualization Platform

## Project Overview
Build a comprehensive Schema.org visualization and management platform using React + TypeScript with Next.js 14 (App Router). The platform should visualize Schema.org V30.0 type hierarchy and provide CRUD operations for all entity types.

## Tech Stack
- Next.js 14 App Router
- TypeScript (strict mode)
- @xyflow/react for type hierarchy visualization
- Tailwind CSS for styling
- shadcn/ui for components
- Zustand for state management, Zustand

## Visual Style
- Modern, clean dark theme
- Schema.org brand colors:
  - Thing: #E8F5E9
  - Action: #E3F2FD
  - CreativeWork: #FFF3E0
  - Event: #F3E5F5
  - Intangible: #E0F2F1
  - MedicalEntity: #FFEBEE
  - Organization: #E8EAF6
  - Person: #FCE4EC
  - Place: #FFF8E1
  - Product: #F1F8E9
  - StructuredValue: #ECEFF1

## Core Features

### 1. Schema.org Type Hierarchy Visualization
- Interactive graph using @xyflow/react
- Display 11 core Schema.org types from Schema.org V30.0
- Root: Thing extends to Action, CreativeWork, Event, Intangible, MedicalEntity, Organization, Person, Place, Product, StructuredValue
- Sub-types: Action → 16 categories (AchieveAction, AssessAction, ConsumeAction, ControlAction, etc.)
- Sub-types: CreativeWork → Book, Movie, Music, SoftwareApplication, WebPage, NewsArticle, etc.
- Sub-types: Organization → Corporation, LocalBusiness, Bank, Restaurant, Hotel, etc.
- Animated edges showing "extends" relationship
- Custom node components with type colors
- MiniMap for navigation
- Click node to view type details

### 2. Type Detail Panel (Slide-over)
- Show all properties for selected type
- Property: expected type, description
- Inherit chain to root (Thing)
- Linked sub-types

### 3. Entity CRUD (Database-backed)
- Create, Read, Update, Delete entities
- Support all core Schema.org types
- Form validation
- Date/time handling per Schema.org

### 4. Search & Filter
- Search by entity name
- Filter by type
- Date range filter (for Event types)
- Property-specific filters

### 5. Dashboard
- Coverage metrics: Types covered / total
- Recent entities
- Quick actions

## Data Model (SurrealDB Schema)

```
// Core Types
Thing { id, name, description, url, image, identifier }
Person: Thing { jobTitle, birthDate, address, email }
Organization: Thing { address, logo, foundingDate, founder }
Place: Thing { geo, address, openingHours }
Product: Thing { brand, sku, price, weight }
Event: Thing { startDate, endDate, location }
CreativeWork: Thing { author, datePublished, genre }
Action: Thing { actionStatus, startTime, endTime }
```

## Component Structure

```
app/
├── page.tsx                     # Dashboard
├── types/
│   └── page.tsx               # Type hierarchy view
├── entities/
│   └── [type]/
│       ├── page.tsx           # List entities
│       └── [id]/page.tsx    # Entity detail
├── search/page.tsx             # Search
├── api/
│   └── entities/route.ts      # CRUD API
├── components/
│   ├── SchemaHierarchy.tsx   # xyflow graph
│   ├── TypeDetail.tsx      # Detail panel
│   ├── EntityForm.tsx      # CRUD form
│   ├── Search.tsx         # Search component
│   └── ui/               # shadcn components
└── lib/
    ├── db.ts              # Database
    └── types.ts           # Type definitions
```

## UI Requirements

1. **Header**: Logo, navigation, dark mode toggle
2. **Sidebar**: Type categories, quick links
3. **Main Area**: xyflow graph, full-screen option
4. **Detail Panel**: Right slide-over, full properties
5. **Footer**: Schema.org link (https://schema.org/docs/full.html)

## Acceptance Criteria

1. Graph displays all 11 core types and at least 20 sub-types
2. Clicking any node shows type properties
3. Can create new entities (forms work)
4. Search returns relevant results
5. Responsive on tablet and desktop
6. Fast loading (<3s initial load)

Build this now in Next.js 14
```

---

## Alternative: Simpler Prompt (for quick prototype)

```
Build a Schema.org type hierarchy visualization in React using @xyflow/react.

Features:
- 11 core types (Thing, Action, CreativeWork, Event, Intangible, etc.)
- Animated edges
- Custom colored nodes
- Dark theme
- MiniMap

Use Next.js, TypeScript, Tailwind.
```

---

## After Initial Build - Chat to Refine

### Add CRUD
```
Add full CRUD for Schema.org entities. Include forms with validation.
Use localStorage for persistence.
```

### Add Search
```
Add search with date range filtering for Event types.
Show search results in a panel.
```

### Add Detail Panel
```
When clicking a node in the graph, show a slide-over panel with:
- Type name
- All properties with descriptions
- List of sub-types
- Link to parent type
```

---

## Deployment Commands (in Bolt.new)

```bash
# Build
npm run build

# Preview
npm run preview

# Export / Connect to Vercel
```

---

Reference: https://bolt.new | https://schema.org/docs/full.html | https://reactflow.dev
