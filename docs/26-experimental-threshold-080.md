# Experimental event threshold 0.80

Status: **EXPERIMENTAL / UNVALIDATED EVENT POLICY**

This branch changes only the backend event-score threshold from the qualified
`0.906` policy to an opt-in `0.80` policy. It does not change the frozen model,
checkpoint, extractor, raw score generation, W1 window, stride, 3-of-5 complete
history requirement, session deduplication, replay, persistence, or alert flow.
The published accuracy, precision, recall, F1, and false-event measurements for
the qualified `0.906` policy do not apply to this experiment.

## Launch

From this experimental worktree, double-click or run:

```powershell
.\launch_sentinel_demo_080.cmd
```

The wrapper scopes these values to its child process and then reuses the
existing launcher:

```text
SENTINEL_EXPERIMENTAL_THRESHOLD=0.80
SENTINEL_DATABASE_URL=sqlite+pysqlite:///<this-worktree>/backend/runtime/sentinel_exp_080.db
SENTINEL_BACKEND_PORT=8010
SENTINEL_FRONTEND_PORT=5180
```

The experimental database is ignored by Git through the existing `runtime/`
rule. Initialization remains idempotent and rejects a stored policy mismatch.
The UI reads the backend status and displays `Experimental event threshold:
0.80` with rolling qualification `3 of 5`.

## Qualified mode

Run `launch_sentinel_demo.cmd` from the original checkout with
`SENTINEL_EXPERIMENTAL_THRESHOLD` unset. It continues using the original
database, ports `8000`/`5173`, and the qualified threshold `0.906`.

Invalid, non-finite, out-of-range, or non-`0.80` experimental values fail at
backend configuration import. There is no silent fallback.
