# Dynamic ingest and continuous-AI acceptance evidence — 2026-10-09

All inference below used the existing qualified worker, frozen model version
`6d22f83d-17f8-5ecf-9f0f-246fa326ec72`, threshold `0.906`, W1/stride 1, and
the complete-history 3-of-5 policy. `+` means `score >= 0.906`; `-` means it
did not. Timestamps are UTC and are relative to the recorded source start
`2026-10-09T00:00:00Z`.

## Exact canonical-source worker windows

- **FIGHT 1.mp4** — 4 windows, 2 positive:
  `00:00:00-00:00:02.133 0.09410486370325089 -`;
  `02.133-04.267 0.9940978288650513 +`;
  `04.267-06.400 0.9803077578544617 +`;
  `06.400-07.867 0.8715246915817261 -`.
- **FIGHT 2.mp4** — 4 windows, 2 positive:
  `00:00:00-00:00:02.133 0.02070985920727253 -`;
  `02.133-04.267 0.9893398880958557 +`;
  `04.267-06.400 0.9961919784545898 +`;
  `06.400-06.733 0.345769464969635 -`.
- **FIGHT 3.mp4** — 6 windows, 3 positive:
  `00:00:00-00:00:02.133 0.12628212571144104 -`;
  `02.133-04.267 0.9915429353713989 +`;
  `04.267-06.400 0.972426176071167 +`;
  `06.400-08.533 0.9939621090888977 +`;
  `08.533-10.667 0.8528982996940613 -`;
  `10.667-11.500 0.3515488803386688 -`.
- **NOR-FIGHT 1.mp4** — 3 windows, 1 positive:
  `00:00:00-00:00:02.133 0.023769691586494446 -`;
  `02.133-04.267 0.01281560305505991 -`;
  `04.267-05.967 0.9439687132835388 +`.
- **NOR-FIGHT 2.mp4** — 3 windows, 0 positive:
  `00:00:00-00:00:02.133 0.012938559986650944 -`;
  `02.133-04.267 0.15762987732887268 -`;
  `04.267-04.667 0.46161767840385437 -`.
- **NORMAL.mp4** — 5 windows, 0 positive:
  `00:00:00-00:00:02.133 0.004017955157905817 -`;
  `02.133-04.267 0.002925110049545765 -`;
  `04.267-06.400 0.00666224118322134 -`;
  `06.400-08.533 0.02820718102157116 -`;
  `08.533-10.167 0.05320148915052414 -`.
- **NORMAL 2.mp4** — 16 windows, 0 positive; scores in order:
  `0.01093252096325159, 0.03897725045681, 0.0688251256942749,
  0.010065027512609959, 0.006193374749273062, 0.005260540172457695,
  0.03787881135940552, 0.006985013838857412, 0.011845745146274567,
  0.08650859445333481, 0.047317299991846085, 0.004906907211989164,
  0.004434657748788595, 0.006281509064137936, 0.23995035886764526,
  0.31496357917785645`. Windows start at `00:00:00`; ends are
  `02.133, 04.267, 06.400, 08.533, 10.667, 12.800, 14.933, 17.067,
  19.200, 21.333, 23.467, 25.600, 27.733, 29.867, 32.000, 33.300`.
- **NORMAL 3.mp4** — 6 windows, 0 positive; scores:
  `0.019342131912708282, 0.013456558808684349, 0.008160246536135674,
  0.004160443786531687, 0.003998036962002516, 0.1435585618019104`;
  ends `02.133, 04.267, 06.400, 08.533, 10.667, 11.667`.
- **NORMAL 4.mp4** — 4 windows, 1 positive:
  `00:00:00-00:00:02.133 0.30754995346069336 -`;
  `02.133-04.267 0.014674295671284199 -`;
  `04.267-06.400 0.9493053555488586 +`;
  `06.400-06.600 0.05994676053524017 -`.

## Real Chrome sessions through the launcher

All nine catalog entries reported `normalization=transcoded`, H.264/yuv420p,
1280×720, 30 FPS, CFR. The values are snapshots after the stated genuine
passes; event count is for that source session.

