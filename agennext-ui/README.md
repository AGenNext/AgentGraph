# AGenNext Platform UI

Next.js frontend for the AGenNext Enterprise agent platform.

## Structure

```
agennext-ui/
├── app/
│   ├── (dashboard)/          # Business user views
│   │   ├── page.tsx          # Task submission + agent picker
│   │   ├── approvals/        # Human-in-the-loop inbox
│   │   └── tasks/[id]/       # Individual task view
│   └── (workspace)/          # Developer views
│       ├── agents/           # Agent registry + raw AgentCards
│       └── logs/             # Task traces + SSE event log
├── components/
│   ├── AgentCard/            # simple + detailed variants
│   ├── TaskStream/           # SSE consumer, business + dev modes
│   └── ApprovalPanel/        # Human-in-the-loop UI
├── hooks/
│   └── useTaskStream.ts      # SSE hook
├── lib/
│   └── a2a-client.ts         # Backend + A2A agent API calls
└── types/
    └── a2a.ts                # A2A protocol types
```

## Setup

```bash
npm install
cp .env.example .env.local
# Set NEXT_PUBLIC_BACKEND_URL to your AGenNext Python backend
npm run dev
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_BACKEND_URL` | `http://localhost:8000` | AGenNext Python backend URL |
| `BACKEND_URL` | `http://localhost:8000` | Backend URL for Next.js rewrites |

## Backend API Contract

The UI expects these endpoints on your Python backend:

| Method | Path | Description |
|---|---|---|
| GET | `/agents` | List registered agents |
| POST | `/agents/register` | Register agent by URL (fetches AgentCard) |
| POST | `/tasks` | Submit a new task |
| GET | `/tasks` | List tasks (filterable) |
| GET | `/tasks/:id` | Get task by ID |
| POST | `/tasks/:id/cancel` | Cancel a task |
| GET | `/tasks/:id/stream` | SSE stream of task events |
| GET | `/approvals` | List pending approval requests |
| POST | `/approvals/:taskId` | Respond to an approval |

## Adding a New Page

1. Create `app/(dashboard)/your-page/page.tsx` for business users
2. Create `app/(workspace)/your-page/page.tsx` for developer view
3. Add navigation links in both nav bars

## Key Design Decisions

- **No routing layer** — user picks the agent, platform executes
- **Two modes** — same components, `mode="business"` vs `mode="developer"` prop
- **SSE-first** — `useTaskStream` hook manages EventSource lifecycle
- **A2A types** — `types/a2a.ts` mirrors the official A2A spec + AGenNext extensions
