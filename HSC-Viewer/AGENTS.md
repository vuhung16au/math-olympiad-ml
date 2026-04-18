<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# HSC Math Hub — Agent Policies & Coding Instructions

This file is read automatically by AI coding agents (GitHub Copilot, Codex, Claude, etc.) before making any changes to this codebase. Follow every policy below. For detailed guidance on each topic, refer to the linked policy file.

## Stack

- **Framework:** Next.js App Router (see note above — read the local docs first)
- **Language:** TypeScript, React 19
- **Styling:** Tailwind CSS + `styles/variables.css` CSS custom properties
- **PDF rendering:** `react-pdf` (client-side only)
- **Package manager:** Bun
- **Deployment:** Vercel
- **Testing:** Playwright e2e (no Jest, no unit tests)

## Policies

| Topic | Policy file | Summary |
|---|---|---|
| Responsiveness | [docs/agents/responsiveness.md](docs/agents/responsiveness.md) | Code must work across all screen sizes |
| Mobile-first | [docs/agents/mobile-first.md](docs/agents/mobile-first.md) | Prioritize mobile UX in all decisions |
| Colors | [docs/agents/colors.md](docs/agents/colors.md) | Use only the defined CSS custom properties |
| Accessibility | [docs/agents/accessibility.md](docs/agents/accessibility.md) | WCAG 2.1 AA, keyboard nav, theme modes |
| Keyboard shortcuts | [docs/agents/shortcuts.md](docs/agents/shortcuts.md) | All power-user shortcuts must be implemented |
| Interaction guidelines | [docs/agents/interaction-guidelines.md](docs/agents/interaction-guidelines.md) | Tooltips, controls, feedback patterns |
| Error handling | [docs/agents/error-handling.md](docs/agents/error-handling.md) | Friendly messages, auto-retry up to 3× |
| Security | [docs/agents/security.md](docs/agents/security.md) | XSS, iframe sandboxing, CSP, URL validation |
| Cookies | [docs/agents/cookies.md](docs/agents/cookies.md) | Allowed data, expiry, privacy rules |
| Performance | [docs/agents/performance.md](docs/agents/performance.md) | Budget targets agents must not regress |
| Offline/caching | [docs/agents/offline-caching.md](docs/agents/offline-caching.md) | Service worker strategy |
| Testing | [docs/agents/testing.md](docs/agents/testing.md) | Playwright e2e requirements for new features |
| Coding conventions | [docs/agents/coding-conventions.md](docs/agents/coding-conventions.md) | Naming, TypeScript rules, import order |
| Architecture | [docs/agents/architecture.md](docs/agents/architecture.md) | File placement, data flow, component responsibilities |
| Libraries | [docs/agents/libraries.md](docs/agents/libraries.md) | Approved deps, disallowed packages, how to add a dep |
| State management | [docs/agents/state-management.md](docs/agents/state-management.md) | useState vs cookies vs URL — where each state lives |
| Analytics | [docs/agents/analytics.md](docs/agents/analytics.md) | Event wrappers, PII rules, how to add a new event |

## Quick rules (must be followed without exception)

1. **Never introduce new color values.** Use only the variables defined in `styles/variables.css`.
2. **Every interactive element must have a `title` or `aria-label` tooltip.**
3. **All PDF load failures must retry up to 3 times before showing an error state.**
4. **Never store PII in cookies or localStorage.**
5. **Validate every user-supplied URL before fetching it.**
6. **New features require Playwright e2e tests before the PR is considered complete.**
7. **Do not regress performance budgets** (see [docs/agents/performance.md](docs/agents/performance.md)).
8. **Read `node_modules/next/dist/docs/` before writing any Next.js code.**
