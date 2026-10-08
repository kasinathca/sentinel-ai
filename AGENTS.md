# Sentinel AI — Codex / AI agent entry point

Read these sources **before changing code**:

1. `docs/22-academic-violence-demo-scope.md` — project-lead scope decision effective 2026-10-08. Narrow review-first and final academic release: one virtual CCTV video source, **actual frozen violence inference**, and **visible qualified alert**.
2. `docs/AGENTS.md` — repository engineering standards and non-fabrication rules. Where older broad MVP requirements conflict with the approved academic scope, follow the explicit scoped change record in `docs/22-academic-violence-demo-scope.md`; do not implement removed functionality silently.
3. `docs/19-violence-model-and-runtime-qualification.md` — frozen model, exact extractor, checkpoint/sha, temporal policy, evaluation provenance. **Never retrain or retune just to obtain a demo.**
4. `docs/21-virtual-cctv-replay-integration.md` — single virtual CCTV camera, looping replay, session and source abstraction.
5. `docs/23-branch-and-pr-reconciliation.md` and `docs/24-review-readiness-and-acceptance.md` — recorded Git status and measurable remaining work.

## Required engineering behavior

- Check existing code, current Git branches, merged PRs, tests, and API contracts before adding new code.
- Preserve the FastAPI modular monolith, separate AI worker, existing SQLite migrations/seed, React/Vite frontend, and existing FFmpeg camera adapter where functional.
- Do not build authentication, roles, tracking, intrusion, loitering, crowd features, large analytics/evidence subsystems, or cloud deployment solely because they appear in old drafts.
- Treat `candidate_condition=true` and `event_persisted=false` as distinct states. Live UI alerts must come from actual qualified model output, never hardcoded fixture labels or test mocks.
- Never assume fixed local machine directories. All model/media/FFmpeg locations are configured or discovered dynamically; keep research footage and checkpoints out of Git.
- Bind local-only demo services to loopback and preserve safe clip ID/path validation.
- For the 2026-10-09 review, prioritize functional video playback and actual model integration/alert over appearance or unnecessary infrastructure.
- Report evidence-backed `PASS`, `FAIL`, `BLOCKED`, and `NOT_YET_EXECUTED` statuses and preserve failed test outputs.
