# Codebase Breakdown

## Repo-Level Map
- `README.md`
  - high-level setup docs (partially stale; references `mind2profit-companion-main`)
- `UPDATE_WORKFLOW.md`, `BACKEND_DEPLOYMENT.md`, `HEROKU_DEPLOYMENT.md`
  - deployment/update process notes
- `backend/`
  - FastAPI application, integrations, strategy generation/testing utilities
- `WEBSITE/mind2profit-publish-main/`
  - Vite React frontend (public marketing + authenticated trader app + psych system)
- `context/`
  - handoff/context docs for ongoing execution

## Backend (`backend/`)

### Core API and App Wiring
- `main.py`
  - FastAPI app bootstrap, CORS, env load
  - includes routers from `strategy_api.py` and `beta_application_api.py`
  - primary endpoints:
    - market/backtest and macro data routes
    - economic calendar range merge logic (TradingEconomics + Massive)
    - waitlist create/list and launch announcement email send
    - journal CRUD + AI trade coaching
    - Tradovate connect/token/oauth/status/sync/disconnect/bypass
    - daily reminder email scheduler startup

### Data/Service Adapters
- `supabase_api.py`
  - Supabase client setup and CRUD helpers for:
    - beta applications
    - waitlist records
  - graceful fallback behavior when Supabase config/dependency is missing
- `beta_application_api.py`
  - beta application submission/list/detail/delete endpoints
  - email notification send on submission
  - file fallback (`beta_applications.json`) when Supabase unavailable

### Strategy/Experiment Layer
- `strategy_api.py`, `strategy_chatbot.py`, `strategy_templates.py`, `rsi_backtest.py`
  - strategy-related API and utility logic
- many timestamped `strategy_*.py` files
  - generated/iterative strategy experiment outputs, currently co-located with production API code

### Tests/Utilities/Artifacts
- `test_server.py`, `test_supabase.py`
  - lightweight test scripts
- export/compare scripts (`export_trades_*`, `compare_trades.py`)
- local state/artifact files (some untracked during current branch work):
  - `journal_entries.json`
  - `tradovate_connection.json`
  - `supabase_schema.sql`

### Backend Runtime Dependencies
- `requirements.txt`
  - `fastapi`, `uvicorn`, `yfinance`, `requests`, `python-dotenv`, `supabase`, `pandas`, `ta`

## Frontend (`WEBSITE/mind2profit-publish-main/`)

### App Composition and Routing
- `src/main.tsx`
  - app entrypoint
- `src/App.tsx`
  - provider stack: React Query, Auth, Notification, Router, toasts/tooltips
  - route groups:
    - public: landing/coming soon/upgrade/about/beta/science hypnosis/sign in/sign up/learn
    - protected: dashboard/settings
- `src/components/ProtectedRoute.tsx`
  - blocks unauthenticated users (and optionally unsubscribed users)

### Auth and User State
- `src/lib/supabase.ts`
  - Supabase client initialization and env guard
- `src/contexts/AuthContext.tsx`
  - session hydration, login/signup/reset/logout
  - metadata-based subscription and preferences modeling
  - billing metadata update methods
- `src/contexts/NotificationContext.tsx`
  - in-app notification preferences/state orchestration

### Dashboard/Trader Workspace
- `src/pages/Index.tsx`
  - authenticated dashboard root
- `src/components/TraderOSLayout.tsx`
  - shell layout (top bar + sidebar + module area)
- `src/components/layout/TopBar.tsx`, `MainContent.tsx`
  - module host and page-level control surface
- `src/components/modules/*`
  - functional trader modules (dashboard, calendar, journal, hypnosis, partner, learn, AI chat, etc.)

### Trading Psychology System
- `PSYCH_SYSTEM_README.md`
  - design/behavior contract and flow definitions
- `src/pages/LiveTradingPage.tsx`
  - session gating + live mode + stop-trading enforcement
- `src/pages/PsychJournalPage.tsx`, `ScriptsPage.tsx`, `PsychStatsPage.tsx`, `LearnPage.tsx`
  - journaling, script management, discipline metrics, lessons
- `src/lib/storage.ts`, `src/lib/types.ts`, `src/lib/seedScripts.ts`
  - localStorage persistence model (`psych_app_state_v1`), domain types, default script seeds
- `src/components/psych/*`
  - psych-specific reusable UI controls

### Design System and Build
- `src/components/ui/*`
  - shadcn-style UI primitives and wrappers
- `package.json`
  - Vite scripts (`dev`, `build`, `lint`, `preview`)
  - React + TypeScript + Tailwind + Radix + Supabase + React Query stack
- `vite.config.ts`, `tailwind.config.ts`
  - frontend bundler and styling configuration
- `env.example`
  - frontend runtime config contract (`VITE_API_URL`, Supabase vars)

## Runtime Request/Response Flow (Typical)
- Browser loads React app -> routes user to public or protected views.
- Protected flow checks Supabase session in `AuthContext`.
- Frontend calls backend API (`VITE_API_URL`) for dynamic features:
  - waitlist, journal, macro data, broker connectivity, AI coaching.
- Backend handlers in `main.py` fan out to:
  - external APIs (Massive/FRED/TradingEconomics/OpenAI/Tradovate),
  - Supabase via `supabase_api.py`,
  - local file fallback when configured services unavailable.
- Response returns to frontend for UI rendering and notifications.

## Areas With Highest Change Velocity
- `src/pages/LandingPage.tsx` and public marketing routes.
- `backend/main.py` (multi-domain endpoint concentration).
- psychology pages + local state utilities.
- auth context and protected route behavior.
