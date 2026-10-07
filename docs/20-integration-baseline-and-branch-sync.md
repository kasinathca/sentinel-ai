---
title: "Sentinel AI — Integration Baseline and Branch Synchronization Record"
document_id: "SEN-INTEGRATION-SYNC"
version: "0.1.0"
status: "IMPLEMENTATION_RECORD"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
recorded_at: "2026-10-06"
source_baseline_branch: "staging"
source_baseline_commit: "71115d7dde91eb300678a82a916a9b916e15bffb"
---

# Sentinel AI — Integration Baseline and Branch Synchronization Record

## 0. Purpose and authority

This is an **implementation/integration record**, not a replacement for the SRS, architecture, API, database, AI/ML, security, test, or deployment specifications.

It records:

- the Git branch state inspected on 2026-10-06;
- how the currently integrated code should be promoted to `main` without losing teammate work;
- reproducible setup corrections discovered during frontend/backend staging integration;
- machine-path portability rules;
- verification commands;
- the branch synchronization procedure after promotion.

If this record conflicts with a baselined requirements/design document, the authoritative requirements/design document takes precedence and the implementation must be reviewed.

---

# 1. Source integration baseline

This change set is intentionally based on:

```text
branch: staging
commit: 71115d7dde91eb300678a82a916a9b916e15bffb
```

At inspection time:

| Branch | Head | Relationship to old `main` |
|---|---|---|
| `main` | `dc828663ff26ef60d553dc572b4d59168cec06a4` | older baseline |
| `gouri/backend-domain` | `42399c06159fbe3f5c5bd5689bab12eee8369257` | backend work branch |
| `aaditi/frontend-operator-ui` | `a99232200f0e3c3e87f2fdfa9477eb1a4b78dd81` | frontend work branch |
| `staging` | `71115d7dde91eb300678a82a916a9b916e15bffb` | contains both teammate branches |

`staging` was 16 commits ahead of the old `main` and 0 behind. Therefore applying integration fixes directly to the stale old `main` would risk omitting already-integrated teammate work.

**Promotion rule:** create the fix/integration branch from current `origin/staging`, verify it, then merge that branch into `main`.

---

# 2. Database initialization incident

Observed staging behavior:

```text
GET /api/v1/health   -> 200
GET /api/v1/cameras  -> 500
sqlite OperationalError: no such table: cameras
```

After running the documented database initialization:

```text
GET /api/v1/health   -> 200
GET /api/v1/cameras  -> 200
GET /api/v1/events   -> 200
```

with empty camera/event arrays on the fresh local database.

## 2.1 Root cause

The first response was not evidence that persistence was ready. `/api/v1/health` checks process liveness; the camera route queries the database.

The SQLite file/connection could therefore exist before the required Alembic schema had been applied.

## 2.2 Corrective implementation

This integration update:

1. keeps `/api/v1/health` as liveness;
2. implements the already-proposed `/api/v1/health/readiness` path;
3. checks DB connectivity, required tables, and the expected Alembic revision;
4. returns HTTP `503` when the DB is reachable but uninitialized/outdated;
5. never auto-runs migrations from an HTTP request;
6. adds `backend/scripts/check_database.py`;
7. makes `init_database.py` verify readiness after migration + seed.

The endpoint implementation does not silently baseline unresolved AI-worker/evidence readiness semantics. Those components report truthful `not_checked` / `not_integrated` states.

---

# 3. Filesystem portability correction

Project policy requires runtime environment-specific paths to be externalized and rejects developer-specific absolute paths.

The inspected staging tree contained a developer-specific XD-Violence default in the AI-worker PowerShell helper and developer-machine paths in AI-worker instructions.

This update removes those assumptions.

## 3.1 Required runtime root

Raw-video violence inference uses either:

```text
--root <workspace>
```

or:

```text
SENTINEL_VIOLENCE_ROOT=<workspace>
```

No developer home path is assumed.

## 3.2 Optional artifact overrides

```text
SENTINEL_TEMPORAL_CHECKPOINT
SENTINEL_TEMPORAL_TRAIN_SCRIPT
SENTINEL_EXTRACTOR_PYTHON
SENTINEL_EXTRACTOR_WORKER
SENTINEL_RUNTIME_WORK_DIR
```

Relative values are resolved under the configured workspace root.

The extractor environment default is platform-aware:

```text
Windows -> .venv/Scripts/python.exe
POSIX   -> .venv/bin/python
```

Frozen model/checksum/criterion values are unchanged.

---

