---
title: "Sentinel AI — Security and Privacy Specification"
document_id: "SEN-SEC-PRIV"
version: "0.2.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
last_updated: "2026-09-12"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "security architecture"
  - "privacy controls"
  - "threat model"
  - "authentication and authorization requirements"
  - "API and WebSocket security"
  - "AI-worker trust boundary"
  - "evidence and media protection"
  - "secret management"
  - "logging and redaction"
  - "dependency and supply-chain security"
  - "security testing"
  - "pre-demo hardening"
---

# Sentinel AI — Security and Privacy Specification

> **Document purpose**
>
> This document defines the security and privacy requirements for Sentinel AI.
>
> It is written as an engineering control specification for an academic CCTV-monitoring prototype.
>
> It defines:
>
> - assets that require protection;
> - threat actors and abuse cases;
> - trust boundaries;
> - authentication and authorization principles;
> - API and WebSocket protections;
> - AI-worker trust assumptions;
> - video and evidence-media protections;
> - secrets and configuration handling;
> - database controls;
> - logging and redaction;
> - dependency and software-supply-chain controls;
> - privacy/data-minimization requirements;
> - responsible-AI boundaries;
> - security verification and pre-demo hardening.
>
> **Important scope statement**
>
> Sentinel AI is an academic prototype.
>
> This document uses established security/privacy frameworks as engineering references.
>
> It does **not** claim:
>
> - formal OWASP ASVS certification;
> - legal compliance certification;
> - penetration-test certification;
> - production-security assurance;
> - regulatory approval.
>
> Formal compliance claims require separate legal and security review beyond the project scope.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document becomes authoritative for Sentinel security and privacy behavior.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `01-vision-and-scope.md`
3. `02-srs.md`
4. `04-system-architecture.md`
5. `06-database-design.md`
6. `07-api-specification.md`
7. `12-ui-ux-specification.md`
8. accepted ADRs

If security requirements conflict with convenience, the secure behavior takes priority unless the requirement is formally revised.

## 0.2 Status vocabulary

| Status | Meaning |
|---|---|
| `CONFIRMED` | Required control |
| `PROPOSED` | Candidate control awaiting baseline |
| `TBD` | Unresolved |
| `DEFERRED` | Future hardening |
| `REJECTED` | Explicitly excluded |

## 0.3 Security reference baseline

Current reference sources verified on 2026-08-20:

### OWASP Application Security Verification Standard

Official:

```text
https://owasp.org/www-project-application-security-verification-standard/
```

Current stable version:

```text
ASVS 5.0.0
```

Sentinel uses ASVS as a verification/control reference only.

### OWASP Top 10

Official:

```text
https://owasp.org/Top10/
```

Current edition:

```text
OWASP Top 10:2025
```

### OWASP API Security Top 10

Official:

```text
https://owasp.org/API-Security/editions/2023/
```

Current stable edition:

```text
2023
```

### OWASP WebSocket Security Cheat Sheet

Official:

```text
https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html
```

### NIST AI Risk Management Framework

Official:

```text
https://www.nist.gov/itl/ai-risk-management-framework
```

AI RMF 1.0 remains the published framework and is being revised.

### NIST Privacy Framework

Official:

```text
https://www.nist.gov/privacy-framework
```

Privacy Framework 1.0 remains published; version 1.1 remains an Initial Public Draft at the time of this document.

---

# 1. Security Objectives

Sentinel security is organized around:

```text
Confidentiality
Integrity
Availability
Authentication
Authorization
Accountability
Privacy
Resilience
```

## 1.1 Confidentiality

Protect:

- camera configuration;
- credentials;
- evidence;
- user/account data;
- private CCTV/video;
- model/storage internals.

## 1.2 Integrity

Protect against unauthorized modification of:

- cameras;
- zones;
- rules;
- events;
- acknowledgements;
- model references;
- evidence references;
- audit records.

## 1.3 Availability

Failures in one subsystem should not unnecessarily destroy unrelated application availability.

## 1.4 Accountability

Sensitive operator/admin actions should be attributable to authenticated users where practical.

---

# 2. Protected Assets

## 2.1 Critical application assets

| Asset | Sensitivity |
|---|---|
| Authentication credentials | Critical |
| Tokens/session credentials | Critical |
| Camera credentials | Critical |
| Evidence media | High |
| Raw CCTV/video | High |
| User/role data | High |
| Event records | High |
| Zone/rule configuration | High |
| Model artifacts | Medium/High |
| Model provenance | Medium |
| Audit records | High |
| Analytics aggregates | Medium |
| Source identifiers | Medium |
| Logs | Medium/High depending on content |

---

# 3. Threat Actors

Potential threat actors include:

## 3.1 Unauthenticated external user

Capabilities:

- send arbitrary HTTP requests;
- attempt route discovery;
- manipulate identifiers;
- attempt credential attacks.

## 3.2 Authenticated low-privilege user

Capabilities:

- valid login;
- attempt access to unauthorized cameras/events/evidence;
- attempt administrative operations.

## 3.3 Malicious/compromised frontend client

Browser code/user can alter:

- API payloads;
- route parameters;
- WebSocket messages;
- hidden form values.

Therefore frontend validation is never a security boundary.

## 3.4 Compromised AI worker

Worker may send:

- malformed output;
- fabricated IDs;
- unexpected coordinates;
- oversized payloads;
- stale/replayed results.

Backend shall validate worker data.

## 3.5 Malicious media input

Video may be:

- malformed;
- oversized;
- corrupt;
- crafted to exploit decoder weaknesses;
- extremely resource-intensive.

## 3.6 Accidental insider error

A legitimate administrator may:

- draw wrong zone;
- disable camera;
- expose credentials;
- commit secrets;
- publish restricted footage.

Security design shall reduce accidental harm where feasible.

---

# 4. Trust Boundaries

```mermaid
flowchart LR
    USER[User]
    BROWSER[Browser / Frontend]
    API[FastAPI Backend]
    AI[AI Worker]
    DB[(Database)]
    MEDIA[(Evidence Storage)]
    VIDEO[External Video Source]
    MODEL[(Model Artifacts)]

    USER --> BROWSER

    BROWSER -->|TB-01| API
    AI -->|TB-02| API
    VIDEO -->|TB-03| AI
    API -->|TB-04| DB
    API -->|TB-05| MEDIA
    MODEL -->|TB-06| AI
```

## TB-01 — Browser ↔ Backend

Untrusted boundary.

Controls:

- authentication;
- authorization;
- input validation;
- CSRF protections where applicable;
- CORS;
- rate/resource protections.

## TB-02 — AI Worker ↔ Backend

Internal but not implicitly trusted.

Controls:

- schema validation;
- source/camera validation;
- model provenance;
- message-size bounds;
- replay/idempotency handling;
- internal authentication/network restriction if remote.

## TB-03 — Video Source ↔ Worker

Untrusted media boundary.

Controls:

- decoder validation;
- source-type allowlist;
- timeouts;
- resource limits.

## TB-04 — Backend ↔ Database

Trusted application boundary with credentials.

Controls:

- least-privilege DB account;
- parameterized queries;
- migrations;
- restricted network exposure.

## TB-05 — Backend ↔ Evidence Storage

Sensitive media boundary.

Controls:

- controlled storage keys;
- path normalization;
- authorization;
- no arbitrary filesystem paths.

## TB-06 — Model Artifact ↔ Worker

Model supply-chain/integrity boundary.

Controls:

- approved sources;
- checksums;
- controlled paths;
- no arbitrary user-supplied model loading.

---

# 5. Threat Modeling Method

The project may use a lightweight STRIDE-oriented review.

