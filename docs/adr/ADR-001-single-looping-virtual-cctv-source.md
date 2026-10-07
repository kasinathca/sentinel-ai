---
title: "ADR-001 — Use One Looping Virtual CCTV Source for the Academic Demonstration"
status: "ACCEPTED"
date: "2026-10-07"
project: "Sentinel AI"
---

# ADR-001 — Use One Looping Virtual CCTV Source for the Academic Demonstration

## Context

The Sentinel AI academic project does not have access to a physical live CCTV installation. Earlier generalized documentation allowed several source transports and, in places, UI concepts that assumed multiple cameras or a live-camera selector.

The project nevertheless requires a convincing end-to-end surveillance demonstration and already has controlled recorded-video/model validation infrastructure.

## Decision

The academic baseline shall use **exactly one logical camera**.

That camera shall be driven by a **looping virtual CCTV source** backed by an approved local recorded video.

The video is selected from a **separate Demo Control Panel**.

While active, EOF automatically restarts the same video from the beginning.

The normal Sentinel operator panel consumes the logical camera feed and shall not contain file-selection controls.

Downstream AI/domain logic shall operate through the camera-source abstraction rather than use a special “recorded demo” decision path.

Physical CCTV/RTSP/ONVIF integration and multi-camera behavior are not required for the MVP.

## Consequences

Positive:

- removes dependency on unavailable physical CCTV infrastructure;
- preserves a realistic surveillance data-flow boundary;
- creates reproducible academic demonstrations;
- allows deterministic positive/negative fixtures;
- lets future physical-camera adapters reuse downstream processing.

Trade-offs:

- the demo does not establish real network-camera compatibility;
- looped scenes may repeat AI observations;
- source/display/AI synchronization must be tested;
- event deduplication semantics remain a separate backend concern.

## Constraints

- no arbitrary browser-supplied filesystem paths;
- local video binaries stay outside Git unless explicitly permitted;
- exactly one camera for this academic baseline;
- loop at EOF;
- frozen violence model/policy unchanged;
- do not claim physical live-CCTV deployment.

## Alternatives rejected for current scope

### Physical RTSP camera integration

Rejected for the academic baseline because no physical CCTV source/credentials are available and it adds unnecessary environmental dependency.

### Webcam as mandatory substitute

Rejected as a requirement because it changes demonstration conditions and is unnecessary when controlled fighting/non-violence video fixtures are already required.

### Multi-camera simulation

Rejected because it increases UI, orchestration, state, testing, and concurrency complexity without academic benefit for the current project.

### Whole-file offline analysis presented as the final camera design

Rejected as the final architecture because the project goal is to present recorded material through a camera-like replay source. Offline file processing remains useful for development/preflight.

## Related documents

- `21-virtual-cctv-replay-integration.md`
- `02-srs.md`
- `04-system-architecture.md`
- `07-api-specification.md`
- `12-ui-ux-specification.md`
- `14-test-plan.md`
- `17-operator-manual.md`
