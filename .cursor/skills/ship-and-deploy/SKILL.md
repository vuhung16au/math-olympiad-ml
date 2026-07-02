---
name: ship-and-deploy
description: >-
  Commit and push changes to GitHub main, then deploy HSC Math Hub to Cloudflare.
  Use when the user asks to ship, publish, commit and push, push to main, deploy,
  deploy to Cloudflare, or run the release workflow for this repo.
---

# Ship and Deploy (math-olympiad-ml)

Standard two-step release workflow for this repository:

1. **Git** — commit and push to `main`
2. **Deploy** — `make deploy` in `HSC-Viewer/` (Cloudflare via OpenNext)

Run both steps unless the user asks for only one.

## Step 1: Commit and push to main

### Preflight

```bash
git branch --show-current
git status
git diff
git diff --staged
git log -5 --oneline
```

- Confirm the user wants to commit (this skill implies yes).
- If not on `main`, switch to `main` or ask before pushing elsewhere.
- Do **not** commit `.env`, credentials, or other secrets.
- Do **not** update git config, force-push `main`, or skip hooks.

### Stage and commit

Stage only files that belong to the change. Draft a 1–2 sentence commit message focused on **why**, matching recent repo style (lowercase, concise).

```bash
git add <paths>
git commit -m "$(cat <<'EOF'
Your commit message here.

EOF
)"
git status
```

If a pre-commit hook modifies files, fix issues and create a **new** commit (do not amend unless all amend rules are met).

### Push

```bash
git push origin main
```

Requires `git_write` and `network` (or `all`) permissions.

## Step 2: Deploy to Cloudflare

Deploy runs from **HSC-Viewer**, not the repo root:

```bash
cd HSC-Viewer && make deploy
```

This runs `bun run deploy` → OpenNext Cloudflare build + deploy.

Requires `network` or `all` permissions. Cloudflare/Wrangler auth must already be configured on the machine.

### Verify

- Confirm the command exits 0.
- Report the deploy URL if printed (production site: https://vumaths.com/).

## Failure handling

| Failure | Action |
|---------|--------|
| Nothing to commit | Skip Step 1; proceed to deploy if requested |
| Push rejected (behind remote) | `git pull --rebase origin main`, resolve conflicts, push again |
| Deploy build error | Fix the error, recommit if needed, redeploy |
| Hook failure | Fix hook issues, new commit, do not amend failed commit |

## Quick reference

```bash
# Full workflow (from repo root)
git add … && git commit -m "$(cat <<'EOF'
message

EOF
)" && git push origin main && cd HSC-Viewer && make deploy
```

Only run the one-liner when changes are already reviewed and staging is intentional.
