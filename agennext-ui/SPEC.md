# Agent Registry Platform - UI Specification

**Version:** 1.0  
**Last Updated:** 2026-05-08

---

## 1. SCREEN LAYOUTS

### SCREEN 1: AGENT LIST (/agents)

```
┌──────────────────────────────────────────────────┐
│ [Logo]  Agent Registry          [+ New Agent] [⚙] │
├──────────────────────────────────────────────────┤
│ [🔍 Search agents...] [Filter ▼] [Sort ▼]         │
├──────────────────────────────────────────────────┤
│  AGENT CARDS (Grid: 3 columns desktop, 1 mobile)  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │
│  │ Sales-AI  │ │ Support-AI│ │Lead-Gen-AI│  │
│  │ ───────  │ │ ────────  │ │ ──────── │  │
│  │ OpenAI   │ │ Google    │ │ LangChain│  │
│  │ gpt-4o  │ │ gemini-2  │ │ rag     │   │
│  │ ● Active │ │ ○ Inactive│ │ ● Active│  │
│  │ v2.1    │ │ v1.0     │ │ v1.2    │  │
│  │         │ │         │ │        │   │
│  │ Chat    │ │ Chat    │ │ Chat   │   │
│  │ [⋮]    │ │ [⋮]    │ │ [⋮]   │   │
│  └─────────────┘ └─────────────┘ └─────────────┘  │
├──────────────────────────────────────────────────┤
│ Showing 3 of 3 agents        [< 1 > 2 > 3 >]      │
└──────────────────────────────────────────────────┘
```

**Components:**
| Element | Type | ID | Actions |
|---------|------|-----|---------|
| Header logo | Image | logo | - |
| New Agent button | Button | btn-new | → Screen 2 |
| Settings | Icon btn | settings | → Settings |
| Search input | Text input | search | live filter |
| Filter dropdown | Select | filter-type | All/Active/Inactive |
| Sort dropdown | Select | sort | Name/Date/Provider |
| Agent card | Card | card-* | click → Detail |
| Card menu btn | Dropdown | card-menu | Edit/Clone/Delete |
| Pagination | Nav | pagination | page change |

### SCREEN 2: ADD/EDIT AGENT (/agents/new or /agents/edit/{id})

```
┌──────────────────────────────────────────────────┐
│ [+ New Agent]                      [Cancel] [Save]│
├──────────────────────────────────────────────────┤
│  ┌─ BASIC ──────────────────────────────────┐   │
│  │ Name: [_______________________________]     │   │
│  │ Description: [_______________________]   │   │
│  └──────────────────────────────────────────  │
│  ┌─ PROVIDER ───────────────────────────────┐   │
│  │ SDK: [OpenAI ▼]      [Load from cloned? ]│   │
│  │ Model: [gpt-4o ▼]                       │   │
│  │ Temperature: [━━━●━━━] 0.7            │   │
│  │ Max Tokens: [━━━●━━━] 2000              │   │
│  │ System Prompt: [_____________________]   │   │
│  └──────────────────────────────────────────  │
│  ┌─ AUTHENTICATION ────────────────────────┐   │
│  │ Auth Method: [API Key ▼]                │   │
│  │ API Key: [••••••••••••••••] [Show]    │   │
│  │ Or: [Use Environment Variable ▼]      │   │
│  └──────────────────────────────────────────  │
│  ┌─ UI INTERFACE ──────────────────────────┐   │
│  │ Chat UI: [✓ Enable]  [Chat Playground] │   │
│  │ RAG UI: [ ] Enabled                   │   │
│  │ Tools: [✓ Calculator] [✓ Search]    │   │
│  └──────────────────────────────────────────  │
│  ┌─ VERSION ───────────────────────────────┐   │
│  │ Version: v2.1 (auto)                  │   │
│  │ [ ] Mark as default                    │   │
│  └──────────────────────────────────────────  │
└──────────────────────────────────────────────────┘
```

