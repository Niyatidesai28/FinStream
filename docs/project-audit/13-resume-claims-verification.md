# Resume claim evidence

| Claim | Verdict | Source / accurate wording / likely follow-up |
|---|---|---|
| Engineered real-time financial dashboard | PARTIALLY SUPPORTED | App + PriceGenerator; say simulated stock-price dashboard; explain random walk vs exchange data |
| React integrated with FastAPI | SUPPORTED | api.js fetch + main.py routers; explain origins, JSON and state updates |
| REST APIs | SUPPORTED | GET stocks/alerts and POST alerts; explain 201 vs 422 |
| WebSockets for live streaming | SUPPORTED for local simulated feed | main.py lifespan + routes/stocks.py + App.onmessage; tested snapshot/tick/alert delivery |
| Structured visualizations | SUPPORTED | LiveChart.jsx Recharts, rolling 40-point history; explain chart props |
| Backend logic, debugging, reliability | PARTIALLY SUPPORTED | threshold evaluator and audit regressions demonstrate techniques; no production reliability evidence; learn the fixes before claiming personal debugging experience |
| SQL in reported stack | UNSUPPORTED | no database code; remove SQL from this project's stack |

Suggested wording: “Built a React/FastAPI dashboard that streams simulated stock prices
over WebSockets, visualizes rolling history with Recharts, and supports in-memory threshold
alerts through REST endpoints.” Do not say real exchange data, persistent alerts, SQL,
production scale, authentication or guaranteed delivery. Audit-added tests/fixes are new
work; they are not evidence that the original project had those properties.
