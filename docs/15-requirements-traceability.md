---
title: "Sentinel AI — Requirements Traceability Matrix"
document_id: "SEN-RTM"
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
  - "requirement-to-design traceability"
  - "requirement-to-use-case traceability"
  - "requirement-to-planned-implementation traceability"
  - "requirement-to-test traceability"
  - "verification evidence tracking"
  - "coverage-gap identification"
---

# Sentinel AI — Requirements Traceability Matrix

> **Document purpose**
>
> This document is the master traceability ledger for Sentinel AI.
>
> It connects every formal SRS requirement to its relevant use cases, engineering specifications, planned implementation area, verification method, planned test evidence, and current verification status.
>
> It is intentionally evidence-conservative: **no requirement is marked verified merely because a design document or planned test exists.**
>
> As of 2026-09-12, violence model/runtime qualification evidence has been
executed and attached conceptually through the experiment artifacts described in
`19-violence-model-and-runtime-qualification.md`.

Application-level verification remains conservative: model/runtime evidence does
not by itself prove backend event persistence, duplicate suppression, evidence
generation, notifications, or operator workflows.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document becomes authoritative for project traceability.

Requirement wording and metadata remain authoritative in `02-srs.md`. This matrix does not rewrite or renumber requirements.

The principal source documents are:

- `02-srs.md` — formal requirement definitions;
- `03-use-case-specification.md` — actor/use-case behavior;
- `04-system-architecture.md` — system/module boundaries;
- `06-database-design.md` — persistence design;
- `07-api-specification.md` — integration contracts;
- `08-ai-ml-design.md` — AI subsystem design;
- `10-dataset-registry.md` — actual dataset identity/use;
- `11-model-card-and-evaluation.md` — evaluation evidence standard;
- `12-ui-ux-specification.md` — frontend behavior;
- `13-security-and-privacy.md` — security/privacy controls;
- `14-test-plan.md` — verification plan and test IDs.

## 0.2 Traceability rule

The required project chain is:

```text
Requirement
→ Use Case / Behavioral Need
→ Design Decision / Specification
→ Planned Implementation Target
→ Test / Review
→ Execution Evidence
→ Verification Status
```

No link may be silently inferred during final reporting.

## 0.3 Current execution state

```text
Requirement definitions: PRESENT
Design traceability: PRESENT
Planned test traceability: PRESENT
Implementation evidence: PARTIAL — violence model/runtime evidence exists
Test execution evidence: PARTIAL — violence qualification suite executed
Final requirement verification: NOT_YET_VERIFIED for whole application
```

---

# 1. Traceability Status Vocabulary

| Status | Meaning |
|---|---|
| `PLANNED_TEST_LINKED` | Existing test-plan/security test IDs are linked |
| `PLANNED_REVIEW_LINKED` | Requirement is primarily verified by inspection/document/model review and an evidence source is defined |
| `PLANNED_COVERAGE_GAP` | Requirement is traceable to design, but an exact dedicated test/review item still needs to be added |
| `BLOCKED_BY_TBD_DECISION` | Verification cannot be finalized until a `TBD_SCOPE` design decision is resolved |
| `BLOCKED_BY_DOMAIN_DECISION` | Entire domain concept is unresolved and implementation/test must not be invented |
| `NOT_YET_VERIFIED` | No actual pass/review evidence has been attached yet |
| `VERIFIED` | Requirement has accepted execution/review evidence |
| `FAILED` | Verification evidence shows requirement is not satisfied |
| `INVALIDATED` | Previous verification evidence is no longer valid due to a material change |

---

# 2. SRS Coverage Snapshot

This matrix contains **155 of 155** formal SRS requirement IDs.

## 2.1 Scope status

| SRS scope status | Requirements |
|---|---:|
| `CONFIRMED_SCOPE` | 115 |
| `PROPOSED_SCOPE` | 19 |
| `TBD_SCOPE` | 21 |
| **Total** | **155** |

## 2.2 Priority

| Priority | Requirements |
|---|---:|
| `MUST` | 133 |
| `SHOULD` | 22 |
| **Total** | **155** |

## 2.3 Planned verification coverage

| Coverage state | Requirements |
|---|---:|
| `PLANNED_TEST_LINKED` | 98 |
| `PLANNED_REVIEW_LINKED` | 23 |
| `PLANNED_COVERAGE_GAP` | 24 |
| `BLOCKED_BY_TBD_DECISION` | 9 |
| `BLOCKED_BY_DOMAIN_DECISION` | 1 |
| **Total** | **155** |

> These counts describe **planning traceability**, not passed tests. All rows remain `NOT_YET_VERIFIED` until evidence is attached.

---

# 3. Traceability Fields

Each requirement row records:

1. **Requirement ID and title** — copied from the SRS heading.
2. **Scope/Priority** — copied from SRS metadata.
3. **Use case(s)** — behavioral trace where applicable.
4. **Design / planned implementation** — authoritative design files and conceptual implementation target.
5. **Verification / planned test** — SRS verification method plus existing test/review identifiers.
6. **Expected evidence** — artifact class to retain when executed.
7. **Coverage state** — whether the verification link is already defined or still has a planning gap.
8. **Execution state** — currently `NOT_YET_VERIFIED` for every requirement.

---

# 4. Implementation Target Disclaimer

Paths in this matrix such as:

```text
backend/app/modules/events
ai_worker
frontend/src/features/events
models/registry
data/manifests
```

are **planned architecture targets** from the design documents. They are not evidence that those files/modules already exist.

During implementation, replace or supplement these entries with actual module/file references without changing the stable requirement ID.

---

# 5. Master Requirements Traceability Matrix

The tables below preserve the SRS order and all 155 IDs.

## 5.1 `FR-AUTH`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-AUTH-001` | Authenticated access to protected application functions | `PROPOSED_SCOPE` / `MUST` | UC-AUTH-001, UC-AUTH-002 | 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/auth; frontend/src/auth | System test → SEC-AUTH-001; ACPT-002; ACPT-003; TC-UI-SHELL-003 | artifacts/security/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-AUTH-002` | Server-side authorization | `PROPOSED_SCOPE` / `MUST` | UC-AUTH-001, UC-AUTH-002 | 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/auth; frontend/src/auth | Security test → SEC-AUTHZ-001; SEC-AUTHZ-004; ACPT-019 | artifacts/security/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-AUTH-003` | Authentication failure handling | `PROPOSED_SCOPE` / `MUST` | UC-AUTH-001, UC-AUTH-002 | 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/auth; frontend/src/auth | Security test → SEC-AUTH-002; SEC-AUTH-004 | artifacts/security/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-AUTH-004` | Logout or session termination | `TBD_SCOPE` / `MUST` | UC-AUTH-001, UC-AUTH-002 | 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/auth; frontend/src/auth | System test → SEC-AUTH-003; dedicated logout UI/API test `TBD` | artifacts/security/ + artifacts/tests/api/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |

## 5.2 `FR-USER`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-USER-001` | User identity record | `PROPOSED_SCOPE` / `MUST` | UC-AUTH-001; UC-ADM-001; dedicated user-management UC `TBD` | 06-database-design.md; 07-api-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/users; DB user/role tables | Integration test → Document/DB verification + dedicated user-identity persistence test `TBD` | artifacts/security/ + artifacts/tests/database/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-USER-002` | Role or permission association | `TBD_SCOPE` / `MUST` | UC-AUTH-001; UC-ADM-001; dedicated user-management UC `TBD` | 06-database-design.md; 07-api-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/users; DB user/role tables | System test → SEC-AUTHZ-001–004; exact role-association persistence test `TBD` | artifacts/security/ + artifacts/tests/database/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |

