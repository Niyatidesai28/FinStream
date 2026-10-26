# API contract

All application routes are unauthenticated. No query/path parameters exist. Base URL
for local testing: http://127.0.0.1:8000. FastAPI also exposes /docs, /redoc and /openapi.json.

| Method / route | Handler | Request | Success | Errors / test evidence |
|---|---|---|---|---|
| GET / | main.root | none | 200 message object | health test |
| GET /stocks | routes/stocks.get_stocks | none | 200 StockPrice[] | four positive prices tested |
| GET /alerts | routes/alerts.list_alerts | none | 200 Alert[] newest first | lifecycle test |
| POST /alerts | routes/alerts.create_alert | AlertCreate JSON | 201 Alert | 422 invalid body/price/condition/symbol; six negative cases tested |
| WS /ws/prices | routes/stocks.websocket_prices | upgrade, then optional incoming text | initial and periodic PriceUpdateMessage | disconnect cleanup path; no replay/authentication |

Request example:
```json
{"symbol":"AAPL","condition":"above","target_price":200}
```
Symbol is stripped/uppercased by the repaired route and must exist in PriceGenerator.
Condition is the literal above or below. Price must be finite and >0. Missing required
fields fail Pydantic validation. These checks occur before storage. Pydantic 422 detail
is an array of field errors; unsupported symbol detail is a string. UI handles both.

StockPrice: symbol, price, previous_close, change, change_percent, updated_at ISO datetime.
Alert: id UUID string, symbol, condition, target_price, triggered bool, created_at and
nullable triggered_at. TriggeredAlert additionally carries current_price.
WebSocket payload: type='price_update', stocks array, triggered_alerts array. Initial
payload has no triggered alerts. Subsequent events include newly triggered alerts only.

No database operations occur. No rate limiting, pagination, delete endpoint, ownership
check or stable persistence guarantee exists. 404 applies to unknown routes; 405 to a
known route with an unsupported method. There is no documented custom 500 recovery.