**Components:**
| Element | Type | ID | Actions |
|---------|------|-----|---------|
| Name input | Text | input-name | validation required |
| Description | Textarea | input-desc | max 500 chars |
| SDK select | Select | select-sdk | OpenAI/Google/Microsoft/LangChain/LangGraph/Custom |
| Model select | Select | select-model | depends on SDK |
| Temperature | Slider | slider-temp | 0-2, step 0.1 |
| Max tokens | Slider | slider-tokens | 100-128000 |
| System prompt | Textarea | input-system | system instructions |
| Auth method | Select | select-auth | api_key/env/oauth |
| API key input | Password | input-key | show/hide toggle |
| Env var select | Select | select-env | from list |
| Chat UI checkbox | Checkbox | check-chat | enables chat component |
| RAG checkbox | Checkbox | check-rag | enables RAG |
| Tools multiselect | Multi | select-tools | Calculator/Search/Database etc |
| Version label | Text | label-version | auto |
| Save button | Button | btn-save | → validate → save → list |
| Cancel button | Button | btn-cancel | → confirm → list |

**Transitions:**
- New → Save → Success toast → Redirect to list
- Edit → Save → Success toast → Stay on edit
- Cancel → Confirm modal → List
- Validation error → Inline error messages

### SCREEN 3: CLONE AGENT (/agents/clone/{id})

```
┌──────────────────────────────────────────────────┐
│ Clone: Sales-AI                    [Cancel] [Clone]  │
├──────────────────────────────────────────────────┤
│  Original: Sales-AI v2.1 (OpenAI, gpt-4o)      │
│  ┌─────────────────────────────────────────┐   │
│  │ [x] Name          [x] Provider         │   │
│  │ [x] Model         [ ] Auth (new key)   │   │
│  │ [x] Temperature  [ ] System Prompt   │   │
│  │ [ ] UI Settings                       │   │
│  └─────────────────────────────────────────┘   │
│                                             │
│  New Name: [_____________________________]  │
│                                             │
│  [✓] Copy UI settings                       │
│  [ ] Create as new version                 │
└──────────────────────────────────────────────────┘
```

**Components:**
| Element | Type | ID | Actions |
|---------|------|-----|---------|
| Checkboxes list | Checkbox[] | clone-* | what to copy |
| New name input | Text | input-new-name | required |
| Copy UI checkbox | Checkbox | check-copy-ui | - |
| Version option | Radio | radio-version | new v1 / update v2 |

**Transitions:**
- Clone → Validate → Success → Redirect to cloned agent edit

### SCREEN 4: VERSION HISTORY (/agents/{id}/history)

```
┌──────────────────────────────────────────────────┐
│ ← Back    Version History - Sales-AI               │
├──────────────────────────────────────────────────┤
│                                             │
│  v3  ┌────────────────────────────────────┐   │
│  ●   │ March 2026, 2:30 PM                │   │
│ Curr │ Updated: model → gpt-4o              │   │
│      │ Updated: temperature → 0.8         │   │
│      │ [Restore] [View Config] [Compare]   │   │
│      └────────────────────────────────────┘   │
│                                             │
│  v2  ┌────────────────────────────────────┐   │
│      │ Jan 2026, 10:15 AM                 │   │
│      │ Created from v1                     │   │
│      │ [Restore] [View Config]            │   │
│      └────────────────────────────────────┘   │
│                                             │
│  v1  ┌────────────────────────────────────┐   │
│      │ Dec 2025, 4:45 PM                  │   │
│      │ Initial version                     │   │
│      │ [Restore] [View Config]             │   │
│      └────────────────────────────────────┘   │
│                                             │
│  [Export All] [Compare Selected]                  │
└──────────────────────────────────────────────────┘
```

**Components:**
| Element | Type | ID | Actions |
|---------|------|-----|---------|
| Version card | Card | version-* | - |
| Current badge | Badge | badge-current | - |
| Restore button | Button | btn-restore-* | confirm → restore |
| View config | Button | btn-view-* | show diff modal |
| Compare button | Button | btn-compare | select 2 → diff view |
| Export all | Button | btn-export | download all |

---

## 2. MOBILE LAYOUTS

```
/agents (mobile)
┌───────────────────────────┐
│ ≡  Agent Registry        [+New]│
├───────────────────────────┤
│ [🔍 Search...]          │
├───────────────────────────┤
│ ┌─────────────────────┐ │
│ │ Sales-AI        [⋮]│ │
│ │ OpenAI · gpt-4o     │ │
│ │ ● Active            │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ Support-AI     [⋮]│ │
│ │ Google · gemini-2   │ │
│ │ ● Active            │ │
│ └─────────────────────┘ │
└───────────────────────────┘

Breakpoints:
- Desktop: > 1024px (3 columns)
- Tablet: 768px-1024px (2 columns)
- Mobile: < 768px (1 column)
```