## 5.3 `FR-CAM`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-CAM-001` | Register a camera or video source | `CONFIRMED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-API-CAM-001; ACPT-004 | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CAM-002` | List configured camera or video sources | `CONFIRMED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-API-CAM-003; ACPT-004 | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CAM-003` | Retrieve camera/source details | `CONFIRMED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-API-CAM-004 covers unknown-ID path; successful detail test `TBD` | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-CAM-004` | Update camera/source configuration | `PROPOSED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → Dedicated camera-update API/DB regression test `TBD` | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-CAM-005` | Disable camera/source processing | `PROPOSED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-API-CAM-005; TC-UI-LIVE-003 | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CAM-006` | Camera/source health state | `CONFIRMED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-UNIT-HEALTH-001–004; ACPT-005 | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CAM-007` | Camera-offline event | `CONFIRMED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-UNIT-HEALTH-003; TC-E2E-OFF-001; ACPT-015 | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CAM-008` | Camera recovery state | `PROPOSED_SCOPE` / `MUST` | UC-CAM-001–004; UC-EVT-005 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/cameras; frontend/src/features/cameras | System test → TC-UNIT-HEALTH-005; TC-WRK-FAIL-002 where relevant | artifacts/tests/api/ + artifacts/tests/database/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.4 `FR-ZONE`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-ZONE-001` | Create polygonal monitoring zone | `CONFIRMED_SCOPE` / `MUST` | UC-ZONE-001–002 | 05-uml-and-system-models.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/zones; frontend/src/features/zones | System test → TC-API-ZONE-001–003; TC-UI-ZONE-001–002; ACPT-006–007 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ZONE-002` | Update monitoring zone | `CONFIRMED_SCOPE` / `MUST` | UC-ZONE-001–002 | 05-uml-and-system-models.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/zones; frontend/src/features/zones | System test → TC-API-ZONE-004; TC-UI-ZONE-003,005–006; ACPT-007 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ZONE-003` | Disable monitoring zone | `CONFIRMED_SCOPE` / `MUST` | UC-ZONE-001–002 | 05-uml-and-system-models.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/zones; frontend/src/features/zones | System test → Dedicated zone-disable API/UI test `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-ZONE-004` | Zone-to-source consistency | `CONFIRMED_SCOPE` / `MUST` | UC-ZONE-001–002 | 05-uml-and-system-models.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/zones; frontend/src/features/zones | Integration test → TC-API-ZONE-005; TC-RULE-INT-006 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ZONE-005` | Zone visualization | `CONFIRMED_SCOPE` / `MUST` | UC-ZONE-001–002 | 05-uml-and-system-models.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/zones; frontend/src/features/zones | System test → TC-UI-LIVE-002; TC-UI-ZONE-005; ACPT-007 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.5 `FR-DET`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-DET-001` | Receive structured person detections | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker detection pipeline; backend/app/modules/ai_integration | Contract test → TC-WRK-DET-001–003 | artifacts/tests/worker/ + artifacts/evaluation/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-DET-002` | Preserve detection provenance | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker detection pipeline; backend/app/modules/ai_integration | System test → TC-WRK-DET-001; exact provenance-field contract assertion `TBD` | artifacts/tests/worker/ + artifacts/evaluation/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.6 `FR-TRK`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-TRK-001` | Receive or derive track identifiers | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker tracker; backend AI integration/rule state | System test → TC-WRK-TRK-001; TC-WRK-TRK-003 | artifacts/tests/worker/ + artifacts/evaluation/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-TRK-002` | Track-loss handling | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker tracker; backend AI integration/rule state | System test → TC-WRK-TRK-002; TC-RULE-LOIT-004 | artifacts/tests/worker/ + artifacts/evaluation/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.7 `FR-RULE`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-RULE-001` | Create a rule configuration | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001–004 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/rules; frontend/src/features/rules | System test → TC-API-RULE-001–003; TC-UI-RULE-001–003 | artifacts/tests/unit/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-RULE-002` | Enable and disable rules | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001–004 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/rules; frontend/src/features/rules | System test → TC-API-RULE-005; TC-RULE-INT-005; ACPT-008 | artifacts/tests/unit/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-RULE-003` | Rule configuration validation | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001–004 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/rules; frontend/src/features/rules | System test → TC-API-RULE-002–003; TC-UI-RULE-003 | artifacts/tests/unit/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-RULE-004` | Deterministic rule evaluation | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001–004 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/rules; frontend/src/features/rules | Unit test → TC-RULE-INT-001–006; TC-RULE-LOIT-001–005; TC-RULE-CROWD-001–005 | artifacts/tests/unit/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-RULE-005` | Rule evaluation audit context | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001–004 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/rules; frontend/src/features/rules | System test → TC-DB-EVT-001–003; exact rule-context snapshot assertion `TBD` | artifacts/tests/unit/ + artifacts/tests/api/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.8 `FR-INT`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-INT-001` | Restricted-zone entry evaluation | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001; UC-EVT-001 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule engine + events; AI track observations | System test → TC-RULE-INT-001–002,004 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-INT-002` | Restricted-area intrusion event | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001; UC-EVT-001 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule engine + events; AI track observations | System test → TC-RULE-INT-002; TC-E2E-INT-001; ACPT-009 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-INT-003` | Intrusion duplicate suppression | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-001; UC-EVT-001 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule engine + events; AI track observations | System test → TC-RULE-INT-003–004; ACPT-009 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.9 `FR-LOIT`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-LOIT-001` | Loitering duration tracking | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-002; UC-EVT-002 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule-state/timer logic + events | System test → TC-RULE-LOIT-001–004 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-LOIT-002` | Loitering event threshold | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-002; UC-EVT-002 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule-state/timer logic + events | System test → TC-RULE-LOIT-001–002; TC-E2E-LOIT-001 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-LOIT-003` | Loitering timer reset semantics | `TBD_SCOPE` / `MUST` | UC-RULE-002; UC-EVT-002 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule-state/timer logic + events | System test → TC-RULE-LOIT-003–004 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-LOIT-004` | Loitering duplicate suppression | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-002; UC-EVT-002 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend rule-state/timer logic + events | System test → TC-RULE-LOIT-005; TC-E2E-LOIT-001 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.10 `FR-CROWD`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-CROWD-001` | Crowd count calculation | `TBD_SCOPE` / `MUST` | UC-RULE-003; UC-EVT-003 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend count/rule-state logic + events | System test → TC-RULE-CROWD-001–005; exact reference-count test depends on counting semantics | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CROWD-002` | Crowd-threshold event | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-003; UC-EVT-003 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend count/rule-state logic + events | System test → TC-RULE-CROWD-002–003; TC-E2E-CROWD-001 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CROWD-003` | Crowd-event duplicate suppression | `CONFIRMED_SCOPE` / `MUST` | UC-RULE-003; UC-EVT-003 | 04-system-architecture.md; 05-uml-and-system-models.md; 06-database-design.md; 08-ai-ml-design.md; PLANNED: backend count/rule-state logic + events | System test → TC-RULE-CROWD-004–005; TC-E2E-CROWD-001 | artifacts/tests/unit/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.11 `FR-VIO`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-VIO-001` | Violence/fighting inference request | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 07-api-specification.md; 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker violence pipeline; backend event criterion | AI worker integration test → TC-WRK-VIO-001–002 | artifacts/evaluation/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-VIO-002` | Violence/fighting result contract | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 07-api-specification.md; 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker violence pipeline; backend event criterion | Contract test → TC-WRK-VIO-001–004 | artifacts/evaluation/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-VIO-003` | Violence/fighting event criterion | `TBD_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 07-api-specification.md; 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker violence pipeline; backend event criterion | System test → EVAL-VIO-* threshold evaluation; TC-E2E-VIO-001–002 | artifacts/evaluation/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-VIO-004` | Violence/fighting event provenance | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 07-api-specification.md; 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker violence pipeline; backend event criterion | System test → TC-WRK-VIO-001; TC-UI-EDTL-004; exact DB provenance assertion `TBD` | artifacts/evaluation/ + artifacts/tests/e2e/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-VIO-005` | Violence inference failure distinction | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 07-api-specification.md; 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker violence pipeline; backend event criterion | Fault-injection test → TC-WRK-VIO-002–003; TC-E2E-WRK-001 | artifacts/evaluation/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.12 `FR-EVT`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-EVT-001` | Persist domain events | `CONFIRMED_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → TC-DB-EVT-001–003; TC-E2E-INT-001 | artifacts/tests/database/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVT-002` | Event occurrence time | `CONFIRMED_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → TC-API-EVT-006; exact occurrence-time assertion `TBD` | artifacts/tests/database/ + artifacts/tests/api/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-EVT-003` | Event type | `CONFIRMED_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → TC-API-EVT-003; TC-API-EVT-006 | artifacts/tests/database/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVT-004` | Event retrieval | `CONFIRMED_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → TC-API-EVT-001–005; TC-UI-EVT-001–005 | artifacts/tests/database/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVT-005` | Event status | `TBD_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → Event lifecycle test `TBD` — lifecycle not yet baselined | artifacts/tests/database/ + artifacts/tests/api/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |
| `FR-EVT-006` | Event-state transition history | `TBD_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → Event status-history persistence test `TBD` — lifecycle not yet baselined | artifacts/tests/database/ + artifacts/tests/api/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |
| `FR-EVT-007` | Duplicate event policy | `CONFIRMED_SCOPE` / `MUST` | UC-EVT-001–007; UC-HIST-002 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/events; DB event/context tables | System test → TC-RULE-INT-003; TC-RULE-LOIT-005; TC-RULE-CROWD-004; duplicate policy tests for violence/offline | artifacts/tests/database/ + artifacts/tests/api/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.13 `FR-ALT`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-ALT-001` | Create operator-facing alert representation | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-EVT-006–007; UC-SYS-004 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend event/ack services; realtime broadcaster; frontend events | System test → TC-UI-EVT-001,004–005; TC-E2E-INT-001 | artifacts/tests/realtime/ + artifacts/tests/frontend/ + DB evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ALT-002` | Deliver new alert information to connected clients | `PROPOSED_SCOPE` / `MUST` | UC-MON-001; UC-EVT-006–007; UC-SYS-004 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend event/ack services; realtime broadcaster; frontend events | System test → TC-WS-001–004; TC-E2E-WS-001; ACPT-017 | artifacts/tests/realtime/ + artifacts/tests/frontend/ + DB evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ALT-003` | Alert presentation minimum context | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-EVT-006–007; UC-SYS-004 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend event/ack services; realtime broadcaster; frontend events | UI system test → TC-UI-EVT-001,004–005; TC-UI-EDTL-001–005 | artifacts/tests/realtime/ + artifacts/tests/frontend/ + DB evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ALT-004` | Acknowledge eligible event/alert | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-EVT-006–007; UC-SYS-004 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend event/ack services; realtime broadcaster; frontend events | System test → TC-DB-ACK-001–002; TC-UI-ACK-001–003; ACPT-011 | artifacts/tests/realtime/ + artifacts/tests/frontend/ + DB evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ALT-005` | Persistent acknowledgement state | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-EVT-006–007; UC-SYS-004 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend event/ack services; realtime broadcaster; frontend events | Integration test → TC-DB-ACK-003; TC-UI-ACK-004; ACPT-012 | artifacts/tests/realtime/ + artifacts/tests/frontend/ + DB evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-ALT-006` | False-positive feedback | `PROPOSED_SCOPE` / `SHOULD` | UC-MON-001; UC-EVT-006–007; UC-SYS-004 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend event/ack services; realtime broadcaster; frontend events | System test → Dedicated false-positive feedback API/UI test `TBD` | artifacts/tests/realtime/ + artifacts/tests/frontend/ + DB evidence | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.14 `FR-EVD`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-EVD-001` | Associate evidence with event | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-SYS-003 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/evidence; protected media store; frontend evidence viewer | System test → TC-DB-EVD-001; TC-UI-EVD-001–004 | artifacts/tests/database/ + artifacts/security/ + UI evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVD-002` | Evidence snapshot | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-SYS-003 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/evidence; protected media store; frontend evidence viewer | System test → TC-DB-EVD-002; TC-UI-EVD-001; ACPT-010 | artifacts/tests/database/ + artifacts/security/ + UI evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVD-003` | Evidence clip | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-SYS-003 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/evidence; protected media store; frontend evidence viewer | System test → TC-DB-EVD-002; TC-UI-EVD-002; ACPT-010 | artifacts/tests/database/ + artifacts/security/ + UI evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVD-004` | Protected evidence access | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-SYS-003 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/evidence; protected media store; frontend evidence viewer | Security test → SEC-EVD-001–004; TC-UI-EVD-005; ACPT-018 | artifacts/tests/database/ + artifacts/security/ + UI evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-EVD-005` | Evidence integrity reference | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-SYS-003 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/evidence; protected media store; frontend evidence viewer | System test → Evidence checksum/integrity test `TBD` | artifacts/tests/database/ + artifacts/security/ + UI evidence | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-EVD-006` | Evidence retention/deletion behavior | `TBD_SCOPE` / `MUST` | UC-EVD-001; UC-SYS-003 | 04-system-architecture.md; 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/evidence; protected media store; frontend evidence viewer | Document review + system test → Evidence retention/deletion lifecycle test `TBD` | artifacts/tests/database/ + artifacts/security/ + UI evidence | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |

## 5.15 `FR-INC`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-INC-001` | Incident concept | `TBD_SCOPE` / `MUST` | `TBD` — event/incident relationship unresolved | 01-vision-and-scope.md; 06-database-design.md — relationship remains `TBD`; NO IMPLEMENTATION TARGET YET — domain relationship `TBD` | System test → No executable test yet — incident concept remains `TBD_SCOPE` | TBD after incident semantics are approved | `BLOCKED_BY_DOMAIN_DECISION` / `NOT_YET_VERIFIED` |

