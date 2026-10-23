# Sentinel AI Frontend

React/Vite operator frontend integrated with the current Sentinel backend REST routes.

## Current backend integration

The frontend service layer currently consumes:

```text
GET /api/v1/health
GET /api/v1/cameras
GET /api/v1/cameras/{id}
GET /api/v1/events
GET /api/v1/events/{id}
GET /api/v1/demo/clips
PUT /api/v1/demo/source
POST /api/v1/demo/source/start
POST /api/v1/demo/source/stop
POST /api/v1/demo/source/restart
GET /api/v1/demo/source/status
GET /api/v1/cameras/{id}/stream
```

The Camera Monitoring view provides approved-source selection, start/stop/restart controls, the canonical MJPEG stream, AI/session diagnostics, and a qualified alert driven by backend state. The application truthfully displays unavailable states for capabilities that do not exist in this release, including persisted acknowledgement and snapshot/evidence delivery.

## Install and run

```powershell
cd .\frontend
npm ci
npm run dev
```

## Development API proxy

The Vite proxy no longer requires source-code editing when the backend address changes.

Default:

```text
http://127.0.0.1:8000
```

Optional machine-local override:

```powershell
Copy-Item .env.example .env
```

Then edit only the ignored `.env` file:

```dotenv
VITE_API_PROXY_TARGET=http://127.0.0.1:8000
```

Do not commit machine-specific `.env` values.

## Quality checks

```powershell
npm run lint
npm run build
```

The repository-level verification script also runs these checks:

```powershell
powershell -ExecutionPolicy Bypass -File ..\scripts\verify_integration.ps1
```
