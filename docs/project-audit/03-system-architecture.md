# Architecture and flows

These Mermaid diagrams describe this repository only. Database/authentication/ML diagrams
are inapplicable: those subsystems do not exist.

```mermaid
flowchart LR
  browser["React App"] -->|"GET stocks / alerts; POST alerts"| routes["FastAPI routes"]
  routes --> prices["PriceGenerator dictionary"]
  routes --> alerts["AlertService dictionary"]
  loop["main.py lifespan: every 2 seconds"] --> prices
  prices --> alerts
  alerts --> manager["WebSocketManager"]
  prices --> manager
  manager -->|"price_update JSON"| browser
```

```mermaid
flowchart TD
  app["App: shared state"] --> nav["Navbar -> ConnectionStatus"]
  app --> grid["StockGrid -> StockCard"]
  app --> chart["LiveChart -> Recharts"]
  app --> panel["AlertPanel: form and notifications"]
  panel -->|"onCreateAlert"| api["api.js fetch"]
  grid -->|"onSelect"| app
```

```mermaid
sequenceDiagram
  participant U as User
  participant R as React App
  participant A as FastAPI routes
  participant S as AlertService
  participant B as Broadcast loop
  U->>R: Open page
  R->>A: GET stocks and alerts
  A-->>R: JSON snapshots
  R->>A: WebSocket upgrade
  A-->>R: Initial price_update
  U->>R: Submit target
  R->>A: POST alerts
  A->>S: Validate and create UUID alert
  A-->>R: 201 Alert
  B->>S: Check next price tick
  S-->>B: Newly triggered alerts only
  B-->>R: price_update over WebSocket
  R-->>U: Chart, badge and notification
```

```mermaid
flowchart TD
  submit["Form submit"] --> local["Finite positive price?"]
  local -->|"No"| formError["Accessible form error"]
  local -->|"Yes"| optimistic["Temporary alert in React state"]
  optimistic --> request["POST alerts"]
  request --> valid["Pydantic + supported symbol"]
  valid -->|"Invalid"| error["422 JSON detail"]
  error --> rollback["Remove temporary alert; show message"]
  valid -->|"Valid"| stored["In-memory Alert"]
  stored --> success["201 replaces temporary alert"]
```

```mermaid
flowchart LR
  closed["WebSocket close"] --> disconnected["Disconnected badge"]
  disconnected --> delay["2 second timer"]
  delay --> reconnect["Create new WebSocket"]
  reconnect --> snapshot["Fresh prices; no alert-event replay"]
```

Backend layering is routes -> services -> Pydantic response serialization. There is no
repository/DAO layer. `main.py:19` owns the scheduler. `App.jsx:25` appends each message
to a per-symbol array and keeps the last 40 points. The initial REST and WS requests run
independently; late REST responses can temporarily overwrite fresher state. Reconnection
restores prices but does not refresh alerts, so missed notifications are not durable.