## 5.16 `FR-HIST`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-HIST-001` | List historical events | `CONFIRMED_SCOPE` / `MUST` | UC-HIST-001–002 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: events query service + frontend event history | System test → TC-API-EVT-001; TC-UI-EVT-001; ACPT-013 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-HIST-002` | Filter events by time range | `CONFIRMED_SCOPE` / `MUST` | UC-HIST-001–002 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: events query service + frontend event history | System test → Dedicated time-range API/UI filter test `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-HIST-003` | Filter events by event type | `CONFIRMED_SCOPE` / `MUST` | UC-HIST-001–002 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: events query service + frontend event history | System test → TC-API-EVT-003; TC-UI-EVT-002; ACPT-014 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-HIST-004` | Filter events by source | `CONFIRMED_SCOPE` / `MUST` | UC-HIST-001–002 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: events query service + frontend event history | System test → TC-API-EVT-002; TC-UI-EVT-002; ACPT-014 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-HIST-005` | Filter by acknowledgement/status | `PROPOSED_SCOPE` / `MUST` | UC-HIST-001–002 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: events query service + frontend event history | System test → TC-API-EVT-004; TC-UI-EVT-004 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-HIST-006` | Pagination or bounded result retrieval | `PROPOSED_SCOPE` / `SHOULD` | UC-HIST-001–002 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: events query service + frontend event history | System test → TC-API-PAGE-001–004 | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.17 `FR-ANL`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-ANL-001` | Analytics from persisted data | `CONFIRMED_SCOPE` / `MUST` | UC-ANL-001 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/analytics; frontend analytics | System test → TC-UI-DASH-001–005; ACPT-023; dedicated analytics API test `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-ANL-002` | Event count by type | `CONFIRMED_SCOPE` / `MUST` | UC-ANL-001 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/analytics; frontend analytics | System test → ACPT-023; dedicated analytics-by-type API/UI assertion `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-ANL-003` | Event activity over time | `CONFIRMED_SCOPE` / `SHOULD` | UC-ANL-001 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/analytics; frontend analytics | System test → ACPT-023; dedicated timeseries API/UI assertion `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-ANL-004` | Event count by camera/source | `CONFIRMED_SCOPE` / `SHOULD` | UC-ANL-001 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/analytics; frontend analytics | System test → ACPT-023; dedicated analytics-by-camera assertion `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-ANL-005` | Acknowledgement analytics | `PROPOSED_SCOPE` / `SHOULD` | UC-ANL-001 | 06-database-design.md; 07-api-specification.md; 12-ui-ux-specification.md; PLANNED: backend/app/modules/analytics; frontend analytics | System test → ACPT-023; acknowledgement-analytics assertion `TBD` | artifacts/tests/api/ + artifacts/tests/frontend/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.18 `FR-AUD`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-AUD-001` | Audit security-sensitive user actions | `PROPOSED_SCOPE` / `SHOULD` | UC-ADM-001 | 06-database-design.md; 07-api-specification.md; 13-security-and-privacy.md; PLANNED/PROPOSED: backend/app/modules/audit; DB audit table | Security test → Security/audit integration test `TBD` — audit feature remains proposed | artifacts/security/ + DB/API test evidence | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-AUD-002` | Audit acknowledgement | `PROPOSED_SCOPE` / `SHOULD` | UC-ADM-001 | 06-database-design.md; 07-api-specification.md; 13-security-and-privacy.md; PLANNED/PROPOSED: backend/app/modules/audit; DB audit table | System test → Acknowledgement-to-audit linkage test `TBD` | artifacts/security/ + DB/API test evidence | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.19 `FR-UI`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-UI-001` | Display system navigation | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-HIST-001–002; UC-ANL-001; configuration UCs as applicable | 12-ui-ux-specification.md; 07-api-specification.md; PLANNED: frontend application shell/shared/domain components | System test → TC-UI-SHELL-001–002 | artifacts/tests/frontend/ + screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-UI-002` | Loading state | `CONFIRMED_SCOPE` / `SHOULD` | UC-MON-001; UC-HIST-001–002; UC-ANL-001; configuration UCs as applicable | 12-ui-ux-specification.md; 07-api-specification.md; PLANNED: frontend application shell/shared/domain components | System test → TC-UI-DASH-002; component loading-state tests across pages | artifacts/tests/frontend/ + screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-UI-003` | Error state | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-HIST-001–002; UC-ANL-001; configuration UCs as applicable | 12-ui-ux-specification.md; 07-api-specification.md; PLANNED: frontend application shell/shared/domain components | System test → TC-UI-DASH-004; TC-UI-EVT-003/section errors; dedicated global error-state checks | artifacts/tests/frontend/ + screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-UI-004` | Empty state | `CONFIRMED_SCOPE` / `SHOULD` | UC-MON-001; UC-HIST-001–002; UC-ANL-001; configuration UCs as applicable | 12-ui-ux-specification.md; 07-api-specification.md; PLANNED: frontend application shell/shared/domain components | System test → TC-UI-DASH-003; TC-UI-EVT-003 | artifacts/tests/frontend/ + screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-UI-005` | Connection state | `TBD_SCOPE` / `SHOULD` | UC-MON-001; UC-HIST-001–002; UC-ANL-001; configuration UCs as applicable | 12-ui-ux-specification.md; 07-api-specification.md; PLANNED: frontend application shell/shared/domain components | System test → TC-WS-REC-001–004; TC-REC-UI-001; ACPT-017 | artifacts/tests/frontend/ + screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.20 `FR-INTG`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-INTG-001` | AI-worker/backend structured contract | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001–002 | 04-system-architecture.md; 07-api-specification.md; 08-ai-ml-design.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/ai_integration; ai_worker transport adapter | System test → TC-WRK-DET-001–003; TC-WRK-VIO-001–004; malformed-result tests | artifacts/tests/worker/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-INTG-002` | Correlation of processing jobs | `PROPOSED_SCOPE` / `SHOULD` | UC-AI-001–002; UC-SYS-001–002 | 04-system-architecture.md; 07-api-specification.md; 08-ai-ml-design.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/ai_integration; ai_worker transport adapter | System test → Correlation-ID contract/log assertion `TBD`; NFR-OBS-002 verification | artifacts/tests/worker/ + artifacts/tests/e2e/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `FR-INTG-003` | Malformed worker result handling | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001–002 | 04-system-architecture.md; 07-api-specification.md; 08-ai-ml-design.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/ai_integration; ai_worker transport adapter | Fault-injection test → SEC-WRK-001–005; malformed worker result tests | artifacts/tests/worker/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `FR-INTG-004` | Worker-unavailable behavior | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001–002 | 04-system-architecture.md; 07-api-specification.md; 08-ai-ml-design.md; 13-security-and-privacy.md; PLANNED: backend/app/modules/ai_integration; ai_worker transport adapter | Integration test → TC-WRK-FAIL-001–002; TC-REC-WRK-001; ACPT-016 | artifacts/tests/worker/ + artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.21 `FR-CFG`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-CFG-001` | Externalized runtime configuration | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting system setup; no single user-facing UC | 04-system-architecture.md; 13-security-and-privacy.md; future 16-deployment-guide.md; PLANNED: backend/core configuration; frontend/runtime config; .env.example | Inspection + integration test → SEC-CFG-001; ACPT-001; clean-environment startup test | clean-environment startup evidence + config review | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `FR-CFG-002` | Documented configuration keys | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting system setup; no single user-facing UC | 04-system-architecture.md; 13-security-and-privacy.md; future 16-deployment-guide.md; PLANNED: backend/core configuration; frontend/runtime config; .env.example | Document review → Document review + clean-environment setup test | clean-environment startup evidence + config review | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |

## 5.22 `FR-DEMO`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `FR-DEMO-001` | Reproducible recorded-video test path | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-005 | 03-use-case-specification.md; 14-test-plan.md; PLANNED: deterministic replay fixture + integrated demo path | System test → TC-E2E-INT-001; ACPT-009; clean-environment replay | artifacts/tests/e2e/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.23 `MLR-MOD`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-MOD-001` | Model identity and version | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: models/registry; AI worker model loader | Inspection + integration test → Model-card/registry review; worker model-version contract assertion | models/registry/ + artifacts/evaluation/ | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-MOD-002` | Model-source provenance | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: models/registry; AI worker model loader | Document review → Model-card source/provenance review; checksum/source evidence | models/registry/ + artifacts/evaluation/ | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |

## 5.24 `MLR-DATA`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-DATA-001` | Dataset registry | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; model-evaluation workflow | 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: data/manifests; scripts/data; dataset registry | Document review → Document review: 10-dataset-registry.md | data/manifests/ + dataset review evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-DATA-002` | Dataset acquisition provenance | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; model-evaluation workflow | 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: data/manifests; scripts/data; dataset registry | Document review → Document review: 09-dataset-acquisition.md + acquisition manifests | data/manifests/ + dataset review evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-DATA-003` | Train/validation/test separation | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; model-evaluation workflow | 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: data/manifests; scripts/data; dataset registry | Document review + model evaluation → Dataset split-manifest validation + final evaluation review | data/manifests/ + dataset review evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-DATA-004` | Duplicate leakage check | `CONFIRMED_SCOPE` / `SHOULD` | UC-AI-002; model-evaluation workflow | 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: data/manifests; scripts/data; dataset registry | Model evaluation → Leakage-validation script/test `TBD` | data/manifests/ + dataset review evidence | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `MLR-DATA-005` | Dataset usage limitations | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; model-evaluation workflow | 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: data/manifests; scripts/data; dataset registry | Document review → Dataset registry/model-card limitation review | data/manifests/ + dataset review evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |

## 5.25 `MLR-DET`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-DET-001` | Person detection capability | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: detector experiment/evaluation scripts + ai_worker detector | AI worker integration test → TC-WRK-DET-001–002; EVAL-DET-* | artifacts/evaluation/EVAL-DET-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-DET-002` | Person detector evaluation | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: detector experiment/evaluation scripts + ai_worker detector | Model evaluation → EVAL-DET-*; TC-PERF-DET-001 | artifacts/evaluation/EVAL-DET-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-DET-003` | Detector threshold provenance | `TBD_SCOPE` / `MUST` | UC-AI-001 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: detector experiment/evaluation scripts + ai_worker detector | Model evaluation → Detector threshold-sweep evidence `EVAL-DET-*` | artifacts/evaluation/EVAL-DET-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.26 `MLR-TRK`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-TRK-001` | Tracking capability | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: tracker experiment/evaluation + ai_worker tracker | AI worker integration test → TC-WRK-TRK-001–003 | artifacts/evaluation/EVAL-TRK-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-TRK-002` | Tracker evaluation | `CONFIRMED_SCOPE` / `SHOULD` | UC-AI-001 | 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: tracker experiment/evaluation + ai_worker tracker | Model evaluation → EVAL-TRK-*; TC-PERF-TRK-001 | artifacts/evaluation/EVAL-TRK-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.27 `MLR-VIO`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-VIO-001` | Temporal violence/fighting model | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: violence training/evaluation pipeline + ai_worker model | Model evaluation → EVAL-VIO-* model-card task-definition review | artifacts/evaluation/EVAL-VIO-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-VIO-002` | Violence dataset fitness assessment | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: violence training/evaluation pipeline + ai_worker model | Document review → EVAL-VIO-* preprocessing/window contract tests | artifacts/evaluation/EVAL-VIO-*/ | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-VIO-003` | Violence model baseline | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: violence training/evaluation pipeline + ai_worker model | Model evaluation → EVAL-VIO-* reproducible baseline execution | artifacts/evaluation/EVAL-VIO-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-VIO-004` | Violence model evaluation metrics | `CONFIRMED_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: violence training/evaluation pipeline + ai_worker model | Model evaluation → EVAL-VIO-* confusion matrix + precision/recall/F1 | artifacts/evaluation/EVAL-VIO-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-VIO-005` | Violence threshold provenance | `TBD_SCOPE` / `MUST` | UC-AI-002; UC-EVT-004 | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: violence training/evaluation pipeline + ai_worker model | Model evaluation → EVAL-VIO-* threshold calibration on validation split | artifacts/evaluation/EVAL-VIO-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-VIO-006` | Violence false-positive review | `CONFIRMED_SCOPE` / `SHOULD` | UC-AI-002; UC-EVT-004 | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: violence training/evaluation pipeline + ai_worker model | Model evaluation → EVAL-VIO-* false-positive/false-negative analysis | artifacts/evaluation/EVAL-VIO-*/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.28 `MLR-INF`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-INF-001` | Inference failure reporting | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker inference runtime + backend contract adapter | Fault-injection test → TC-WRK-DET-001–003; TC-WRK-VIO-001–004 | artifacts/tests/worker/ + artifacts/performance/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-INF-002` | Inference input preprocessing traceability | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker inference runtime + backend contract adapter | Inspection → TC-WRK-VIO-002–003; TC-WRK-DET-003; TC-WRK-FAIL-001 | artifacts/tests/worker/ + artifacts/performance/ | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-INF-003` | Inference latency measurement | `CONFIRMED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker inference runtime + backend contract adapter | Performance test → TC-PERF-DET-001; TC-PERF-VIO-001; TC-PERF-WRK-001 | artifacts/tests/worker/ + artifacts/performance/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-INF-004` | Model loading strategy | `PROPOSED_SCOPE` / `MUST` | UC-AI-001–002; UC-SYS-001 | 07-api-specification.md; 08-ai-ml-design.md; 11-model-card-and-evaluation.md; PLANNED: ai_worker inference runtime + backend contract adapter | Inspection + performance test → Worker startup/model-load test `TBD`; TC-WRK-VIO-003 partial | artifacts/tests/worker/ + artifacts/performance/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.29 `MLR-EXP`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-EXP-001` | Experiment reproducibility record | `CONFIRMED_SCOPE` / `MUST` | Model-evaluation workflow; no separate end-user UC | 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: experiment records/artifacts/evaluation scripts | Document review → Experiment-record/document review + reproducibility rerun | experiment config/log/artifact bundle | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `MLR-EXP-002` | Randomness control | `CONFIRMED_SCOPE` / `SHOULD` | Model-evaluation workflow; no separate end-user UC | 08-ai-ml-design.md; 10-dataset-registry.md; 11-model-card-and-evaluation.md; PLANNED: experiment records/artifacts/evaluation scripts | Model evaluation → Environment/commit/config evidence review | experiment config/log/artifact bundle | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.30 `MLR-LIC`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `MLR-LIC-001` | AI dependency license review | `CONFIRMED_SCOPE` / `MUST` | Model/data governance; no end-user UC | 08-ai-ml-design.md; 09-dataset-acquisition.md; 10-dataset-registry.md; PLANNED: model/dataset registry metadata + ADR/license review | Document review → License/source review in model/dataset registry + ADR | license/ADR/model-registry evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |

