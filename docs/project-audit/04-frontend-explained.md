# Frontend walkthrough

`main.jsx` creates one React root. There is no router or multi-page navigation.
`App.jsx:14–23` owns stocks (symbol map), history (symbol -> point array), selectedSymbol,
alerts, notifications, connection status, lastUpdated and socket/timer refs. State setters
cause rerendering; refs hold mutable handles without rerendering.

| Component | Props / state / events |
|---|---|
| Navbar | status and lastUpdated; formats time; includes ConnectionStatus |
| ConnectionStatus | status selects one of three labels/classes; unknown values become disconnected |
| StockGrid | stocks map, selectedSymbol, onSelect; empty placeholder until data |
| StockCard | stock, isSelected, onSelect; native button selects symbol; displays signed change |
| LiveChart | symbol/history props; calculates rising colour; responsive Recharts line chart; empty placeholder |
| AlertPanel | alerts/callbacks/notifications props; symbol, condition, targetPrice, error, submitting local state |

AlertPanel prevents default form navigation, parses the number, validates, disables submit,
awaits the parent callback, clears the input after success and shows an error on failure.
The audit added accessible control names and required/min validation. `App.handleCreateAlert`
adds a temporary item then replaces it with the server response; failure removes it.
Notifications expire after six seconds or dismiss on click.

`api.js` uses VITE_API_BASE_URL and VITE_WS_URL. Backend .env names do not configure Vite.
Default browser requests go to localhost:8000. On another device localhost means that
device, so use explicit URLs and a matching allowed origin when testing beyond loopback.

Executed browser checks: cards, selection, visible chart, create/trigger notification,
dismissal, mocked 422 response/optimistic rollback, and 390px overflow. The mocked response
only proves UI error handling; the normal create/trigger test used the real backend.
No manual screen-reader audit or exhaustive keyboard/contrast audit was performed.

Remaining issues: initial fetch errors are swallowed (`App.jsx:126,130`); JSON.parse in
onmessage is unguarded; reconnect does not synchronize missed alert state; REST/WS races
and alert creation/trigger timing races are possible. CSS uses 960px and 480px breakpoints.
No search, date-range filter or saved preferences exists. Stock selection is the only filter.