---

## 3. EMPTY STATES

```
/agents - No agents yet
┌─────────────────────────────────────┐
│                                     │
│            🤖                       │
│       No agents yet                  │
│                                     │
│   Create your first agent to         │
│   get started with AI assistance.   │
│                                     │
│      [+ Create Agent]                │
└─────────────────────────────────────┘

/agents - No search results
┌─────────────────────────────────────┐
│           🔍                        │
│     No agents found                 │
│                                     │
│   Try adjusting your search         │
│   or create a new agent.            │
│                                     │
│      [+ Create Agent]              │
└─────────────────────────────────────┘
```

---

## 4. LOADING STATES

```
Loading spinner
┌─────────────────────────────────────┐
│          ◌  Loading...              │
└─────────────────────────────────────┘

Skeleton (agent list)
┌─────────────────┐ ┌─────────────────┐
│ ████████████   │ │ ████████████   │
│ ████████        │ │ ████████        │
│ ███            │ │ ███            │
└─────────────────┘ └─────────────────┘
```

---

## 5. ERROR STATES

```
Error toast
┌─────────────────────────────────────┐
│ ⚠ Failed to save agent              │
│ Something went wrong. Please try again.│
│                          [Dismiss] │
└─────────────────────────────────────┘

Error on page
┌─────────────────────────────────────┐
│          ⚠️                         │
│    Something went wrong            │
│                                     │
│   We couldn't load this page.     │
│                                     │
│      [Try Again] [Go Back]        │
└─────────────────────────────────────┘

Form validation errors inline
Name: [________________]
       ← This field is required

API Key: [••••••••]
       ← Invalid API key
```

---

## 6. HOVER/FOCUS STATES

```css
.btn-primary {
  background: #6366f1;
}
.btn-primary:hover {
  background: #4f46e5;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}
.btn-primary:active {
  transform: translateY(0);
}
.btn-primary:focus-visible {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
}
.btn-primary:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.card:hover {
  border-color: #6366f1;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  transform: translateY(-2px);
  cursor: pointer;
}

.input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
.input:error {
  border-color: #ef4444;
}
```

---

## 7. ACCESSIBILITY (A11Y)

| Element | A11Y Requirement |
|---------|-----------------|
| All buttons | `aria-label` if no text |
| Form inputs | `aria-describedby` for errors |
| Loading | `aria-live="polite"` |
| Modals | `role="dialog"`, trap focus |
| Headings | h1 → h6 hierarchy |
| Images | `alt` text |
| Focus visible | 2px outline |

```html
<button aria-label="Create new agent">
  <Icon>+</Icon> New Agent
</button>

<button aria-label="Delete agent" aria-describedby="delete-help">
  <Icon>🗑</Icon>
</button>
<span id="delete-help" class="sr-only">
  This will permanently delete the agent
</span>
```

---

## 8. DARK MODE

```css
--bg-primary: #0f172a;
--bg-secondary: #1e293b;
--bg-card: #334155;
--text-primary: #f1f5f9;
--text-secondary: #94a3b8;
--border: #475569;
```

---

## 9. CSS DESIGN SYSTEM

**Colors:**
| Name | Value | Usage |
|------|-------|-------|
| Primary | #6366f1 | buttons, links |
| Secondary | #64748b | text muted |
| Success | #22c55e | active status |
| Error | #ef4444 | errors |
| Warning | #f59e0b | warnings |
| Background | #f8fafc | page bg |
| Card | #ffffff | card bg |
| Text | #1e293b | primary text |
| Text muted | #64748b | secondary |

**Spacing:**
| Token | Value |
|-------|-------|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 32px |

**Typography:**
- Font: Inter, system-ui
- Headings: h1=32px, h2=24px, h3=20px
- Body: 16px
- Small: 14px

---

## 10. SUMMARY

| Screen | Route | Purpose |
|--------|-------|---------|
| Agent List | /agents | View all, search, filter |
| Add/Edit | /agents/new or /agents/edit/{id} | Create or modify agent |
| Clone | /agents/clone/{id} | Duplicate existing |
| History | /agents/{id}/history | Version management |

---

*End of Spec*