## 5.31 `NFR-SEC`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-SEC-001` | Secrets shall not be committed | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Inspection + secret scan → SEC-LOG-001; SEC-CFG-001; repository secret scan/review | artifacts/security/ | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-SEC-002` | Protected resource authorization | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Security test → SEC-AUTHZ-001–004; ACPT-019 | artifacts/security/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-SEC-003` | Password handling | `TBD_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Security test → Password-storage/auth tests `TBD_IF_LOCAL_PASSWORD_AUTH` | artifacts/security/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |
| `NFR-SEC-004` | Authentication token confidentiality | `TBD_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Inspection + security test → Token/session confidentiality test `TBD_AFTER_AUTH_SELECTION` | artifacts/security/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |
| `NFR-SEC-005` | Input validation | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | API/contract test → SEC-INJ-001; API validation tests | artifacts/security/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-SEC-006` | Path traversal protection | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Security test → SEC-PATH-001 | artifacts/security/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-SEC-007` | Error information exposure | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Security test → API error-envelope tests; SEC-AUTH-004; TC-API-HLT-002 | artifacts/security/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-SEC-008` | Dependency version recording | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Inspection → SEC-DEP-001; dependency audit evidence | artifacts/security/ | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-SEC-009` | Evidence access control | `CONFIRMED_SCOPE` / `MUST` | All protected UCs; especially UC-AUTH-001, UC-EVD-001, configuration UCs | 13-security-and-privacy.md; 07-api-specification.md; 12-ui-ux-specification.md; CROSS-CUTTING: backend, frontend, worker, DB, media, deployment | Security test → SEC-EVD-001–004; ACPT-018 | artifacts/security/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.32 `NFR-PERF`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-PERF-001` | Event-to-client latency measurement | `TBD_SCOPE` / `MUST` | UC-MON-001; UC-EVT-001–005; UC-HIST-001 | 04-system-architecture.md; 11-model-card-and-evaluation.md; 14-test-plan.md; CROSS-CUTTING: worker, backend, realtime, measurement instrumentation | Performance test → TC-PERF-E2E-001 | artifacts/performance/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-PERF-002` | API latency measurement | `CONFIRMED_SCOPE` / `SHOULD` | UC-MON-001; UC-EVT-001–005; UC-HIST-001 | 04-system-architecture.md; 11-model-card-and-evaluation.md; 14-test-plan.md; CROSS-CUTTING: worker, backend, realtime, measurement instrumentation | Performance test → Dedicated API latency benchmark `TBD` | artifacts/performance/ | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |
| `NFR-PERF-003` | Non-blocking long-running AI work | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-EVT-001–005; UC-HIST-001 | 04-system-architecture.md; 11-model-card-and-evaluation.md; 14-test-plan.md; CROSS-CUTTING: worker, backend, realtime, measurement instrumentation | Architecture inspection + performance test → Architecture/code inspection + TC-PERF-WRK-001; no long-running inference in request handler | artifacts/performance/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-PERF-004` | Bounded history responses | `PROPOSED_SCOPE` / `SHOULD` | UC-MON-001; UC-EVT-001–005; UC-HIST-001 | 04-system-architecture.md; 11-model-card-and-evaluation.md; 14-test-plan.md; CROSS-CUTTING: worker, backend, realtime, measurement instrumentation | System test → TC-API-PAGE-001–004 | artifacts/performance/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.33 `NFR-REL`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-REL-001` | Explicit component health | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-001–004; UC-EVT-006 | 04-system-architecture.md; 07-api-specification.md; 12-ui-ux-specification.md; 14-test-plan.md; CROSS-CUTTING: health, recovery, persistence, realtime | Integration test → TC-API-HLT-001–002; TC-WRK-FAIL-001–002; ACPT-001/016 | artifacts/tests/recovery/ + e2e evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-REL-002` | No silent AI failure | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-001–004; UC-EVT-006 | 04-system-architecture.md; 07-api-specification.md; 12-ui-ux-specification.md; 14-test-plan.md; CROSS-CUTTING: health, recovery, persistence, realtime | Fault-injection test → TC-WRK-DET-003; TC-WRK-VIO-002–003; TC-E2E-WRK-001 | artifacts/tests/recovery/ + e2e evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-REL-003` | Persistent event durability | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-001–004; UC-EVT-006 | 04-system-architecture.md; 07-api-specification.md; 12-ui-ux-specification.md; 14-test-plan.md; CROSS-CUTTING: health, recovery, persistence, realtime | Integration test → TC-DB-EVT-001–003; TC-E2E-INT-001 | artifacts/tests/recovery/ + e2e evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-REL-004` | Idempotent acknowledgement behavior | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-001–004; UC-EVT-006 | 04-system-architecture.md; 07-api-specification.md; 12-ui-ux-specification.md; 14-test-plan.md; CROSS-CUTTING: health, recovery, persistence, realtime | API test → TC-DB-ACK-002–003; TC-UI-ACK-004 | artifacts/tests/recovery/ + e2e evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-REL-005` | Recoverable client connection | `TBD_SCOPE` / `SHOULD` | UC-SYS-001–004; UC-EVT-006 | 04-system-architecture.md; 07-api-specification.md; 12-ui-ux-specification.md; 14-test-plan.md; CROSS-CUTTING: health, recovery, persistence, realtime | System test → TC-WS-REC-001–004; TC-E2E-WS-001 | artifacts/tests/recovery/ + e2e evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.34 `NFR-PRIV`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-PRIV-001` | No facial identification | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-AI-001–002; demo/data workflows | 13-security-and-privacy.md; 09-dataset-acquisition.md; 10-dataset-registry.md; CROSS-CUTTING: media/data/model/UI handling | Inspection → Security/privacy inspection: no facial recognition code/UI/model; repository review | privacy review + data/model registry evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-PRIV-002` | Minimum evidence retention | `TBD_SCOPE` / `MUST` | UC-EVD-001; UC-AI-001–002; demo/data workflows | 13-security-and-privacy.md; 09-dataset-acquisition.md; 10-dataset-registry.md; CROSS-CUTTING: media/data/model/UI handling | Document review → Retention-policy review + evidence deletion test `TBD` | privacy review + data/model registry evidence | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |
| `NFR-PRIV-003` | Demo footage provenance | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-AI-001–002; demo/data workflows | 13-security-and-privacy.md; 09-dataset-acquisition.md; 10-dataset-registry.md; CROSS-CUTTING: media/data/model/UI handling | Document review → DATA-SENT-DEMO-V1 provenance/permission review | privacy review + data/model registry evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-PRIV-004` | No sensitive-attribute inference | `CONFIRMED_SCOPE` / `MUST` | UC-EVD-001; UC-AI-001–002; demo/data workflows | 13-security-and-privacy.md; 09-dataset-acquisition.md; 10-dataset-registry.md; CROSS-CUTTING: media/data/model/UI handling | Inspection → Security/privacy inspection: no sensitive-attribute inference | privacy review + data/model registry evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |

## 5.35 `NFR-MAINT`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-MAINT-001` | Module boundaries | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting implementation governance | PROJECT_HANDBOOK.md; AGENTS.md; 04-system-architecture.md; CROSS-CUTTING: repo architecture, docs, code review | Architecture/code review → Architecture/code review against module boundaries | code/doc review evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-MAINT-002` | Consistent domain terminology | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting implementation governance | PROJECT_HANDBOOK.md; AGENTS.md; 04-system-architecture.md; CROSS-CUTTING: repo architecture, docs, code review | Inspection → Documentation/code terminology review | code/doc review evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-MAINT-003` | No undocumented magic thresholds | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting implementation governance | PROJECT_HANDBOOK.md; AGENTS.md; 04-system-architecture.md; CROSS-CUTTING: repo architecture, docs, code review | Inspection → Configuration/code review for undocumented thresholds | code/doc review evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-MAINT-004` | Documentation synchronized with contract changes | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting implementation governance | PROJECT_HANDBOOK.md; AGENTS.md; 04-system-architecture.md; CROSS-CUTTING: repo architecture, docs, code review | Document/code review → PR/document synchronization review | code/doc review evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-MAINT-005` | Reproducible setup | `CONFIRMED_SCOPE` / `MUST` | Cross-cutting implementation governance | PROJECT_HANDBOOK.md; AGENTS.md; 04-system-architecture.md; CROSS-CUTTING: repo architecture, docs, code review | Clean-environment setup test → Clean-environment setup test; ACPT-001 | code/doc review evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.36 `NFR-TEST`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-TEST-001` | Requirement-linked tests | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-005; all acceptance-relevant UCs | 14-test-plan.md; 11-model-card-and-evaluation.md; CROSS-CUTTING: automated/manual test suites | Inspection → 15-requirements-traceability.md + test execution evidence | test execution log + traceability matrix | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-TEST-002` | Deterministic rule tests | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-005; all acceptance-relevant UCs | 14-test-plan.md; 11-model-card-and-evaluation.md; CROSS-CUTTING: automated/manual test suites | Unit/integration test → TC-RULE-INT-001–006; TC-RULE-LOIT-001–005; TC-RULE-CROWD-001–005 | test execution log + traceability matrix | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-TEST-003` | Vertical-slice integration test | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-005; all acceptance-relevant UCs | 14-test-plan.md; 11-model-card-and-evaluation.md; CROSS-CUTTING: automated/manual test suites | Integration/system test → TC-E2E-INT-001; ACPT-009–012 | test execution log + traceability matrix | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.37 `NFR-USAB`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-USAB-001` | Event comprehension | `CONFIRMED_SCOPE` / `MUST` | UC-MON-001; UC-EVD-001; UC-HIST-001; UC-ANL-001 | 12-ui-ux-specification.md; 14-test-plan.md; PLANNED: frontend UX/accessibility/responsive behavior | Usability/system test → UX-TC-001–003; TC-UI-EVT-*; TC-UI-EDTL-* | artifacts/tests/frontend/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-USAB-002` | Status distinction | `CONFIRMED_SCOPE` / `SHOULD` | UC-MON-001; UC-EVD-001; UC-HIST-001; UC-ANL-001 | 12-ui-ux-specification.md; 14-test-plan.md; PLANNED: frontend UX/accessibility/responsive behavior | UI system test → TC-UI-LIVE-003–005; TC-WS-REC-001; status-component review | artifacts/tests/frontend/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-USAB-003` | Responsive minimum usability | `TBD_SCOPE` / `SHOULD` | UC-MON-001; UC-EVD-001; UC-HIST-001; UC-ANL-001 | 12-ui-ux-specification.md; 14-test-plan.md; PLANNED: frontend UX/accessibility/responsive behavior | System test → Responsive test matrix; ACPT-024 | artifacts/tests/frontend/ + UI screenshots | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.38 `NFR-OBS`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-OBS-001` | Structured diagnostic logging | `CONFIRMED_SCOPE` / `MUST` | UC-SYS-001–003; cross-cutting diagnostics | 04-system-architecture.md; 07-api-specification.md; 13-security-and-privacy.md; PLANNED: structured backend/worker logs + correlation IDs | Inspection + fault test → SEC-LOG-001; logging inspection + worker/backend failure evidence | structured log samples + correlation evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-OBS-002` | Correlation identifier | `PROPOSED_SCOPE` / `SHOULD` | UC-SYS-001–003; cross-cutting diagnostics | 04-system-architecture.md; 07-api-specification.md; 13-security-and-privacy.md; PLANNED: structured backend/worker logs + correlation IDs | System test → Correlation-ID propagation test `TBD` | structured log samples + correlation evidence | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

