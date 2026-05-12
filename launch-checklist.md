# Enterprise SaaS Website Launch Prompt

## Project: AGenNext Enterprise SaaS Website

---

## Design Requirements

### Tech Stack
- Next.js 14+ (App Router)
- React 18+
- shadcn/ui
- TypeScript
- Tailwind CSS

### Design System: IBM Plex Sans

**Color Palette:**
- Background: `#000000` (Pure Black)
- Surface: `#0A0A0A` (Elevated Black)
- Border: `#262626` (Subtle Gray)
- Primary Text: `#FFFFFF` (Pure White)
- Secondary Text: `#A3A3A3` (IBM Gray)
- Accent: `#FFFFFF` (White only)

**Typography:**
- Primary Font: IBM Plex Sans
- Monospace: IBM Plex Mono
- H1: 48px/700
- H2: 36px/600
- H3: 24px/600
- Body: 16px/400
- Small: 14px/400

---

## Pre-Deployment Checklist

### ✅ Design System
- [ ] IBM Plex Sans font loaded (WOFF2)
- [ ] shadcn/ui configured with custom theme
- [ ] Color tokens defined in Tailwind config
- [ ] Component variants (default, secondary, outline, ghost)
- [ ] Dark mode enforced (no light toggle)

### ✅ Pages
- [ ] Landing page (hero, features, pricing, CTA)
- [ ] Documentation page
- [ ] API reference page
- [ ] Pricing page (3 tiers)
- [ ] About page
- [ ] Contact page

### ✅ Components
- [ ] Button (4 variants)
- [ ] Input (with labels)
- [ ] Select/Dropdown
- [ ] Card (with hover states)
- [ ] Tabs
- [ ] Accordion
- [ ] Table
- [ ] Badge
- [ ] Avatar
- [ ] Dialog/Modal

### ✅ Functionality
- [ ] Responsive (320px to 2560px)
- [ ] Navigation works
- [ ] Mobile menu works
- [ ] All links functional
- [ ] Forms validate
- [ ] Loading states
- [ ] Error states

### ✅ Performance
- [ ] Lighthouse Performance > 90
- [ ] Lighthouse Accessibility > 90
- [ ] Lighthouse Best Practices > 90
- [ ] Lighthouse SEO > 90
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s

---

## Self-Evaluation Criteria

### Design (25 points)
| Criteria | Score | Notes |
|----------|-------|-------|
| IBM font rendering correct | /5 | Verify Plex Sans displays |
| Black/white only colors | /5 | No other colors allowed |
| shadcn components styled | /5 | Consistent with theme |
| Responsive works | /5 | All breakpoints |
| No layout shifts | /5 | CLS < 0.1 |

### Functionality (25 points)
| Criteria | Score | Notes |
|----------|-------|-------|
| All pages load | /5 | 200 status |
| Navigation works | /5 | No broken links |
| Forms work | /5 | Validation passes |
| Mobile menu works | /5 | Touch targets 44px+ |
| No JS errors | /5 | Console clean |

### Performance (25 points)
| Criteria | Score | Notes |
|----------|-------|-------|
| Lighthouse > 90 | /10 | Performance |
| FCP < 1.5s | /5 | First Contentful Paint |
| TTI < 3s | /5 | Time to Interactive |
| Bundle < 200KB | /5 | gzipped |

### Accessibility (25 points)
| Criteria | Score | Notes |
|----------|-------|-------|
| Alt text present | /5 | All images |
| Label present | /5 | All inputs |
| Focus visible | /5 | Keyboard nav |
| ARIA correct | /5 | Screen reader |
| Color contrast | /5 | 7:1 ratio |

**Total: ___/100** (Pass: 80+)

---

## Pre-Deployment Commands

```bash
# 1. Install dependencies
npm install

# 2. Build production
npm run build

# 3. Type check
npm run type-check

# 4. Lint
npm run lint

# 5. Start local
npm run start

# 6. Test in browser
# - localhost:3000
# - Check all pages
# - Test mobile responsive
```

