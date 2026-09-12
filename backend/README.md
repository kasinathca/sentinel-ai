# Sentinel AI Backend — Phase 2L AI Integration Slice

This is the first FastAPI backend implementation slice. It implements the transport-neutral consumption side of the frozen violence worker contract without choosing the final backend↔worker transport.

## Implemented

- FastAPI application factory and `GET /api/v1/health`;
- strict worker success/failure validation;
- frozen model-version registry adapter;
- rolling state keyed by `(camera_id, model_version_id)`;
- frozen `score >= 0.906` + `3-of-5` criterion;
- explicit worker failure handling;
- event-domain condition handoff port;
- development JSONL replay adapter;
- backend↔worker frozen-value parity test.

## Deliberately not implemented yet

Authentication, PostgreSQL migrations, worker HTTP/queue/IPC transport, persistent event creation, duplicate/cooldown/retrigger behavior, evidence, WebSockets, acknowledgement, detector/tracker integration.

## Setup

```powershell
python -m venv .ackend\.venv
.ackend\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .ackendequirements-dev.txt
$env:PYTHONPATH = ".ackend"
python -m unittest discover -s .ackend	ests -p "test_*.py" -v
```

## Run API

```powershell
uvicorn app.main:app --app-dir .ackend --host 127.0.0.1 --port 8000
```

## Replay worker outputs without selecting a transport

```powershell
$env:PYTHONPATH = ".ackend"
python .ackend\scriptseplay_violence_worker_jsonl.py --input ".i_workeruntime_work\demo-fighting-results.jsonl"
python .ackend\scriptseplay_violence_worker_jsonl.py --input ".i_workeruntime_work\demo-normal-results.jsonl"
```

Expected Fighting: 19 accepted, 10 qualified, first index 4, candidate true.
Expected Normal: 26 accepted, 0 qualified, candidate false.

`candidate_condition=True` is only a condition handoff. It does not require a new persistent event; duplicate/cooldown/retrigger/persistence remain event-domain responsibilities.