## 5.39 `NFR-COMPAT`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-COMPAT-001` | Supported browser | `TBD_SCOPE` / `SHOULD` | All frontend/backend runtime UCs | 12-ui-ux-specification.md; future 16-deployment-guide.md; PLANNED: supported browser/runtime matrix + deployment docs | System test → Browser test matrix + ACPT-024 | browser/runtime matrix + clean setup evidence | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-COMPAT-002` | Supported Python version | `TBD_SCOPE` / `MUST` | All frontend/backend runtime UCs | 12-ui-ux-specification.md; future 16-deployment-guide.md; PLANNED: supported browser/runtime matrix + deployment docs | Inspection → Clean-environment runtime test + deployment guide verification | browser/runtime matrix + clean setup evidence | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |

## 5.40 `NFR-DATA`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-DATA-001` | Unique stable identifiers | `CONFIRMED_SCOPE` / `MUST` | All persistence-related UCs | 06-database-design.md; 07-api-specification.md; 14-test-plan.md; PLANNED: DB schema/migrations/transactions/IDs/timestamps | Integration test → TC-DB-FK-001–004 + identifier schema inspection | artifacts/tests/database/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-DATA-002` | Timestamp consistency | `TBD_SCOPE` / `MUST` | All persistence-related UCs | 06-database-design.md; 07-api-specification.md; 14-test-plan.md; PLANNED: DB schema/migrations/transactions/IDs/timestamps | Integration test → Timestamp consistency assertions `TBD`; event/API timestamp review | artifacts/tests/database/ | `BLOCKED_BY_TBD_DECISION` / `NOT_YET_VERIFIED` |
| `NFR-DATA-003` | Transactional event creation | `PROPOSED_SCOPE` / `MUST` | All persistence-related UCs | 06-database-design.md; 07-api-specification.md; 14-test-plan.md; PLANNED: DB schema/migrations/transactions/IDs/timestamps | Integration test → TC-DB-EVT-003; transaction rollback/fault test | artifacts/tests/database/ | `PLANNED_TEST_LINKED` / `NOT_YET_VERIFIED` |

## 5.41 `NFR-ACAD`

| Requirement | Title | Scope / Priority | Use case(s) | Design + planned implementation | Verification + planned test | Expected evidence | Coverage / execution |
|---|---|---|---|---|---|---|---|
| `NFR-ACAD-001` | Measured claims only | `CONFIRMED_SCOPE` / `MUST` | Model evaluation + final reporting; cross-cutting | 11-model-card-and-evaluation.md; PROJECT_HANDBOOK.md; future 18-final-technical-report.md; CROSS-CUTTING: model cards, test evidence, report claims | Document review → Model-card/evaluation artifact review; final report metric cross-check | model card/test report/final report cross-check | `PLANNED_REVIEW_LINKED` / `NOT_YET_VERIFIED` |
| `NFR-ACAD-002` | Implemented-versus-proposed distinction | `CONFIRMED_SCOPE` / `MUST` | Model evaluation + final reporting; cross-cutting | 11-model-card-and-evaluation.md; PROJECT_HANDBOOK.md; future 18-final-technical-report.md; CROSS-CUTTING: model cards, test evidence, report claims | Document review → Final documentation review: CONFIRMED/PROPOSED/TBD distinctions | model card/test report/final report cross-check | `PLANNED_COVERAGE_GAP` / `NOT_YET_VERIFIED` |

---

# 6. Coverage-Gap Register

The following requirements already have design traceability but still need an exact dedicated test/review item, or are blocked by an unresolved domain decision.

This register is intentionally explicit so the team does not discover verification gaps during final-report week.

