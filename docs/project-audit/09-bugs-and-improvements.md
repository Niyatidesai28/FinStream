# Findings and repair evidence

Baseline references below point to the original commit; repaired files may shift lines.

| ID / severity | Evidence and reproduction | Root cause / observed vs expected | Resolution |
|---|---|---|---|
| F1 Medium | routes/alerts.py:14–16; POST UNKNOWN or empty symbol | returned 201 for alerts that can never fire; should reject | supported-symbol validation; two previously failing tests now pass |
| F2 High | models/schemas.py:19; POST target_price='Infinity' | gt=0 permits infinity; stored alert causes JSON serialization failure | allow_inf_nan=False; regression now returns 422 without storage |
| F3 Medium | frontend/src/api/api.js:25; server returns detail array | Error coerced array to [object Object] | extract Pydantic messages; browser test verifies readable text and rollback |
| F4 Low | AlertPanel.jsx form controls | missing accessible names, negative numbers pass local JS check | labels, min/required and finite-positive JS check; browser exercised controls |
| F5 Medium | routes/alerts.py synchronous handlers + alert_service.py:43 | worker-thread writes can overlap dict iteration on event loop | async handlers keep these short operations on one event loop; not a distributed lock |
| F6 High | dependency audit | old Starlette and Vite/esbuild have published advisories | compatible npm transitive updates applied; major framework upgrades deferred for separate review |
| F7 Medium | App.jsx:66–99 | reconnect sends prices but does not refetch alert state; triggers while away are lost | documented; needs snapshot/event replay semantics |
| F8 Medium | App.jsx:116–130 | fetch failures swallowed; late response can overwrite fresher stream state | documented; add independent loading/error state and timestamp merge |
| F9 Medium | alert_service.py:17 and websocket_manager.py:27 | unbounded shared alerts, serial sends, no auth | documented demo limits; user/session policy and retention require product decisions |
| F10 Low | core/config.py:7–9; .env.example | unused backend URLs/secret imply nonexistent integration/security | documented; use frontend VITE_ variables; no automatic dotenv loading |

Other risks: raw JSON.parse can throw; no server history; chart data duplicated by
initial streams; temporary alert IDs use Date.now; events can arrive before POST response.
No SQL injection surface exists because there is no SQL. These findings do not establish
production security. Avoid inventing a database simply to make the resume claim true.
