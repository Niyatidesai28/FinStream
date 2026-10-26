# Repository map

See SOURCE-INDEX.md for the original tracked-file list. There was no README or CI.

| Path | Responsibility and important symbols |
|---|---|
| backend/main.py:17 | lifespan starts/cancels the broadcast_loop task; app/router/CORS setup |
| backend/core/config.py:5 | Settings reads APP_NAME and CORS_ORIGINS; API_BASE_URL, WS_URL and SECRET_KEY are unused backend settings |
| backend/models/schemas.py:7 | StockPrice, AlertCreate, Alert, TriggeredAlert, PriceUpdateMessage are Pydantic contracts, not database models |
| backend/routes/stocks.py:10 | get_stocks REST snapshot and websocket_prices initial snapshot/receive loop |
| backend/routes/alerts.py:10 | list/create alert endpoints and supported-symbol check |
| backend/services/price_generator.py:16 | PriceGenerator owns reference/current dictionaries, tick/snapshot/symbols |
| backend/services/alert_service.py:8 | AlertService owns UUID-keyed alerts and inclusive threshold evaluation |
| backend/services/websocket_manager.py:7 | WebSocketManager accepts, sends and broadcasts; prunes failed clients |
| frontend/src/main.jsx:6 | mounts App under React StrictMode |
| frontend/src/App.jsx:13 | shared React state, REST bootstrapping, WS lifecycle, optimistic create and notifications |
| frontend/src/api/api.js:1 | environment-based URLs and fetch wrappers |
| frontend/src/components/ | seven small presentation/form components explained in 04 |
| frontend/src/App.css | grid, cards, form, connection/alert states; 960px/480px breakpoints |
| frontend/vite.config.js | React compilation plugin |
| frontend/package.json / package-lock.json | declared dependencies and resolved versions |
| frontend/index.html | root element and browser entry module |
| .env.example | example names only; backend does not automatically load dotenv |
| .gitignore | excludes environments/build/dependency directories |
| backend/tests/ | audit-added unit/API/WebSocket regression suite |
| tests/browser_smoke.py | audit-added Chrome end-to-end smoke plus explicitly mocked error case |

Empty __init__.py files mark Python packages. No generated dependencies are explained
as application logic. Duplicated CSS import is harmless. Hardcoded SYMBOLS in AlertPanel
can drift from backend INITIAL_PRICES. Do not remove SECRET_KEY assuming it secures anything:
it currently has no consumer at all.
