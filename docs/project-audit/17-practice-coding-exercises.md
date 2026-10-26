# Exercises with acceptance criteria

1. **Validation:** Implement a helper accepting only finite positive prices. Test -1, 0,
   1, NaN and infinity. Explain why gt=0 alone allowed the observed failure.
2. **Thresholds:** Recreate check_alerts for two alerts at exactly 100. Both matching
   above/below equality conditions fire once; a second call returns no new triggers.
3. **React selection:** Add an aria-pressed attribute to StockCard. Clicking MSFT must
   select its chart and expose pressed=true only for that card. Use native button semantics.
4. **History:** Implement append-and-trim without mutating previous state. With a cap
   of 3, adding a fourth point retains points 2–4 and leaves the old input array unchanged.
5. **Error messages:** Convert either a string detail or a list of {msg} to display text.
   An empty/unknown response falls back to a useful message; never [object Object].
6. **Reconnect:** Design a GET /alerts refresh after connection recovery. Test an alert
   triggered while disconnected. Explain how to avoid a late snapshot overwriting newer events.
7. **Broadcast isolation:** Use fake sockets where one raises. Verify other clients still
   receive messages and only the failing connection is removed. Then reason about a client
   that hangs rather than raises; propose a timeout test without sleeping indefinitely.
8. **Persistence extension:** In a separate exercise database, create users and alerts
   with a foreign key and parameterized INSERT. Query active alerts by user. This project
   currently does not perform SQL; do not present the exercise as existing functionality.

Suggested solution approach: inspect tests/test_app.py (under backend/) for 1,2,7;
App.appendHistory for 4; api.createAlert for 5. Write a failing test first, then the smallest
change, then rerun the real browser workflow. For 6 and 8 specify race/ownership semantics
before coding. No exercise should use production data or a paid market-data service.