---

## Post-Deployment Checks

### Immediate (0-5 min)
- [ ] Site loads at production URL
- [ ] All pages return 200
- [ ] No 404 errors in console
- [ ] Assets loading (CSS/JS)
- [ ] Fonts loading

### Performance (5-15 min)
- [ ] Lighthouse score > 90
- [ ] No blocking resources
- [ ] Images optimized
- [ ] Caching headers set
- [ ] Gzip/Brotli enabled

### Functionality (15-30 min)
- [ ] Navigation works
- [ ] Forms work
- [ ] Mobile responsive
- [ ] No console errors
- [ ] Analytics tracking

### Security (30-60 min)
- [ ] No sensitive data in URL
- [ ] CSP headers set
- [ ] X-Frame-Options set
- [ ] HTTPS enforced
- [ ] No credentials exposed

---

## Final Confirmation

### Pre-Flight Checks
- [ ] All tests passing locally
- [ ] Design matches IBM spec
- [ ] No console errors
- [ ] Lighthouse > 90
- [ ] Accessibility score > 90

### Deployment Checklist
- [ ] Production build succeeds
- [ ] No TypeScript errors
- [ ] No lint errors
- [ ] All pages tested
- [ ] Forms tested
- [ ] Mobile tested

### Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Designer | | | |
| QA | | | |
| Product | | | |

---

## Launch Prompt (Copy-Paste)

```
Build an enterprise SaaS marketing website with:

## Tech Stack
- Next.js 14 (App Router)
- React 18
- shadcn/ui
- TypeScript
- Tailwind CSS

## Design System: IBM Plex
- Background: #000000 (Black)
- Surface: #0A0A0A 
- Border: #262626
- Text: #FFFFFF / #A3A3A3
- Font: IBM Plex Sans (WOFF2)
- Monospace: IBM Plex Mono

## Pages Required
1. Landing (hero, features, how-it-works, pricing, CTA, footer)
2. Documentation (sidebar, content area)
3. API Reference
4. Pricing (3 tiers)
5. About
6. Contact

## Components (shadcn/ui)
- Button (default, secondary, outline, ghost)
- Input, Select, Card
- Tabs, Accordion
- Table, Badge, Avatar
- Dialog/Modal

## Requirements
- Black/white only (no other colors)
- IBM Plex Sans font mandatory
- Mobile responsive (320px-2560px)
- Lighthouse 90+
- No light mode
- Strict accessibility

## Deployment
- GitHub Pages
- Self-contained (no external dependencies except CDN)
```

---

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SITE_URL=https://example.com
NEXT_PUBLIC_ANALYTICS_ID=
```

---

## File Structure

```
nextjs-website/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── docs/
│   │   ├── pricing/
│   │   └── contact/
│   ├── components/
│   │   ├── ui/ (shadcn)
│   │   └── main-nav.tsx
│   ├── lib/
│   │   └── utils.ts
│   └── public/
│       └── fonts/
├── components.json
├── tailwind.config.ts
├── tsconfig.json
├── next.config.js
└── package.json
```

---

## Success Criteria Summary

| Metric | Target | Actual |
|--------|--------|--------|
| Performance | 90+ | |
| Accessibility | 90+ | |
| Best Practices | 90+ | |
| SEO | 90+ | |
| First Paint | <1.5s | |
| TTI | <3s | |
| Bundle | <200KB | |
| CLP | <0.1 | |

---

## Launch Ready ✓

After completing all checks above, confirm:

- [ ] Design matches IBM spec (black/white, Plex Sans)
- [ ] All pages implemented
- [ ] shadcn/ui components styled
- [ ] Responsive works
- [ ] No console errors
- [ ] Lighthouse > 90
- [ ] Accessibility > 90
- [ ] Final sign-off obtained

**Date: ___/___/____**

**Launch Authority: ___**

---

## Emergency Rollback

```bash
# Rollback command
git revert HEAD
git push origin main
```

Reference: 
- https://ui.shadcn.com/
- https://www.ibm.com/design/language/