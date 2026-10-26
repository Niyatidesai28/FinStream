# Audit changes

- Baseline commits 5d25863a02b44bcbe6885ed7c84852144edbc6c4 and
  e36268d88a181b2c1cdf1a1091a7c03df38263be capture recovery/progress (second adds baseline file).
- Reject non-finite prices and unsupported normalized symbols before storage.
- Run short alert handlers on the event loop to avoid cross-thread dictionary mutation.
- Format API detail arrays; label and constrain alert form controls.
- Add 13 backend regression cases and a real local browser workflow with explicit mocked error case.
- Apply compatible npm lockfile advisory fixes; add pytest 9.0.3/httpx development requirements.
- Document actual simulation/in-memory design, limitations, 32 interview questions and rebuild exercises.

Use `git log --oneline main..HEAD` to identify each later repair/documentation commit.
No SQL, external market feed, authentication or deployment was added.