# 4. Frontend development configuration

The frontend still uses relative `/api/v1/...` requests.

The Vite development proxy target is now configurable through:

```text
VITE_API_PROXY_TARGET
```

with the existing localhost development behavior retained as the fallback.

This is development configuration only; it does not decide the project's final deployment port/topology.

---

# 5. Environment examples

Repository examples intentionally contain no real secrets or developer-specific paths:

```text
.env.example
frontend/.env.example
```

Real `.env` files remain ignored.

---

# 6. Verification gate before promotion

Run from repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_integration.ps1
```

The verification script uses a disposable SQLite DB and runs:

1. Alembic migration + frozen seed;
2. DB readiness check;
3. backend tests;
4. AI-worker pure/unit tests;
5. frontend `npm ci`;
6. frontend lint;
7. frontend production build.

Raw-video violence inference is a separate gate because it requires the external qualified runtime/artifacts/GPU. It must not be falsely marked passed by unit tests.

---

# 7. Promotion workflow

The recommended history-preserving sequence is:

```text
origin/staging
    ↓
new integration/fix branch
    ↓
apply portability/readiness change
    ↓
verification gate
    ↓
commit
    ↓
merge into main
    ↓
push main
    ↓
fast-forward staging to main
```

Do not reset `main` to `staging` and force-push. Do not rewrite teammate feature-branch history merely to make all branch heads identical.

---

# 8. Post-promotion teammate workflow

Preferred for new work:

```powershell
git fetch origin --prune
git checkout main
git pull --ff-only origin main
git checkout -b <new-feature-branch>
```

If an existing teammate branch must continue:

```powershell
git fetch origin --prune
git checkout <existing-branch>
git merge origin/main
```

Resolve conflicts in that branch, run verification, and then push normally.

Do **not** force-push unless the team explicitly agrees to rewrite that branch.

---

# 9. Branch divergence inspection

Use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check_branch_sync.ps1
```

The script reports, for each known branch:

```text
main-only commits
branch-only commits
```

It performs only `git fetch` plus read-only Git queries. It does not merge or push.

---

# 10. Ownership/scope rule for this integration update

This update intentionally handles cross-cutting integration/reproducibility issues suitable for the promoted `main` baseline:

- database readiness and initialization verification;
- runtime path portability;
- development proxy configuration;
- environment examples;
- integration verification tooling;
- branch synchronization documentation.

It intentionally does **not** implement unfinished product/domain subsystems such as:

- authentication/authorization;
- durable acknowledgement;
- evidence storage/delivery;
- WebSocket/realtime event delivery;
- detector/tracker integration;
- restricted-area/loitering/crowd rule implementation;
- camera streaming/snapshots;
- analytics;
- violence-event cooldown/deduplication/episode policy.

Those must follow their requirements/design decisions and normal branch ownership/review.

---

# 11. Maintenance rule

Whenever a migration is added after `20261005_0002`:

1. update `EXPECTED_ALEMBIC_HEAD` in `backend/app/db/readiness.py`;
2. update readiness tests;
3. run `scripts/verify_integration.ps1`;
4. update this integration record or its successor if the operational baseline changes.

Whenever the external runtime layout changes:

1. preserve frozen artifact identity/checksum requirements;
2. prefer configuration overrides over machine-specific path edits;
3. update `.env.example` and AI-worker README;
4. rerun pure/unit tests and qualified runtime preflight.

---

<!-- VIRTUAL_CCTV_BASELINE_20261007:BEGIN -->

# 2026-10-07 Integration Record Addendum — Virtual CCTV Documentation Baseline

Immediately before this documentation kit was prepared, the following remote branches were verified identical:

```text
main
staging
aaditi/frontend-operator-ui
gouri/backend-domain
```

Verified common commit:

```text
81d7222d8880b52a4990a9987540b9e68eb74b59
```

The approved next documentation baseline introduces:

- one camera only;
- looping recorded-video virtual CCTV;
- separate Demo Control Panel;
- no physical CCTV dependency;
- no multi-camera requirement;
- no model retuning;
- explicit target-vs-implemented distinction.

Safe propagation rule:

1. update `main` from the verified common baseline;
2. commit documentation once;
3. fast-forward the three other branches to the documentation commit if they have not diverged;
4. if any branch has diverged, stop and merge/review normally;
5. never force-push merely to synchronize documentation.

The provided `apply_and_sync_all_branches.ps1` implements this conservative workflow.

<!-- VIRTUAL_CCTV_BASELINE_20261007:END -->
