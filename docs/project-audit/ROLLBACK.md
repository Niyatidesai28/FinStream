# Recovery without changing main

Original repository: https://github.com/Niyatidesai28/FinStream
Original commit: `5ca6a97cdfd31562b2980e20d318bd60a11c6a84`. Audit branch: `codex/finstream-audit`.

First run `git status`. Commit your own work to a separate branch or copy it to a safe
location before switching branches. Do not discard uncommitted changes.

```sh
git log --oneline --decorate
git show 5ca6a97cdfd31562b2980e20d318bd60a11c6a84
git switch main
git switch codex/finstream-audit
git show <fix-commit>
```

`main` was not modified by this audit. To inspect the original version separately:
`git worktree add --detach ../original-review 5ca6a97cdfd31562b2980e20d318bd60a11c6a84`.
To undo one published change, create a new commit with `git revert <fix-commit>`
on the audit branch, resolve any conflicts, then rerun its tests. This preserves history.
To adopt selected fixes, create a new review branch from main and run
`git cherry-pick <fix-commit>`. Include prerequisite test/config commits where needed.

To abandon the audit, switch to main and leave the audit branch archived. Optional
`git branch -d codex/finstream-audit` refuses to remove an unmerged branch. Do not use force deletion
unless you have backed up the branch and consciously accept losing its local reference.
Remote deletion is not part of this audit. No reset-hard or clean commands are needed.

Review the draft PR's Files changed, tests and risk notes before deciding what to merge.
The user must make that decision. No auto-merge, history rewrite or production deployment
has been performed. A final documentation commit cannot contain its own SHA; use
`git log --format='%H %s' 5ca6a97cdfd31562b2980e20d318bd60a11c6a84..codex/finstream-audit` for the exact complete history.