## STRIDE categories

```text
Spoofing
Tampering
Repudiation
Information Disclosure
Denial of Service
Elevation of Privilege
```

This document does not claim a formal full STRIDE analysis.

---

# 6. Threat Register

| ID | Threat | Primary mitigation |
|---|---|---|
| TH-001 | Unauthorized event/evidence access | object-level authorization |
| TH-002 | Admin endpoint used by operator | function-level authorization |
| TH-003 | Camera credential disclosure | secret separation/redaction |
| TH-004 | Path traversal through evidence ID/path | opaque IDs + safe storage resolution |
| TH-005 | SQL injection | ORM/parameterized queries + validation |
| TH-006 | XSS from user-controlled labels/notes | output encoding/framework protections |
| TH-007 | CSRF on authenticated mutation | auth-strategy-specific CSRF defense |
| TH-008 | WebSocket hijacking | origin/auth validation + WSS |
| TH-009 | Worker sends malformed result | contract validation |
| TH-010 | Replay/duplicate worker result | correlation/idempotency policy |
| TH-011 | Oversized video/resource exhaustion | limits + bounded processing |
| TH-012 | Secret committed to Git | secret policy + scans/review |
| TH-013 | Dependency compromise | pinned/reviewed dependencies |
| TH-014 | Restricted footage published | data classification + Git exclusion |
| TH-015 | Face-identification feature creep | explicit scope rejection |
| TH-016 | Debug endpoint exposed | environment hardening |
| TH-017 | Evidence URL guessing | authorization on every access |
| TH-018 | Role hidden in frontend but not enforced | backend authorization |
| TH-019 | Log leaks token/media path | redaction |
| TH-020 | Stale/frozen camera shown as live | UI state integrity |

---

# 7. Authentication

Exact authentication mechanism remains:

```text
TBD
```

Candidate:

- server session;
- secure cookie;
- bearer/JWT.

The implementation must satisfy the following regardless of mechanism.

## 7.1 Authentication requirements

1. Protected API endpoints require authenticated identity.
2. Authentication failure returns safe error.
3. Backend resolves current user server-side.
4. Logout/revocation semantics shall be defined.
5. Credentials/tokens shall not be logged.
6. Production/demo secrets shall not use default values.

---

# 8. Password Security

Applicable only if local password authentication is selected.

## 8.1 Password storage

Never store plaintext passwords.

Use a maintained password hashing mechanism appropriate to the selected auth library.

Potential:

```text
Argon2id
bcrypt
```

Exact algorithm:

```text
TBD_IF_LOCAL_PASSWORD_AUTH
```

## 8.2 Password logs

Never log:

- raw password;
- hash;
- reset token.

---

# 9. Session / Token Security

Exact strategy: `TBD`.

## 9.1 General requirements

- unpredictable credentials;
- expiry;
- revocation/logout strategy;
- secure transport;
- no token in normal logs;
- no token embedded in public links.

## 9.2 Cookie-based session

If used, consider:

```text
HttpOnly
Secure
SameSite
```

according to deployment.

## 9.3 Bearer token

If used:

- client storage strategy must be reviewed;
- avoid unnecessary long-lived tokens;
- do not expose token in query strings.

---

# 10. Authorization

Authorization is:

```text
CONFIRMED_SERVER_SIDE
```

Frontend hiding does not count.

## 10.1 Object-level authorization

Every endpoint using user-controlled object IDs shall verify the authenticated user may access that object.

Examples:

```text
/events/{event_id}
/evidence/{evidence_id}
/cameras/{camera_id}
/rules/{rule_id}
```

This directly addresses the object-level access-control risk emphasized by the OWASP API Security Top 10.

---

# 11. Function-Level Authorization

Administrative functions require explicit permissions.

Examples:

```text
create camera
change camera source
create zone
change rule
disable camera
manage users
view audit
```

Do not rely on:

```text
admin button hidden in UI
```

---

# 12. Property-Level Authorization / Mass Assignment

Request schemas shall whitelist mutable fields.

Example:

A camera update request must not be allowed to overwrite:

```text
id
created_at
internal credential fields
audit actor
```

simply because fields exist in ORM models.

---

# 13. Proposed RBAC Model

Status:

```text
PROPOSED
```

Potential roles:

- Administrator
- Operator
- Reviewer

## 13.1 Candidate permission matrix

| Capability | Admin | Operator | Reviewer |
|---|---:|---:|---:|
| View dashboard | Yes | Yes | Yes |
| View events | Yes | Yes | Yes |
| View evidence | Yes | Yes | Yes |
| Acknowledge | Yes | Yes | TBD |
| Submit false-positive feedback | Yes | Yes | TBD |
| Create/edit camera | Yes | No | No |
| Draw/edit zones | Yes | No | No |
| Configure rules | Yes | No | No |
| View analytics | Yes | Yes | Yes |
| View model metadata | Yes | TBD | Yes |
| View audit | Yes | No | TBD |
| Manage users | TBD | No | No |

This is not yet authoritative until RBAC is baselined.

---

# 14. Authorization Denial

If authorization fails:

```text
403
```

or application-equivalent denial.

No database mutation shall occur.

Audit logging may record denied sensitive actions where useful.

---

# 15. API Input Validation

All request inputs are untrusted.

Validate:

- identifiers;
- strings;
- enums;
- timestamps;
- polygon coordinates;
- duration values;
- URLs/source locators;
- upload metadata;
- filters;
- nested JSON.

---

# 16. Injection Prevention

## 16.1 SQL injection

Use:

- parameterized ORM queries;
- bound parameters.

Do not build:

```python
sql = "SELECT ... WHERE name = '" + user_input + "'"
```

## 16.2 OS command injection

Avoid shell execution for:

- ffmpeg;
- ffprobe;
- media processing;

when library APIs or argument arrays are available.

If subprocess is required:

- no shell interpolation;
- use explicit argument list;
- validate file paths.

---

# 17. Cross-Site Scripting

User-controlled content may include:

- camera name;
- zone name;
- rule name;
- acknowledgement comment;
- feedback notes.

Frontend framework escaping should remain enabled.

Avoid raw HTML rendering.

If HTML rendering is ever required:

- sanitize deliberately.

---

# 18. CSRF

CSRF protection depends on authentication mechanism.

## Cookie-based authentication

Mutating endpoints require appropriate CSRF defenses.

## Bearer-token API

Risk profile differs, but CORS/origin and token handling remain important.

Status:

```text
TBD_AFTER_AUTH_SELECTION
```

---

# 19. CORS

Allowed origins shall be explicitly configured for deployment.

Avoid:

```text
Access-Control-Allow-Origin: *
```

together with credentialed requests.

Development origins may differ from final demo configuration.

---

# 20. API Inventory

The project shall maintain a known list of:

- public routes;
- protected routes;
- internal worker routes;
- development-only routes.

This reduces accidental exposure of forgotten endpoints.

---

# 21. Development / Test Endpoints

Any endpoint used to inject fake events or bypass normal processing must be:

```text
DEVELOPMENT_ONLY
```

Requirements:

- disabled in final demo configuration unless explicitly disclosed;
- inaccessible from normal production route set;
- never presented as real AI functionality.

---

# 22. API Resource Consumption

Potential expensive operations:

- history queries;
- video upload;
- evidence streaming;
- analytics;
- worker jobs.

Controls may include:

- maximum pagination limit;
- upload size limit;
- bounded date range;
- bounded worker queue;
- streaming rather than loading full media into memory.

Exact limits remain:

```text
TBD
```

Do not leave operations unbounded by default.

---

# 23. Server-Side Request Forgery

