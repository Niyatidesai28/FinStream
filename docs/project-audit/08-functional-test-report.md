# Executed verification — 26 October 2026

| Check | Result | Evidence / scope |
|---|---|---|
| Dependency setup | PASS after environment repair | npm ci; managed Python 3.12 + uv; host Python expat broken |
| Baseline regression suite | FAIL as expected | 3 failed, 10 passed: unknown/empty symbols and Infinity |
| Repaired backend suite | PASS | `python -m pytest backend/tests -q`: 13 passed; actual FastAPI app in TestClient |
| Frontend production build | PASS | npm run build, 836 modules; ~534KB JS chunk warning |
| Backend startup | PASS | Uvicorn loopback :8000 startup complete |
| Browser primary workflow | PASS | tests/browser_smoke.py: real HTTP POST 201, real socket, visible triggered alert |
| Selector/chart/dismissal | PASS | browser assertions for four cards, MSFT chart, line SVG, notification click |
| 422 UI rollback | PASS, mocked response | injected FastAPI-shaped error; readable message and no leftover optimistic item |
| Mobile layout | PASS, limited | 390x844 viewport; document width <= viewport and create control visible |
| CORS | PASS | configured localhost origin preflight test |
| One-time inclusive thresholds | PASS | above/below equality plus second-call empty result |
| Dead-client pruning | PASS with fake sockets | one send throws, healthy client still receives |
| SQL persistence | BLOCKED / absent | no SQL implementation to connect or test |
| Real market integration | BLOCKED / absent | source is random simulation, no credentials required |
| Dependency security | FAIL / outstanding | npm: remaining Vite/esbuild advisories; Python: Starlette advisories |
| Reconnection delivery semantics | PARTIAL | retry implementation inspected; no missed-event replay guarantee |
| Accessibility | PARTIAL | labels added and native controls tested; no exhaustive assistive-tech audit |
| Lint/type checks | NOT TESTED | no configured linter/typechecker; build and Python compile checks used |
| Load/soak/multi-worker | NOT TESTED | no production-scale reliability claim |

Commands from repository root:
```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-dev.txt
.venv/bin/python -m pytest backend/tests -q
.venv/bin/python -m compileall -q backend
# separate terminals
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
cd frontend && npm ci && npm run dev -- --host 127.0.0.1
# root; install optional playwright==1.64.1 first
.venv/bin/python tests/browser_smoke.py
```
Build: `(cd frontend && npm run build)`. Browser script uses installed macOS Google Chrome;
change executable_path for another system. It creates synthetic in-memory alerts and is
intended only for a disposable local server. No production data/services were contacted.
The app has no persistent store, so this is end-to-end for the actual in-memory product.