| Clip | Session | Passes | Windows | Positive total | Current / 5 | Max / 5 | Ever qualified | Session detected | Event count | Loops | Latest score |
|---|---|---:|---:|---:|---:|---:|---|---|---:|---:|---:|
| FIGHT 1 | `d4578443-75f6-4756-84e2-adc750631502` | 3 | 12 | 6 | 2 | 3 | yes | yes | 1 | 6 | 0.8715246915817261 |
| FIGHT 2 | `1771c0ce-6129-4dc5-858a-e4f4196b40f9` | 2 | 8 | 4 | 2 | 3 | yes | yes | 1 | 4 | 0.345769464969635 |
| FIGHT 3 | `0a42ef46-7476-4800-98f5-be121079070b` | 1 | 6 | 3 | 3 | 3 | yes | yes | 1 | 1 | 0.3515488803386688 |
| NOR-FIGHT 1 | `0ea8fce7-1a9f-46db-af36-d3c43904ed0c` | 2 | 6 | 2 | 2 | 2 | no | no | 0 | 4 | 0.9439687132835388 |
| NOR-FIGHT 2 | `2c8fa03f-f797-4059-85cf-5b9722da4a99` | 2 | 6 | 0 | 0 | 0 | no | no | 0 | 6 | 0.46161767840385437 |
| NORMAL | `2d00d017-b94e-48a4-b5d9-199fc51b19d1` | 1 | 5 | 0 | 0 | 0 | no | no | 0 | 1 | 0.05320148915052414 |
| NORMAL 2 | `ad6c5631-977e-4821-996c-093befb8604c` | 1 | 16 | 0 | 0 | 0 | no | no | 0 | 1 | 0.31496357917785645 |
| NORMAL 3 | `a3a4552c-ad6d-4382-b4e3-a8515579dc7e` | 1 | 6 | 0 | 0 | 0 | no | no | 0 | 1 | 0.1435585618019104 |
| NORMAL 4 | `a1ed3030-471c-4f48-b1e0-71776e15879b` | 2 | 8 | 2 | 1 | 2 | no | no | 0 | 5 | 0.05994676053524017 |

FIGHT 1 first qualified at `2026-10-09T02:24:23.405+05:30`, event
`a2d31c4e-6443-4a2f-a000-35e2f9716c99`. FIGHT 2 first qualified at
`2026-10-09T02:25:20.808+05:30`, event
`6cbbe726-7b73-4d17-b4d7-b7bba0657300`. FIGHT 3 first qualified at
`2026-10-09T02:25:56.436+05:30`, event
`a55f845a-5371-4fec-8c0f-11c9bad68223`.

FIGHT 1 and FIGHT 2 demonstrate both truths simultaneously: their current
rolling state later fell to 2/5 (not currently qualifying), while
`session_violence_detected=true` and the single persisted event remained.
NOR-FIGHT 1 demonstrates that a latest positive observation alone does not
qualify a 2/5 rolling history.

## Live ingest, identity, and shutdown evidence

- External source: 340×256 H.264/yuv420p, 28 FPS, 10 seconds, SHA-256
  `071e60535eaf0aed475ddac06269ee0cdfc4740158f22d9ccd2c3b93b42aa344`.
- Copied while running as `sir_live_test.mov`; Chrome showed waiting then
  ready after Refresh Videos. No manifest/backend restart/manual FFmpeg.
- Opaque ID: `demo-1b22db93f2f45658897ac058d6978cff`.
- Canonical derivative: H.264/yuv420p, 1280×720, 30 FPS, CFR, 10 seconds.
- Replay process and worker source-map both resolved the exact same canonical
  derivative path for that opaque ID.
- Identical bytes copied as `fight_video.mp4`, `normal_video.mp4`, and
  `banana_123.mov`; all derivatives had identical SHA-256
  `2b982044e472440515cdf68f29c05f7abd5c1aca5eeec232a6deac5542e32d53`.
- Ctrl+C during active normalization of a 69.066667-second video left no
  listener on ports 8010/5180 and no partial output. Immediate relaunch
  produced ready canonical ID `demo-3d1049bbde465af19578105630058a39`.

## Verification status

- Full `scripts/verify_integration.ps1`: PASS — database migration/readiness,
  backend 96/96, AI-worker 19/19, npm install/audit, lint, production build.
- Frontend view-model tests: 5/5 PASS.
- Frozen model preflight: PASS (`ready`, extractor/model/process all ready).
- Launcher missing-FFprobe negative test: PASS (clear early failure, exit 1).
- Real launcher, browser ingest, all-nine fixture run, dashboard return,
  Ctrl+C during normalization, and immediate relaunch: PASS.
- An initial focused test invocation from the repository root failed because
  `app` was not on `PYTHONPATH`; the corrected backend-working-directory run
  passed 36/36. A sandboxed retry then failed because Python's temporary
  directory was outside the writable sandbox; the same command with the
  required filesystem permission passed. These setup failures were retained
  rather than misreported as product failures.