Relevant if Sentinel accepts remote source URLs.

Risk:

A user-supplied camera URI could cause the server/worker to access:

- localhost;
- private metadata services;
- internal network services.

If arbitrary remote URLs are supported:

- restrict source schemes;
- validate destinations;
- consider allowlisting;
- prevent unintended internal network access.

Exact control depends on selected camera input mode.

---

# 24. Camera Source Validation

Accepted source types shall be allowlisted.

Do not pass arbitrary strings into decoder/network libraries without validation.

Potential source kinds:

```text
file
webcam
rtsp
uploaded_video
```

Only baselined types are accepted.

---

# 25. Camera Credential Protection

Camera credentials shall not be stored directly inside a publicly retrievable source URI.

Avoid:

```text
rtsp://user:password@host/path
```

inside ordinary DB/API response.

Preferred:

```text
source locator
+
separate secret/credential reference
```

Exact secret backend:

```text
TBD
```

---

# 26. Secret Management

Secrets include:

- DB password;
- application signing secret;
- camera password;
- internal worker credential;
- object-storage key.

## 26.1 Repository

Never commit secrets.

Use:

```text
.env.example
```

with placeholders only.

Example:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DB
APP_SECRET=CHANGE_ME
```

But real values never enter the file.

---

# 27. `.env` Handling

Recommended:

```gitignore
.env
.env.*
!.env.example
```

Adjust carefully if environment-specific examples are needed.

---

# 28. Secret Rotation

Formal automated rotation is not required for MVP.

But if a secret is accidentally committed:

1. remove from current code;
2. revoke/replace it;
3. do not assume deleting Git line removes exposure;
4. review repository history and sharing.

---

# 29. Git Security

Before commit:

- inspect staged files;
- exclude videos/models/secrets;
- review configuration.

No private CCTV, external dataset archive, or secret should be committed accidentally.

---

# 30. Dependency Security

Dependencies are a supply-chain risk.

## Controls

- pin versions where practical;
- use official package registries;
- avoid abandoned/unnecessary libraries;
- review licenses;
- minimize dependency count;
- update known vulnerable libraries before final demo.

---

# 31. Lock Files

Use the package ecosystem's lock/pinned mechanism where practical.

Examples:

```text
requirements.txt with pinned versions
pyproject/lock
package-lock.json
pnpm-lock.yaml
```

Exact tooling: `TBD`.

---

# 32. Dependency Introduction Rule

Every major dependency should have:

```text
purpose
source
license
maintenance status
security implications
```

Do not add a package merely to implement a trivial utility.

---

# 33. AI/ML Dependency Risk

Model frameworks may:

- load serialized Python objects;
- execute unsafe deserialization;
- download artifacts automatically.

Only load model artifacts from:

- approved source;
- controlled local path;
- registry-verified artifact.

---

# 34. Unsafe Model Serialization

Some model formats can execute arbitrary code during loading depending on framework/serialization.

Therefore:

- do not load arbitrary user-uploaded model files;
- prefer trusted sources;
- record checksum;
- use safer formats/options where supported.

---

# 35. Model Artifact Integrity

Final model artifacts should have:

```text
SHA-256
```

stored in registry.

If checksum mismatches:

```text
do not deploy silently
```

---

# 36. AI Worker Trust

The worker is internal but not fully trusted.

Backend validates:

- schema version;
- camera ID;
- correlation ID;
- model version;
- coordinates;
- score type;
- status;
- message size.

---

# 37. Worker Authentication

If worker uses network communication:

internal authentication is:

```text
TBD
```

Potential:

- local-only binding;
- shared internal token;
- mutual TLS;
- protected private network.

For local academic deployment, localhost/private process isolation may be sufficient if documented.

---

# 38. Worker Network Exposure

Do not expose worker API directly to the public internet.

Frontend shall not call worker directly.

---

# 39. Worker Replay / Duplicate Handling

If transport retries messages:

backend shall tolerate duplicate delivery according to correlation/idempotency design.

A repeated result shall not produce uncontrolled duplicate events.

---

# 40. Worker Failure

Worker failure must not be translated into:

```text
no detection
```

or:

```text
non-violence
```

Failure is a separate state.

---

# 41. Video Input Security

Media is untrusted.

Controls:

- supported-container validation;
- decoder error handling;
- maximum size where uploaded;
- maximum duration if appropriate;
- bounded resolution if appropriate;
- safe temporary paths;
- cleanup.

Exact numeric limits:

```text
TBD
```

---

# 42. File Upload Security

Applicable only if uploaded-video mode is selected.

## Requirements

- random/server-generated storage key;
- never trust client filename as path;
- validate extension and actual decode/type;
- size limit;
- isolated storage;
- no direct execution;
- no path traversal.

---

# 43. Filename Handling

Bad:

```python
save_path = uploads / user_filename
```

without validation.

Preferred:

```text
server-generated opaque filename/storage key
```

Original filename may be stored only as metadata if needed.

---

# 44. Path Traversal

User must never control arbitrary filesystem path.

Protected resources use:

```text
evidence_id
```

not:

```text
/path/to/file.mp4
```

Backend resolves ID to controlled storage record.

---

# 45. Media Content Access

Every evidence content request requires authorization.

Do not assume:

```text
unguessable UUID = authorization
```

---

# 46. Direct Static Media Serving

If evidence is exposed through static server:

- avoid public directory;
- use protected routing/signed access;
- short-lived URLs where object storage is used.

Exact mechanism: `TBD`.

---

# 47. Media Content-Disposition

If download is implemented:

use safe filenames and appropriate response headers.

Do not reflect unsafe client-supplied filenames.

---

# 48. Video Browser Security

If streaming/proxying video:

- validate content type;
- avoid open proxy behavior;
- protect camera/source secrets;
- restrict origin/access.

---

# 49. Database Security

## 49.1 Network exposure

Database should not be publicly reachable unless explicitly required.

Local/demo deployment should bind/restrict appropriately.

## 49.2 Credentials

Use application-specific DB credentials.

Do not use:

```text
root/admin/superuser
```

for ordinary application access where avoidable.

---

# 50. Database Least Privilege

Application DB user should have only required permissions.

Migration/admin credentials may be separate if practical.

For academic MVP, one DB user may be acceptable if limited to the project DB and not system-wide.

---

# 51. Database Query Safety

Use:

- ORM;
- parameterized queries.

Dynamic sort/filter keys should be allowlisted.

---

# 52. Database Integrity

Enforce:

- PK;
- FK;
- unique constraints;
- basic checks.

Do not remove constraints simply because application code hits errors.

---

# 53. Database Backups

Backup data may contain sensitive event/user metadata.

Protect backup files with the same care as the DB.

Do not commit dumps to Git.

---

# 54. Evidence Storage Security

Evidence storage contains potentially identifying footage.

Controls:

- non-public by default;
- application-mediated access;
- controlled key paths;
- deletion policy;
- no directory listing;
- no credential exposure.

---

# 55. Evidence Integrity

Recommended:

```text
SHA-256
```

metadata for final evidence where practical.

This can detect unexpected file replacement.

---

# 56. Evidence Failure

A missing media file should not trigger fallback to arbitrary path lookup.

Return explicit:

```text
not found / failed / deleted
```

state.

---

# 57. Logging Principles

Logs are operational evidence but can become a privacy/security leak.

## Log

- request ID;
- route template;
- result code;
- user ID where relevant;
- event ID;
- camera ID;
- correlation ID;
- safe error code;
- timing.

## Do not log

- password;
- auth token;
- cookie;
- camera password;
- raw evidence;
- full private source URL with credentials;
- raw video frames;
- secret environment variables.

---

# 58. Log Redaction

If a URL may contain credentials:

redact before logging.

Example:

```text
rtsp://***:***@host/path
```

or preferably log only camera ID.

---

# 59. Exception Logging

Server logs may include technical tracebacks in development.

Final client responses shall not.

Production/demo logs should avoid leaking secrets in stack context.

---

# 60. Audit Log

Status:

```text
PROPOSED
```

Potential audited actions:

- login failures/success where appropriate;
- camera create/update/disable;
- zone update;
- rule update;
- acknowledgement;
- feedback;
- user/role change.

---

# 61. Audit Integrity

User cannot choose:

```text
actor_user_id
```

in ordinary client request.

Backend derives actor from authenticated identity.

---

# 62. Audit Metadata

Use limited structured metadata.

Do not dump:

```text
full HTTP body
```

by default.

---

# 63. WebSocket Security

If WebSocket is selected, it is a persistent authenticated channel and requires separate security treatment.

---

# 64. WebSocket Transport

For non-local/non-development deployment:

```text
wss://
```

is required.

Plain:

```text
ws://
```

is acceptable only in controlled local development where transport encryption is not available/necessary.

Do not call unencrypted transport secure.

---

# 65. WebSocket Authentication

Authentication mechanism: `TBD`.

Possible:

- secure session cookie;
- connection token;
- bearer protocol mechanism.

Do not place durable secrets in URL query parameters without explicit review.

---

# 66. WebSocket Origin Validation

Validate allowed origins where browser-based connections are used.

This helps prevent cross-site WebSocket hijacking.

---

# 67. WebSocket Authorization

Authorization shall be checked:

- at connection;
- for sensitive message/action if client-to-server commands are supported.

Do not assume an authenticated socket can access every camera/event.

---

# 68. WebSocket Message Validation

Incoming messages, if any, are untrusted.

Validate:

- type;
- size;
- schema;
- identifiers.

If Sentinel WebSocket is server-push-only, reject unsupported client command messages.

---

# 69. WebSocket Resource Limits

Potential controls:

- maximum message size;
- connection count;
- idle timeout;
- ping/pong;
- bounded outbound queue.

Exact values:

```text
TBD
```

---

# 70. WebSocket Compression

OWASP currently recommends caution around `permessage-deflate`.

Sentinel should not enable WebSocket compression unless needed and reviewed.

Status:

```text
PROPOSED: DISABLED_UNLESS_REQUIRED
```

---

# 71. WebSocket Logging

Log safe events:

- connect;
- disconnect;
- auth failure;
- protocol error;
- unusual message.

Do not log sensitive payload bodies indiscriminately.

---

# 72. Frontend Security

Frontend is not trusted.

Controls:

- no secrets in bundle;
- API remains authoritative;
- safe rendering;
- dependency review;
- route guards for UX only;
- server authz for security.

---

# 73. Local Storage

Do not store:

- camera passwords;
- DB secrets.

Token storage strategy depends on auth selection.

Avoid persistent browser storage of sensitive video/evidence.

---

# 74. Browser Cache

Sensitive evidence may require cache-control headers.

Exact policy:

```text
TBD
```

For highly sensitive media, conservative caching is preferred.

---

# 75. Security Headers

Recommended final deployment review:

```text
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
frame-ancestors / anti-clickjacking
Strict-Transport-Security when HTTPS
```

Exact header values depend on deployment.

Do not copy a CSP that breaks required video/WebSocket endpoints without testing.

---

# 76. Clickjacking

Administrative pages should not be frameable by arbitrary sites.

Use CSP `frame-ancestors` or equivalent policy.

---

# 77. Content Security Policy

A practical CSP may reduce XSS impact.

Status:

```text
PROPOSED
```

Requires frontend resource inventory.

---

# 78. HTTPS

If application is exposed beyond local trusted machine/network:

```text
HTTPS
```

should be used.

For classroom/localhost development, plaintext HTTP may be used with documentation.

Do not present localhost HTTP as production-secure deployment.

---

# 79. Debug Mode

Final demo configuration shall not expose framework debug pages with:

- stack trace;
- environment values;
- filesystem paths.

---

# 80. Default Credentials

Prohibited.

If demo users are seeded:

- use non-secret course-demo credentials only when appropriate;
- do not reuse real passwords;
- document them as demo-specific if disclosed.

---

# 81. Error Handling Security

Client receives safe messages.

Example:

```text
Internal server error.
Request ID: ...
```

Detailed stack remains in controlled logs.

---

# 82. Exceptional Condition Handling

OWASP Top 10:2025 explicitly includes mishandling of exceptional conditions as a major risk category.

Sentinel must handle:

- failed DB transaction;
- missing evidence;
- worker timeout;
- invalid media;
- model failure;
- WebSocket disconnect;

without insecure fallback or false-success behavior.

---

# 83. Secure Failure

Security-sensitive failure should default to:

```text
deny
```

rather than:

```text
allow
```

Examples:

- auth service error;
- evidence authorization lookup failure;
- invalid role state.

---

# 84. Analytics Authorization

Analytics may expose sensitive operational patterns.

Access should follow role policy.

Do not assume aggregate data is automatically public.

---

# 85. Model Metadata Authorization

Model version/license may be low sensitivity.

Artifact path, private storage path, internal model URL may be higher sensitivity.

Expose only required fields.

---

# 86. API Response Minimization

Return only fields needed.

Do not serialize entire ORM objects.

This reduces accidental exposure of:

- credential refs;
- internal timestamps;
- private paths;
- audit metadata.

---

# 87. Enumeration

Public IDs may be UUIDs, but UUID does not replace authorization.

Where practical, errors should avoid leaking sensitive resource existence to unauthorized users.

---

# 88. Rate Limiting

Exact limits remain `TBD`.

Potential candidates for limits:

- login;
- upload;
- expensive analytics;
- repeated evidence requests;
- internal worker submit endpoint.

Rate limiting is not a substitute for authorization.

---

# 89. Denial of Service

Potential resource-exhaustion sources:

- giant uploads;
- many concurrent streams;
- expensive analytics ranges;
- WebSocket connections;
- unbounded worker queue;
- high-resolution video.

Controls:

- bounds;
- concurrency limits;
- timeouts;
- backpressure;
- pagination.

---

# 90. Backpressure Security/Relevance

Unbounded queue can cause:

- memory exhaustion;
- stale alerts.

Bounded/latest-frame strategy is preferred.

---

# 91. Data Privacy Scope

Sentinel processes data that may identify people visually even without facial recognition.

Therefore video/evidence should be treated as potentially personal/sensitive operational data.

---

# 92. Privacy Principles

Sentinel shall follow:

```text
purpose limitation
data minimization
access limitation
retention limitation
transparency in project documentation
human review
```

as engineering principles.

---

# 93. Purpose Limitation

Video is processed for:

- person-based monitoring rules;
- violence/fighting event detection;
- evidence review.

It shall not be repurposed for:

- facial identity;
- demographic profiling;
- behavioral scoring unrelated to requirements.

---

# 94. Data Minimization

Do not persist:

- every frame;
- every track indefinitely;
- biometric embeddings;
- unnecessary raw footage.

Persist event-relevant context only.

---

# 95. No Facial Recognition

Status:

```text
REJECTED
```

The system shall not:

- enroll faces;
- match faces;
- identify people;
- search identities across cameras.

---

# 96. No Sensitive Attribute Inference

Do not infer:

- race;
- religion;
- health;
- sexuality;
- political affiliation;
- disability;
- other sensitive attributes.

Such inference is out of scope and unnecessary.

---

# 97. Track IDs

Track IDs are temporary computational identifiers.

They shall not be presented as real-world identity.

---

# 98. Re-identification

Cross-camera persistent person re-identification is not part of MVP.

If tracker internally uses appearance features:

- keep transient;
- do not persist by default;
- do not use for named identity.

---

# 99. Evidence Minimization

Evidence should use short event-focused clips/snapshots rather than indefinite recording where feasible.

Exact pre/post duration:

```text
TBD
```

---

# 100. Retention

Exact retention periods remain:

```text
TBD
```

The project shall not fabricate a legal retention period.

---

# 101. Retention States

Evidence metadata should support:

```text
available
failed
deleted
```

so deletion does not create confusing broken records.

---

# 102. Deletion

When evidence retention expires or explicit deletion occurs:

- remove physical media;
- update metadata;
- preserve minimal historical event facts where allowed/required by project policy.

---

# 103. Dataset Privacy

External datasets shall follow their own usage/redistribution terms.

Do not publish:

- restricted dataset video;
- violent footage;
- private samples;

because they are useful to the demo.

---

# 104. Team-Recorded Footage

If team records participants:

- obtain informed agreement;
- record only what is necessary;
- avoid hidden recording;
- document redistribution permission separately.

---

# 105. Demo Screenshots

Screenshots may include faces/video frames.

Before placing in:

- GitHub;
- report;
- presentation;

review whether the image may be shared.

Prefer staged/team-controlled footage.

---

# 106. Logs and Privacy

Do not log raw frames/evidence.

Do not put acknowledgement comments with unnecessary personal information into verbose logs.

---

# 107. Analytics Privacy

Analytics should aggregate events.

Avoid unnecessary person-level tracking analytics.

---

# 108. AI Risk Principles

NIST AI RMF is used as a voluntary reference.

Sentinel should consider:

- validity/reliability;
- safety;
- security/resilience;
- transparency/accountability;
- privacy;
- harmful bias/limitations.

No formal NIST compliance claim is made.

---

# 109. Human-in-the-Loop

Sentinel outputs are reviewable alerts.

The system shall not autonomously:

- accuse a person;
- initiate punishment;
- determine criminal intent;
- identify a suspect.

---

# 110. Model Error Transparency

Model/rule outputs may contain:

- false positives;
- false negatives.

UI/report shall not imply infallibility.

---

# 111. Score Semantics

Do not label:

```text
score = 0.87
```

as:

```text
87% certainty
```

unless model calibration supports that interpretation.

---

# 112. Responsible False-Positive Feedback

Operator feedback is:

```text
human review signal
```

not automatically ground truth.

---

# 113. No Online Self-Training

MVP does not retrain itself from operator feedback.

---

# 114. Privacy Risk Register

| ID | Risk | Mitigation |
|---|---|---|
| PR-001 | footage identifies participants | restricted access |
| PR-002 | evidence retained too long | retention policy |
| PR-003 | face recognition added accidentally | explicit rejection |
| PR-004 | tracker becomes identity system | transient IDs only |
| PR-005 | dataset media redistributed | registry/terms gate |
| PR-006 | screenshots expose people | sharing review |
| PR-007 | logs contain private media paths/data | redaction |
| PR-008 | analytics becomes person profiling | aggregate event metrics |
| PR-009 | model outputs imply criminality | neutral terminology |
| PR-010 | recorded video called live | UI integrity state |

---

# 115. Data Classification

Proposed classification:

| Data | Class |
|---|---|
| Application source code | Internal/Public depending repo |
| Public docs | Public |
| User credentials | Secret |
| Camera credentials | Secret |
| Event metadata | Restricted |
| Evidence video/images | Restricted |
| External dataset raw media | Restricted per terms |
| Team footage | Restricted unless explicitly shareable |
| Model weights | Internal/License-dependent |
| Logs | Internal/Restricted |
| Analytics | Internal |

Status: `PROPOSED`.

---

# 116. Data Flow Privacy Review

```mermaid
flowchart LR
    CAM[Video Source]
    AI[AI Worker]
    EVT[Event Context]
    EVD[Evidence]
    DB[(Database)]
    UI[Authorized UI]

    CAM --> AI
    AI --> EVT
    EVT --> DB
    EVT --> EVD
    DB --> UI
    EVD --> UI
