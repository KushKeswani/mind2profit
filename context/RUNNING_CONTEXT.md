# Running Context (Living Log)

This file is the active handoff log.  
Reference docs:
- `context/PROJECT_BRIEF.md` - goals, scope, attempts, risks, roadmap
- `context/CODEBASE_BREAKDOWN.md` - technical ownership map by folder/file

---

## Current Snapshot
- Repo: `mind2profit-clean`
- Branch: `main` (tracking `origin/main`)
- Working tree was already dirty before this context pass (frontend + backend feature edits in progress).
- New addition in this pass: context documentation scaffold for faster AI/human handoffs.

## What Was Done In This Context Pass
- Read project docs and setup sources:
  - root `README.md`
  - `backend/README.md`
  - frontend `WEBSITE/mind2profit-publish-main/README.md`
- Read key runtime/config files:
  - `backend/main.py`, `backend/supabase_api.py`, `backend/beta_application_api.py`
  - `backend/env_template.txt`, frontend `env.example`
  - frontend app/auth/layout/psych storage core files
- Reviewed recent commit history to infer product direction and prior attempts.
- Created:
  - `context/PROJECT_BRIEF.md`
  - `context/CODEBASE_BREAKDOWN.md`
  - this file

## Active Direction
- Product has moved from pure backtesting emphasis toward:
  - acquisition funnel + waitlist/launch operations
  - authenticated trader workspace
  - behavior/discipline-focused psychology workflows
- Backend is currently the densest integration point and highest operational risk due to external API and email dependencies.

## Known Immediate Risks
- Backend endpoint surface is broad and lightly protected.
- Mixed persistence model (Supabase + local files) may create source-of-truth drift.
- Local secret/state artifacts in backend increase accidental leakage risk if not controlled.
- Root documentation path references are partially outdated.

## Next Milestones (Near-Term)
1. Harden backend auth for sensitive operational endpoints.
2. Normalize persistence policy and reduce fallback ambiguity.
3. Clean strategy experiment artifact sprawl into a dedicated archive/workbench area.
4. Add integration-level tests for waitlist/auth/calendar/tradovate critical paths.
5. Align README and onboarding docs with actual frontend path and active scope.

## Handoff Notes For Next Agent/Human
- Start with `PROJECT_BRIEF.md` for intent and risk context.
- Then use `CODEBASE_BREAKDOWN.md` to jump directly to ownership files.
- Before making changes, run `git status` and isolate your commit to intended files only (tree is already modified in many areas).
- Treat all backend file-based fallbacks as potentially environment-specific; verify assumptions before refactoring.
