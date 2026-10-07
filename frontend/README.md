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
```

The application truthfully displays unavailable states for backend capabilities that do not yet exist, including persisted acknowledgement and live stream/snapshot delivery.

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