```

Privacy principle:

```text
do not persist full AI/video stream when event-level metadata is sufficient
```

---

# 117. Storage Locations

Every data type should have a known storage class.

Example:

```text
DB → structured metadata
Media store → evidence
Data root → research datasets
Model root → model artifacts
```

Do not scatter sensitive files through desktop/download folders in final setup.

---

# 118. Temporary Files

Media processing may create temporary files.

Requirements:

- controlled directory;
- generated names;
- cleanup after use;
- no user-controlled path;
- permissions appropriate to host.

---

# 119. File Permissions

On multi-user systems, sensitive media/config should not be world-readable.

Exact OS permissions depend on deployment.

---

# 120. Local Demo Environment

For an academic demo on one machine:

security assumptions may include:

- localhost/private network;
- non-public DB;
- non-public worker;
- short-lived demo users.

These assumptions must be documented.

---

# 121. Public Deployment Warning

If the application is exposed to the public internet, additional work becomes necessary:

- HTTPS;
- hardened reverse proxy;
- stronger auth;
- rate limiting;
- operational monitoring;
- backup;
- patching;
- secret management;
- penetration testing.

The current project does not automatically claim readiness for public deployment.

---

# 122. Security Testing Strategy

Security testing layers:

```text
static review
dependency review
unit tests
API authorization tests
input validation tests
media/path tests
WebSocket tests
manual abuse testing
pre-demo hardening
```

---

# 123. Authentication Tests

If auth implemented:

## SEC-AUTH-001

Unauthenticated request to protected endpoint → denied.

## SEC-AUTH-002

Invalid credentials → denied.

## SEC-AUTH-003

Logout/revoked session cannot access protected route.

## SEC-AUTH-004

Authentication failure does not leak password/account internals.

---

# 124. Authorization Tests

## SEC-AUTHZ-001

Operator attempts camera creation → denied if admin-only.

## SEC-AUTHZ-002

Unauthorized user requests protected evidence → denied.

## SEC-AUTHZ-003

User changes object ID to another restricted event → denied.

## SEC-AUTHZ-004

Frontend-hidden admin route called manually → backend denies.

---

# 125. Mass Assignment Test

Send extra fields:

```json
{
  "name": "Test",
  "id": "attacker-chosen",
  "created_at": "...",
  "role": "administrator"
}
```

Expected:

- immutable/unknown fields rejected or ignored according to schema;
- privilege is not changed.

---

# 126. Injection Tests

Test fields such as:

```text
camera name
rule name
feedback notes
filters
```

against:

- SQL injection;
- XSS strings.

Application should store/render safely.

---

# 127. Path Traversal Tests

Attempt evidence request with manipulated paths/IDs.

Examples:

```text
../../etc/passwd
..\..\secret
```

Expected:

- path is never directly resolved from input;
- request denied/not found.

---

# 128. File Upload Tests

If upload enabled:

- oversized file;
- invalid MIME;
- renamed non-video file;
- corrupt video;
- path-like filename;
- zero-byte file.

Expected safe rejection/failure.

---

# 129. SSRF Tests

If remote camera URLs accepted:

attempt:

```text
localhost
127.0.0.1
private network destinations
file://
unsupported schemes
```

Expected behavior follows allowlist/security design.

---

# 130. WebSocket Tests

If WebSocket enabled:

## SEC-WS-001

Unauthenticated connection → denied.

## SEC-WS-002

Disallowed Origin → denied.

## SEC-WS-003

Malformed message → rejected safely.

## SEC-WS-004

Oversized message → rejected/connection handled.

## SEC-WS-005

Disconnected client cannot continue privileged actions.

## SEC-WS-006

Reconnection does not duplicate event state.

---

# 131. Worker Contract Security Tests

## SEC-WRK-001

Unknown camera ID → reject.

## SEC-WRK-002

Malformed bbox → reject.

## SEC-WRK-003

Unknown model version where required → reject.

## SEC-WRK-004

Oversized/unexpected fields → safe failure.

## SEC-WRK-005

Failed inference is not interpreted as negative inference.

---

# 132. Evidence Authorization Tests

## SEC-EVD-001

Authenticated allowed user → content available.

## SEC-EVD-002

Authenticated unauthorized user → denied.

## SEC-EVD-003

Random evidence UUID → no unauthorized leakage.

## SEC-EVD-004

Deleted/failed evidence → explicit state, no arbitrary fallback file.

---

# 133. Secret Tests

Search repository before final demo for:

```text
password=
secret=
token=
apikey
rtsp://user:
```

Review findings manually.

Do not blindly assume all matches are secrets.

---

# 134. Dependency Audit

Use available ecosystem tools if practical.

Potential:

```text
pip-audit
npm audit
```

or equivalent.

Tool selection depends on stack.

Do not claim "zero vulnerabilities" without recording tool/version/date.

---

# 135. Static Security Review

Review code for:

- shell execution;
- raw SQL;
- unvalidated file paths;
- disabled auth checks;
- wildcard CORS;
- hard-coded secrets;
- debug endpoints.

---

# 136. Manual Abuse Testing

A teammate should intentionally try:

- unauthorized resource access;
- invalid IDs;
- malformed JSON;
- direct admin endpoint use;
- repeated acknowledgement;
- evidence URL guessing.

---

# 137. Security Test Evidence

For each security test:

```yaml
test_id: "SEC-..."
date: "..."
commit: "..."
environment: "..."
steps:
  - "..."
