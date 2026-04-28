# Mind2Profit Project Brief

## End Goal
- Ship a production-ready trading platform that combines:
  - public acquisition pages (`/`, `/beta`, `/coming-soon`, `/upgrade`)
  - authenticated member workspace (`/dashboard`, `/settings`)
  - behavior-first trading psychology flows (`/live`, `/journal`, `/scripts`, `/stats`, `/learn`)
  - backend APIs for market/macro data, waitlist capture, beta intake, journaling, coaching, and broker connectivity

## Current Scope (as of this handoff)
- Frontend is a Vite + React + TypeScript app in `WEBSITE/mind2profit-publish-main`.
- Backend is FastAPI in `backend/main.py` with multiple feature groups mounted under `/api`.
- Auth is Supabase-backed on frontend (`src/lib/supabase.ts`, `src/contexts/AuthContext.tsx`).
- Growth funnel + launch sequencing are active:
  - waitlist submit + admin retrieval
  - launch announcement email blast endpoint
  - coming soon + upgrade + landing flows
- Psychology system is actively integrated and localStorage-backed for now (`psych_app_state_v1`).
- Tradovate connection endpoints exist (credentials, token, OAuth URL, status/sync/disconnect, bypass test mode).

## What Has Already Been Tried (inferred from repo + git history)
- Product positioning pivoted multiple times:
  - older emphasis on manual backtesting was removed
  - educational/trader-psychology focus was added
  - repeated landing/launch date and copy revisions
- Deployment hardening attempts:
  - backend deployment docs and Railway startup dependency fixes were added recently
  - frontend API URL moved to environment variable strategy
- Data-source iteration:
  - macro data now prefers Massive API with FRED fallback, plus Trading Economics calendar range merge
- Strategy experimentation happened heavily in backend:
  - many timestamped `strategy_*.py` files indicate iterative generated/tested strategy workflows
- Persistence strategy is mixed:
  - Supabase is primary for waitlist + beta applications
  - file fallbacks exist for resilience/dev continuity (`beta_applications.json`, `journal_entries.json`, `tradovate_connection.json`)

## Architecture And Runtime Flow
- Frontend runtime:
  - `src/main.tsx` boots React app
  - `src/App.tsx` composes providers (React Query, Auth, Notification, Router)
  - protected routes are guarded in `src/components/ProtectedRoute.tsx`
  - `/dashboard` renders `TraderOSLayout` (sidebar + module-based content)
- Auth/runtime state:
  - Supabase session hydration in `AuthContext`
  - auth + plan + profile metadata drive route gating and settings fields
- Backend runtime:
  - FastAPI app in `backend/main.py`
  - CORS open for local dev
  - routes combine direct handlers plus mounted routers (`strategy_api`, `beta_application_api`)
  - scheduler thread optionally starts for daily journal reminder emails
- Integration flow:
  - frontend uses `VITE_API_URL` for backend requests
  - backend relies on env keys for Supabase, Massive/FRED/TradingEconomics, OpenAI, SMTP, Tradovate

## Known Risks / Failure Modes
- **Security risk:** CORS is wildcard and several endpoints rely only on env presence; no hardened auth layer for backend admin-like actions.
- **Data consistency risk:** dual persistence (Supabase + local file fallback) can split source of truth.
- **Sensitive local artifacts:** untracked local JSON credential/state files can leak or diverge across environments.
- **Reliability risk:** many external APIs (Massive, FRED, TradingEconomics, OpenAI, Tradovate, SMTP) create cascading failure surface.
- **Codebase drift:** large set of generated strategy scripts in `backend/` increases maintenance noise and onboarding friction.
- **Frontend/backed path drift:** root `README.md` still references `mind2profit-companion-main`, while actual active frontend path is `mind2profit-publish-main`.

## Practical Onboarding Checklist (AI or Human)
1. Confirm repo root and branch; inspect existing dirty changes before touching code.
2. Backend setup:
   - `cd backend`
   - create/activate venv
   - `pip install -r requirements.txt`
   - copy `env_template.txt` to `.env` and fill keys
   - run `uvicorn main:app --reload`
3. Frontend setup:
   - `cd WEBSITE/mind2profit-publish-main`
   - `npm install`
   - copy `env.example` to `.env` with `VITE_API_URL` + Supabase vars
   - run `npm run dev`
4. Smoke test:
   - `GET /` and `GET /api/economic-data`
   - load landing page + sign-in page + protected `/dashboard`
   - verify waitlist form path and submission handling
5. Validate secrets boundaries:
   - ensure `.env` and local credential JSON files remain uncommitted
6. Decide canonical persistence path:
   - keep file fallback only for local dev or remove for prod consistency

## Immediate Next Milestones
- Standardize environment and docs (fix stale path references and onboarding drift).
- Add backend auth/authorization for sensitive endpoints (waitlist export, email blast, broker control).
- Consolidate persistence and define source-of-truth policy (Supabase-first with explicit local-dev mode).
- Tame backend strategy script sprawl (archive or move generated artifacts into a dedicated subfolder).
- Add integration tests for critical user journeys:
  - waitlist submit
  - auth + protected route behavior
  - macro calendar API with fallback paths
  - Tradovate connect/status/sync lifecycle