| Requirement | Scope | Gap / blocked item | Required action before final verification |
|---|---|---|---|
| `FR-AUTH-004` | `TBD_SCOPE` | SEC-AUTH-003; dedicated logout UI/API test `TBD` | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `FR-USER-001` | `PROPOSED_SCOPE` | Document/DB verification + dedicated user-identity persistence test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-USER-002` | `TBD_SCOPE` | SEC-AUTHZ-001–004; exact role-association persistence test `TBD` | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `FR-CAM-003` | `CONFIRMED_SCOPE` | TC-API-CAM-004 covers unknown-ID path; successful detail test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-CAM-004` | `PROPOSED_SCOPE` | Dedicated camera-update API/DB regression test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-ZONE-003` | `CONFIRMED_SCOPE` | Dedicated zone-disable API/UI test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-DET-002` | `CONFIRMED_SCOPE` | TC-WRK-DET-001; exact provenance-field contract assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-RULE-005` | `CONFIRMED_SCOPE` | TC-DB-EVT-001–003; exact rule-context snapshot assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-VIO-004` | `CONFIRMED_SCOPE` | TC-WRK-VIO-001; TC-UI-EDTL-004; exact DB provenance assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-EVT-002` | `CONFIRMED_SCOPE` | TC-API-EVT-006; exact occurrence-time assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-EVT-005` | `TBD_SCOPE` | Event lifecycle test `TBD` — lifecycle not yet baselined | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `FR-EVT-006` | `TBD_SCOPE` | Event status-history persistence test `TBD` — lifecycle not yet baselined | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `FR-ALT-006` | `PROPOSED_SCOPE` | Dedicated false-positive feedback API/UI test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-EVD-005` | `CONFIRMED_SCOPE` | Evidence checksum/integrity test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-EVD-006` | `TBD_SCOPE` | Evidence retention/deletion lifecycle test `TBD` | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `FR-INC-001` | `TBD_SCOPE` | No executable test yet — incident concept remains `TBD_SCOPE` | Resolve event/incident semantics before defining implementation or tests. |
| `FR-HIST-002` | `CONFIRMED_SCOPE` | Dedicated time-range API/UI filter test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-ANL-001` | `CONFIRMED_SCOPE` | TC-UI-DASH-001–005; ACPT-023; dedicated analytics API test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-ANL-002` | `CONFIRMED_SCOPE` | ACPT-023; dedicated analytics-by-type API/UI assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-ANL-003` | `CONFIRMED_SCOPE` | ACPT-023; dedicated timeseries API/UI assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-ANL-004` | `CONFIRMED_SCOPE` | ACPT-023; dedicated analytics-by-camera assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-ANL-005` | `PROPOSED_SCOPE` | ACPT-023; acknowledgement-analytics assertion `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-AUD-001` | `PROPOSED_SCOPE` | Security/audit integration test `TBD` — audit feature remains proposed | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-AUD-002` | `PROPOSED_SCOPE` | Acknowledgement-to-audit linkage test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `FR-INTG-002` | `PROPOSED_SCOPE` | Correlation-ID contract/log assertion `TBD`; NFR-OBS-002 verification | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `MLR-DATA-004` | `CONFIRMED_SCOPE` | Leakage-validation script/test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `MLR-INF-004` | `PROPOSED_SCOPE` | Worker startup/model-load test `TBD`; TC-WRK-VIO-003 partial | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `NFR-SEC-003` | `TBD_SCOPE` | Password-storage/auth tests `TBD_IF_LOCAL_PASSWORD_AUTH` | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `NFR-SEC-004` | `TBD_SCOPE` | Token/session confidentiality test `TBD_AFTER_AUTH_SELECTION` | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `NFR-PERF-002` | `CONFIRMED_SCOPE` | Dedicated API latency benchmark `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `NFR-PRIV-002` | `TBD_SCOPE` | Retention-policy review + evidence deletion test `TBD` | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `NFR-OBS-002` | `PROPOSED_SCOPE` | Correlation-ID propagation test `TBD` | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |
| `NFR-DATA-002` | `TBD_SCOPE` | Timestamp consistency assertions `TBD`; event/API timestamp review | Resolve the governing TBD decision, update authoritative design/API/DB document, then assign the exact test/review item. |
| `NFR-ACAD-002` | `CONFIRMED_SCOPE` | Final documentation review: CONFIRMED/PROPOSED/TBD distinctions | Add the missing dedicated test/review ID to `14-test-plan.md` (or security/model evaluation suite) and link execution evidence here. |

---

# 7. Domain-to-Artifact Traceability

| Domain | Principal authoritative documents | Primary planned implementation area | Primary verification evidence |
|---|---|---|---|
| Authentication / users | `07`, `13`, `12` | backend auth/users + frontend auth | security/API evidence |
| Cameras | `04`, `06`, `07`, `12` | cameras module + UI | API/DB/UI tests |
| Zones | `05`, `06`, `07`, `12` | zones module + SVG/editor UI | geometry/API/UI tests |
| Rules | `04`, `06`, `07`, `08` | rule engine | deterministic rule tests |
| Detection / tracking | `07`, `08`, `11` | AI worker | worker + evaluation evidence |
| Violence/fighting | `08`, `10`, `11` | AI worker + event criterion | model evaluation + E2E |
| Events / acknowledgement | `06`, `07`, `12` | events service + DB + UI | DB/API/UI/E2E |
| Evidence | `06`, `07`, `12`, `13` | evidence service/store | DB/UI/security tests |
| History / analytics | `06`, `07`, `12` | query/analytics services + UI | API/UI tests |
| Security/privacy | `13` | cross-cutting | `artifacts/security/` |
| Configuration/deployment | `04`, `13`, future `16` | core/config/infra | clean-environment test |
| Academic/model claims | `10`, `11`, `14`, future `18` | evidence/reporting workflow | model/test/report cross-check |

---

# 8. Requirement-to-Evidence Rules

## 8.1 Unit/module requirement

Expected evidence may include:

```text
automated test output
test log
coverage of the specific branch/behavior
```

## 8.2 API requirement

Expected evidence should include:

```text
request
response/status
contract assertion
negative case where applicable
```

## 8.3 Database requirement

Expected evidence should include:

```text
migration/schema state
transaction/assertion result
persistence/read-back verification
```

## 8.4 UI requirement

Expected evidence may include:

```text
automated interaction test
manual test record
screenshot
API-backed state verification
```

 A screenshot alone shall not prove persistence or authorization.

## 8.5 AI/model requirement

Expected evidence shall include the relevant:

```text
model ID/version
dataset ID
split manifest
experiment/evaluation ID
metrics artifact
environment
```

## 8.6 Security/privacy requirement

Expected evidence may include:

```text
negative security test
configuration inspection
secret/dependency scan
authorization evidence
privacy/data-registry review
```

---

# 9. Verification State Transition

Recommended lifecycle:

```text
NOT_YET_VERIFIED
→ TEST/REVIEW EXECUTED
→ PASS or FAIL
→ VERIFIED if evidence accepted
```

If code, API, schema, model, threshold, dataset split, or governing requirement changes materially:

```text
VERIFIED
→ INVALIDATED
→ rerun verification
```

---

# 10. Change-Control Rules

## 10.1 Requirement change

If a requirement changes:

1. preserve the stable ID where meaning remains substantially the same;
2. update SRS lifecycle/status;
3. update use-case/design references;
4. identify affected implementation modules;
5. invalidate affected test evidence;
6. rerun verification.

## 10.2 API change

Update:

```text
07-api-specification.md
12-ui-ux-specification.md
14-test-plan.md
this traceability matrix
```

plus implementation/contract tests.

## 10.3 Database change

Update:

```text
06-database-design.md
migration
API schemas if affected
tests
this matrix
```

## 10.4 Model/data change

Update:

```text
08-ai-ml-design.md
10-dataset-registry.md
11-model-card-and-evaluation.md
model/data registry
evaluation evidence
this matrix
```

---

# 11. Baseline Gate

Before this matrix is marked `BASELINED`:

- [ ] all 155 SRS IDs are present;
- [ ] no duplicate requirement ID exists;
- [ ] requirement titles match SRS;
- [ ] all `TBD_SCOPE` requirements are visibly marked;
- [ ] use-case mappings reviewed;
- [ ] design mappings reviewed;
- [ ] planned implementation targets reviewed;
- [ ] every `MUST` requirement has a verification strategy;
- [ ] coverage-gap register reviewed;
- [ ] test-plan gaps are added or explicitly blocked;
- [ ] no requirement is marked verified without evidence;
- [ ] incident semantics remain unimplemented while `FR-INC-001` is unresolved;
- [ ] future document references are labeled as future rather than pretending the files exist.

---

# 12. Final Verification Gate

Before the final technical report claims MVP completion:

- [ ] every `CONFIRMED_SCOPE` + `MUST` requirement is either `VERIFIED` or has an explicitly approved exception;
- [ ] every accepted `PROPOSED_SCOPE` requirement has an updated final status;
- [ ] every `TBD_SCOPE` requirement is resolved, deferred, or explicitly excluded;
- [ ] no failed critical security requirement remains;
- [ ] golden vertical slice is verified;
- [ ] model metrics trace to actual evaluation artifacts;
- [ ] test evidence corresponds to the final code/model/data version;
- [ ] screenshots are not used as substitutes for backend/security evidence;
- [ ] final report only claims implemented and verified behavior.

---

# 13. AI Assistant Traceability Rules

An AI coding assistant shall never:

1. create a new requirement ID merely to justify code already written;
2. renumber an existing requirement referenced by tests/design;
3. mark a requirement `VERIFIED` without execution/review evidence;
4. replace a missing test with a fabricated test ID;
5. infer that a design document proves implementation;
6. infer that implementation proves verification;
7. silently convert `TBD_SCOPE` into implemented behavior;
8. omit a requirement because it is inconvenient;
9. change expected test behavior to match a defect without SRS/design review;
10. claim a model/data/security requirement is satisfied from third-party documentation alone;
11. hide failed or blocked requirements from the matrix;
12. treat planned implementation paths as existing files unless verified.

---

# 14. Final Traceability Rule

> **Sentinel AI shall be able to explain every final project claim by walking backward from evidence to the requirement that justified it.**
>
> The authoritative completion chain is:
>
> ```text
> final claim
> → verification evidence
> → test/review ID
> → implementation/design artifact
> → use case
> → SRS requirement ID
> ```
>
> If any link is missing, the project may still have working code, but the requirement is not yet fully traceable or academically verified.


---

# 19. Violence Requirement Evidence Update — 2026-09-12

The following evidence is now available for the `FR-VIO-*` family.

| Requirement | Model/runtime evidence | Application-level status |
|---|---|---|
| `FR-VIO-001` violence inference request | exact raw-video inference path qualified on controlled fixtures | worker transport/application job dispatch pending |
| `FR-VIO-002` violence result contract | structured model score semantics and model-version identity frozen | backend contract validator pending |
| `FR-VIO-003` violence event criterion | `W1 / stride 1 / 3-of-5 / threshold 0.906` selected on validation and tested once on official TEST | backend rolling-state integration pending |
| `FR-VIO-004` event provenance | exact model/checkpoint/version/dataset lineage established | persistent event provenance assertion pending |
| `FR-VIO-005` failure distinction | API/design requires explicit worker failure; runtime integration package preserves this rule | fault-injection E2E pending |

Therefore:

```text
model/policy qualification != complete FR-VIO application verification
```

The model/runtime evidence may be cited for the AI portions of these
requirements, but the matrix should not mark the entire requirement `VERIFIED`
until the backend/worker/event integration tests also pass.

Evidence source:

`19-violence-model-and-runtime-qualification.md`