expected: "..."
actual: "..."
status: "PASS/FAIL"
evidence: "..."
```

---

# 138. OWASP Top 10:2025 Mapping

Current OWASP Top 10:2025 categories include:

```text
A01 Broken Access Control
A02 Security Misconfiguration
A03 Software Supply Chain Failures
A04 Cryptographic Failures
A05 Injection
A06 Insecure Design
A07 Authentication Failures
A08 Software or Data Integrity Failures
A09 Security Logging and Alerting Failures
A10 Mishandling of Exceptional Conditions
```

Sentinel uses these as an awareness/mapping reference.

---

# 139. Sentinel ↔ OWASP Top 10 Mapping

| OWASP 2025 area | Sentinel control |
|---|---|
| Broken Access Control | server-side RBAC/object auth |
| Security Misconfiguration | environment hardening, no debug |
| Supply Chain Failures | dependency pinning/review |
| Cryptographic Failures | HTTPS/WSS where network exposed |
| Injection | validated/parameterized inputs |
| Insecure Design | trust boundaries/threat model |
| Authentication Failures | auth/session controls |
| Integrity Failures | model checksum, migration discipline |
| Logging/Alerting Failures | safe structured logs/audit |
| Exceptional Conditions | explicit worker/evidence/DB failure behavior |

This mapping is not an ASVS/OWASP certification.

---

# 140. OWASP API Security Mapping

Relevant API Security Top 10:2023 concerns include:

```text
Broken Object Level Authorization
Broken Authentication
Broken Object Property Level Authorization
Unrestricted Resource Consumption
Broken Function Level Authorization
Unrestricted Access to Sensitive Business Flows
Server Side Request Forgery
Security Misconfiguration
Improper Inventory Management
Unsafe Consumption of APIs
```

---

# 141. Sentinel API Security Mapping

| API risk | Sentinel example |
|---|---|
| Object-level authorization | event/evidence access |
| Broken authentication | protected API |
| Property auth | mass assignment |
| Resource consumption | pagination/upload/worker bounds |
| Function auth | admin camera/rule operations |
| Sensitive flow | acknowledgement/configuration |
| SSRF | remote camera source |
| Misconfiguration | debug/CORS |
| Inventory | `/api/v1`, internal routes |
| Unsafe API consumption | worker/external service validation |

---

# 142. ASVS Use

Sentinel may use OWASP ASVS 5.0.0 as a checklist reference for:

- authentication;
- session management;
- access control;
- validation;
- API/web-service controls;
- file handling;
- logging;
- configuration.

If specific ASVS requirement IDs are referenced later, include the ASVS version prefix.

Example style:

```text
v5.0.0-x.y.z
```

Do not copy uncontrolled requirement IDs without checking the actual standard.

---

# 143. NIST Privacy Framework Use

Sentinel uses the Privacy Framework only as a privacy-risk-management influence.

Engineering themes include:

- data processing awareness;
- governance;
- minimization;
- control;
- protection.

No formal NIST Privacy Framework conformity claim is made.

---

# 144. NIST AI RMF Use

Sentinel uses AI RMF concepts as a responsible-AI reference.

Particularly relevant:

- validity/reliability;
- safety;
- security/resilience;
- privacy;
- transparency/accountability;
- test/evaluation.

---

# 145. Legal / Regulatory Claims

The project shall not state:

```text
GDPR compliant
DPDP compliant
HIPAA compliant
ISO certified
```

without a dedicated legal/compliance assessment.

Engineering alignment is not legal compliance.

---

# 146. India Privacy Context

Because the project is developed in India, Indian data-protection obligations may become relevant depending on:

- deployment;
- actual data;
- institutional policies;
- whether personal data is processed in a regulated context.

This document does not provide legal advice.

Before any real deployment beyond controlled academic use, obtain institution/legal guidance.

---

# 147. Academic Demo Data Policy

Preferred demonstration media:

1. team-controlled staged footage;
2. clearly permitted public research/sample media;
3. synthetic media where appropriate.

Avoid using real private surveillance footage merely for realism.

---

# 148. Faculty/Reviewer Access

If faculty need to inspect the system:

create a controlled demo account rather than sharing developer secrets.

Exact account strategy: `TBD`.

---

# 149. Repository Visibility

Repository visibility:

```text
TBD
```

Before making public:

review:

- licenses;
- external datasets;
- model licenses;
- screenshots;
- secrets;
- config;
- participant footage.

---

# 150. License/Security Interaction

A technically secure dependency may still have incompatible licensing.

Both gates must pass.

Example:

```text
detector selected
→ technical evaluation
→ license review
→ security/supply-chain review
```

---

# 151. Model Download at Runtime

Avoid automatic model download during final demo where possible.

Preferred:

- artifact acquired beforehand;
- checksum known;
- controlled local location.

This improves reproducibility and reduces network/supply-chain failure.

---

# 152. Dataset Download at Runtime

Training/inference application shall not automatically download research datasets during normal startup.

Dataset acquisition is a separate controlled workflow.

---

# 153. Update Security

Automatic dependency/model updates are not required for MVP.

Pin the evaluated version.

Do not change critical library the night before demo without retesting.

---

# 154. Secure Defaults

Examples:

- camera disabled until configured;
- unknown authorization → deny;
- missing secret → startup failure or feature unavailable;
- unknown worker schema → reject;
- evidence private by default.

---

# 155. Configuration Validation

Startup should validate mandatory config.

Do not silently fall back to insecure:

```text
APP_SECRET=secret
```

or:

```text
AUTH_DISABLED=true
```

in final mode.

---

# 156. Environment Modes

Recommended conceptual modes:

```text
development
test
demo
```

If production mode is added later, define separately.

Each mode must have documented security differences.

---

# 157. Demo Mode

Demo mode must not automatically:

- disable auth;
- enable fake data;
- expose debug endpoint;

unless those choices are explicitly documented and disclosed.

---

# 158. Mock Data Security

Mock mode should not accidentally connect to real private camera sources.

Use separate configuration.

---

# 159. Error Fallback Security

Do not fall back from failed real API call to mock data.

That creates misleading/insecure behavior.

---

# 160. Evidence URL Expiry

If signed URLs are used:

expiry duration:

```text
TBD
```

Use short-lived access appropriate to demo/user flow.

---

# 161. Object Storage

If object storage is selected:

- bucket/container private by default;
- scoped credentials;
- no public listing;
- signed access or backend proxy.

---

# 162. Local Filesystem Storage

If local media is selected:

- store outside public static root;
- map evidence ID → controlled path;
- prevent traversal;
- use application authorization.

---

# 163. Evidence Naming

Use opaque event/evidence IDs.

Avoid exposing:

```text
person-name
camera-password
private-user-path
```

inside filenames.

---

# 164. Camera Snapshot Privacy

A snapshot for zone editing may contain people.

Treat it as sensitive media.

Do not cache indefinitely or expose publicly.

---

# 165. Analytics Cache

If analytics cached:

do not create public unauthenticated cache endpoint accidentally.

---

# 166. User Enumeration

Login errors may use generic invalid-credential messaging where appropriate.

Exact UX depends on auth design.

---

# 167. Brute Force

Login rate limiting/account lock policy:

```text
TBD_IF_LOCAL_AUTH
```

A simple rate limit may be adequate for demo.

Do not create irreversible lockout that jeopardizes demonstration without recovery path.

---

# 168. Password Reset

Not required for MVP unless user-management scope demands it.

Avoid implementing insecure reset flow just for completeness.

---

# 169. Email/SMS

Out of MVP.

Therefore no email/SMS credential/security design is currently required.

---

# 170. Multi-Tenancy

Not in MVP.

Do not claim tenant isolation.

---

# 171. Multi-Site

Deferred.

No site/organization-level authorization model is required now.

---

# 172. Incident Response

For an academic prototype, basic response steps:

```text
detect
contain
record
revoke/replace secret if needed
fix
retest
document
```

No formal SOC process is implied.

---

# 173. Security Issue Severity

Suggested internal categories:

```text
Critical
High
Medium
Low
```

Exact rubric: `TBD`.

Critical examples:

- auth bypass;
- evidence exposed without auth;
- committed real secret;
- arbitrary code execution.

---

# 174. Security Stop-Ship Conditions

Do not present final integrated demo as secure if any known issue allows:

- unauthenticated evidence access;
- role bypass;
- plaintext real credential exposure;
- arbitrary filesystem read;
- arbitrary shell command injection;
- public debug console;
- secret embedded in frontend bundle.

Fix or explicitly disable affected feature first.

---

# 175. Security Definition of Ready

A feature is security-ready for implementation when:

- data sensitivity known;
- actor/permission known;
- trust boundary known;
- input defined;
- storage defined;
- abuse cases considered.

---

# 176. Security Definition of Done

A security-sensitive feature is done when:

- authentication/authorization implemented;
- input validation implemented;
- errors safe;
- logs redacted;
- tests include negative/unauthorized case;
- secrets not committed;
- documentation updated.

---

# 177. Pre-Demo Security Checklist — Repository

- [ ] No `.env` committed.
- [ ] No tokens/keys committed.
- [ ] No camera password committed.
- [ ] No DB dump committed.
- [ ] No external dataset archive committed.
- [ ] No restricted model artifact published against license.
- [ ] No private CCTV media committed.
- [ ] `.gitignore` reviewed.
- [ ] Git diff reviewed.

---

# 178. Pre-Demo Security Checklist — Backend

- [ ] Debug mode off or controlled.
- [ ] Protected endpoints require auth.
- [ ] Admin functions enforce authz.
- [ ] Object-level access checks exist.
- [ ] Request schemas reject extra dangerous fields.
- [ ] SQL queries parameterized.
- [ ] CORS reviewed.
- [ ] Errors do not show stack trace to client.
- [ ] Pagination bounded.
- [ ] Development test endpoints disabled/isolated.

---

# 179. Pre-Demo Security Checklist — WebSocket

If used:

- [ ] Auth required.
- [ ] Allowed origin checked.
- [ ] WSS used if exposed beyond local dev.
- [ ] Unknown messages handled.
- [ ] Message size bounded.
- [ ] Reconnect tested.
- [ ] No token logged.

---

# 180. Pre-Demo Security Checklist — AI Worker

- [ ] Worker not publicly exposed.
- [ ] Model paths controlled.
- [ ] Model checksum/source recorded.
- [ ] Worker payload validated.
- [ ] Failed inference distinguished.
- [ ] Resource failure handled.
- [ ] No arbitrary uploaded model loading.

---

# 181. Pre-Demo Security Checklist — Media

- [ ] Evidence access authorized.
- [ ] Evidence not in public static directory.
- [ ] Path traversal tested.
- [ ] Upload validation tested if used.
- [ ] Snapshot/clip sharing reviewed.
- [ ] Team demo footage permissions known.

---

# 182. Pre-Demo Security Checklist — Database

- [ ] DB not publicly exposed.
- [ ] App credentials not superuser where practical.
- [ ] Migrations current.
- [ ] Constraints present.
- [ ] No real secrets in seed data.
- [ ] Backup/dump handling reviewed.

---

# 183. Pre-Demo Security Checklist — Frontend

- [ ] No secret in bundle.
- [ ] Route guards do not replace backend authz.
- [ ] XSS-safe rendering.
- [ ] Error states safe.
- [ ] Recorded vs live distinction correct.
- [ ] AI score terminology correct.
- [ ] Disabled vs offline distinction correct.

---

# 184. Pre-Demo Privacy Checklist

- [ ] No facial recognition.
- [ ] No sensitive-attribute inference.
- [ ] No unnecessary persistent tracks.
- [ ] Evidence minimized.
- [ ] Private footage not public.
- [ ] Dataset terms checked.
- [ ] Demo screenshots reviewed.
- [ ] Retention limitation documented or marked TBD.
- [ ] No claim of legal compliance without assessment.

---

# 185. Security Test Matrix

| Test ID | Area | Expected |
|---|---|---|
| SEC-AUTH-001 | auth | protected route denied without auth |
| SEC-AUTHZ-001 | RBAC | operator cannot admin-configure |
| SEC-OBJ-001 | object auth | unauthorized event/evidence denied |
| SEC-INJ-001 | injection | payload handled safely |
| SEC-XSS-001 | rendering | user text escaped |
| SEC-PATH-001 | traversal | arbitrary path rejected |
| SEC-UPL-001 | upload | invalid media rejected |
| SEC-SSRF-001 | source URL | unsafe destination rejected if applicable |
| SEC-WS-001 | WebSocket | unauthenticated socket denied |
| SEC-WRK-001 | worker | malformed result rejected |
| SEC-EVD-001 | media | evidence requires auth |
| SEC-LOG-001 | logging | secrets absent |
| SEC-CFG-001 | config | no default production secret |
| SEC-DEP-001 | dependency | vulnerabilities reviewed |

---

# 186. Security Evidence Directory

Recommended:

```text
artifacts/security/
├── test-results/
├── dependency-audit/
├── screenshots/
└── review-notes/
```

Do not store sensitive attack payload captures if they contain secrets.

---

# 187. Security Review Record

Template:

```yaml
review_id: "SEC-REVIEW-..."
date: "..."
commit: "..."
reviewers:
  - "..."
