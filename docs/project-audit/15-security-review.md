# Security review

Scope: all original first-party code/configuration, synthetic local requests, package
advisory scans and pattern-based secret scan. No intrusive remote tests or production use.

No obvious credential pattern matched in tracked/candidate files. `.env.example` contains
only examples including unused SECRET_KEY=change-me. This limited scan does not prove no
secret ever existed in Git history. Do not put confidential values in VITE_ variables.

Repaired: unknown/empty-symbol acceptance, non-finite price serialization/storage failure,
readable API validation errors and form validation/accessibility. Async alert handlers avoid
thread-pool mutation of the dictionary used by the broadcast coroutine within one worker.

Outstanding: all alerts are shared and unauthenticated; unbounded creation is a resource
risk; WebSockets have no ownership/origin validation; serial sends lack a per-client timeout;
startup fetch failures are hidden. CORS is configured for local origins but is not access
control. There is no SQL injection surface or upload/path handling in this repository.
React renders values as text; no dangerouslySetInnerHTML was found. No authenticated session,
password storage or authorization model exists to assess.

`npm audit` initially reported 7 affected dependency entries (2 moderate, 5 high).
`npm audit fix --ignore-scripts` made compatible lockfile changes; 2 remain (Vite high,
esbuild moderate). A forced Vite major upgrade is deferred under the prompt's breaking-change
rule. [esbuild advisory](https://github.com/advisories/GHSA-67mh-4wv8-2f99).
Python advisory scan initially reported 16 vulnerability records across pytest and Starlette,
including duplicate IDs. The audit-added pytest was upgraded to fixed 9.0.3. FastAPI 0.115.0
constrains Starlette to the old compatibility range; resolving remaining Starlette advisories
requires a reviewed framework upgrade. Counts are scanner records, not unique exploitable
bugs; feature reachability was not exhaustively assessed. Raw scans are retained locally
and summarized here without claiming a clean bill of health.

Recommended order: compatible framework migration + regression, explicit demo-only hosting,
then authentication/ownership/retention and durable storage/event semantics if the product
is to be deployed. No security protections were disabled to obtain passing tests.
