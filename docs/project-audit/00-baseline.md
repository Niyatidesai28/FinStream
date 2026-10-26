# FinStream baseline — 26 October 2026

Repository: https://github.com/Niyatidesai28/FinStream
Default branch verified through GitHub API and origin/HEAD: `main`.
Original HEAD: `5ca6a97cdfd31562b2980e20d318bd60a11c6a84`.
Fresh clone; clean working tree; no existing user changes or audit branches.
Isolated working branch: `codex/finstream-audit`. Local main remains at baseline.
GitHub connector is read-only under a different account; GitHub CLI owner account has admin/push permission. CLI publication will be used.

Initial inventory: FastAPI backend, React/Vite/Recharts frontend, npm lockfile,
no tests, README, database driver, migrations or CI workflows.
Source prices are a random walk over four fixed symbols; no market-data provider.
Python 3.12 selected because original Pydantic pin predates host Python 3.14.
Initial virtualenv ensurepip failed in sandbox; environment setup is pending retry.
No production environment, credentials or customer data used.