scope:
  - "..."
findings:
  critical: []
  high: []
  medium: []
  low: []
open_risks:
  - "..."
decision: "TBD"
```

---

# 188. Open Security Decisions

| ID | Decision | Status |
|---|---|---|
| SEC-OD-001 | Authentication mechanism | `TBD` |
| SEC-OD-002 | Exact RBAC permissions | `TBD` |
| SEC-OD-003 | Password hashing if local auth | `TBD` |
| SEC-OD-004 | Session/token storage | `TBD` |
| SEC-OD-005 | CSRF strategy | `TBD` |
| SEC-OD-006 | HTTPS deployment | `TBD_DEPLOYMENT` |
| SEC-OD-007 | Worker authentication | `TBD` |
| SEC-OD-008 | Evidence storage backend | `TBD` |
| SEC-OD-009 | Signed media URLs vs backend proxy | `TBD` |
| SEC-OD-010 | Upload size/duration limits | `TBD` |
| SEC-OD-011 | Camera URL SSRF policy | `TBD` |
| SEC-OD-012 | Rate limits | `TBD` |
| SEC-OD-013 | Audit-log inclusion | `PROPOSED` |
| SEC-OD-014 | Retention periods | `TBD` |
| SEC-OD-015 | Repository visibility | `TBD` |
| SEC-OD-016 | Security headers/CSP | `PROPOSED` |
| SEC-OD-017 | Browser evidence caching | `TBD` |
| SEC-OD-018 | Demo account strategy | `TBD` |
| SEC-OD-019 | Dependency audit tooling | `TBD` |
| SEC-OD-020 | Worker resource limits | `TBD` |

---

# 189. SRS Traceability

| Security area | Requirements |
|---|---|
| authentication | FR-AUTH-* |
| users/roles | FR-USER-* |
| server authz | NFR-SEC-002 |
| secrets | NFR-SEC-001 |
| validation | NFR-SEC-005 |
| path traversal | NFR-SEC-006 |
| safe errors | NFR-SEC-007 |
| dependencies | NFR-SEC-008 |
| evidence access | NFR-SEC-009 |
| privacy/no face ID | NFR-PRIV-* |
| logging | NFR-OBS-* |
| worker failure | FR-INTG-* |
| data integrity | NFR-DATA-* |
| academic claims | NFR-ACAD-* |

---

# 190. Use-Case Traceability

| Security concern | Use Cases |
|---|---|
| authentication | UC-AUTH-001/002 |
| camera admin | UC-CAM-* |
| zone/rule config | UC-ZONE-*, UC-RULE-* |
| evidence | UC-EVD-001 |
| acknowledgement | UC-EVT-006 |
| false-positive feedback | UC-EVT-007 |
| worker failure | UC-SYS-001/002 |
| media failure | UC-SYS-003 |
| reconnect | UC-SYS-004 |

---

# 191. Baseline Checklist

Before changing status to `BASELINED`:

- [ ] Authentication selected.
- [ ] RBAC selected.
- [ ] Object-level authorization policy accepted.
- [ ] Secret-management strategy accepted.
- [ ] Camera credential strategy accepted.
- [ ] CORS policy accepted.
- [ ] CSRF policy selected if relevant.
- [ ] WebSocket security policy accepted.
- [ ] Worker trust/auth policy accepted.
- [ ] Media authorization flow accepted.
- [ ] Upload validation policy accepted if uploads exist.
- [ ] SSRF controls accepted if remote sources exist.
- [ ] Logging/redaction accepted.
- [ ] Database exposure/privilege accepted.
- [ ] Dependency review process accepted.
- [ ] Privacy/data-minimization policy accepted.
- [ ] No facial recognition confirmed.
- [ ] Retention status recorded.
- [ ] Security test matrix accepted.
- [ ] No compliance certification is falsely claimed.

---

# 192. AI Assistant Security Rules

Once this document is baselined, an AI coding assistant shall never:

1. disable authentication to make a test pass;
2. remove authorization checks for convenience;
3. trust frontend role checks as security;
4. expose evidence by opaque ID without authorization;
5. return raw ORM models containing secret/internal fields;
6. hard-code a real secret;
7. log credentials/tokens;
8. add wildcard credentialed CORS without approval;
9. accept arbitrary local file paths from users;
10. invoke a shell with unsanitized user input;
11. load arbitrary user-supplied model files;
12. expose the AI worker publicly;
13. treat worker messages as trusted without schema validation;
14. change failed inference into a negative result;
15. add facial recognition;
16. persist biometric embeddings;
17. add cross-camera identity tracking;
18. use restricted dataset/evidence media in public UI without review;
19. claim OWASP/NIST/legal compliance merely because controls are inspired by them;
20. weaken validation, limits, or security solely to make the demo succeed.

---

# 193. Final Security and Privacy Rule

> **Sentinel AI shall fail transparently and securely rather than appear functional through insecure shortcuts.**
>
> The core security expectations are:
>
> ```text
> authenticate the user
> → authorize the operation
> → validate all input
> → protect secrets and media
> → preserve domain/data integrity
> → log safely
> → handle failures explicitly
> → minimize personal data
> → retain human review
> ```
>
> A successful academic demonstration does not require production-grade infrastructure.
>
> It does require that the project does not knowingly:
>
> - expose private footage;
> - bypass access control;
> - commit secrets;
> - misrepresent AI certainty;
> - introduce biometric identity;
> - hide security failures.
>
> Any unresolved control shall remain:
>
> `TBD`
>
> until the team makes and records the decision.


---

# 48. Violence Runtime Security Update — 2026-09-12

The qualified violence runtime introduces two implementation-specific security
requirements without changing the project's overall trust model.

## 48.1 Worker messages remain untrusted input

The backend shall continue to validate:

- schema version;
- `job_id`;
- `correlation_id`;
- `camera_id`;
- model task;
- model-version ID;
- score type/range;
- window timestamps;
- success versus explicit failure.

The selected violence model/version is:

```text
MODEL-VIO-BIGRU-ATTN-XD-V1
model_version_id = 6d22f83d-17f8-5ecf-9f0f-246fa326ec72
```

A worker result is evidence of model computation, not authorization to mutate
persistent event state directly.

## 48.2 Controlled source references

Worker requests shall use an opaque/configured:

```text
source_locator_ref
```

rather than accepting an arbitrary filesystem path supplied by an untrusted
client.

Any local-file development adapter must resolve that reference through trusted
operator-controlled configuration.

The backend/API shall not expose unrestricted local path traversal into the AI
worker.

## 48.3 Artifact integrity

The selected temporal checkpoint and training implementation are pinned by
SHA-256:

```text
checkpoint:
1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772

training script:
630c913060c7800c96214438e8e36064b946679aa83aad4b8fd4943b6717690c
```

Runtime startup should fail closed if the expected artifact identity does not
match.

## 48.4 Failure semantics

A model/extractor/decode failure shall be represented as an explicit worker
failure.

It shall never be transformed into:

```text
successful low score
successful non-violence result
no event
```

because doing so would hide an unavailable safety-analysis capability.

## 48.5 Dataset/model artifacts and Git

Do not commit:

- external raw XD-Violence video archives;
- raw compatibility MP4s unless redistribution is explicitly permitted;
- large `.npy` feature corpora;
- `.pt`, `.pth`, `.pkl`, or comparable model binaries unless the repository
  policy explicitly permits them.

Documentation may record hashes, version IDs, and local path conventions without
publishing the artifacts themselves.
