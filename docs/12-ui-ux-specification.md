---
title: "Sentinel AI — UI/UX Specification"
document_id: "SEN-UIUX"
version: "0.1.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
frontend_framework: "TBD"
last_updated: "2026-08-20"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "information architecture"
  - "page structure"
  - "screen behavior"
  - "frontend interaction states"
  - "UI-to-API mapping"
  - "zone editor behavior"
  - "alert and event presentation"
  - "responsive behavior"
  - "accessibility"
  - "loading empty error and reconnect states"
---

# Sentinel AI — UI/UX Specification

> **Document purpose**
>
> This document defines the user-interface and user-experience behavior of Sentinel AI.
>
> It is intended to be implementation-authoritative once baselined.
>
> It defines:
>
> - application information architecture;
> - navigation;
> - page-level requirements;
> - frontend data dependencies;
> - interaction flows;
> - visual hierarchy;
> - camera and event presentation;
> - polygon-zone configuration;
> - rule configuration;
> - evidence review;
> - analytics behavior;
> - loading, empty, error, and reconnect states;
> - responsive behavior;
> - accessibility expectations;
> - frontend state-management boundaries.
>
> This document does **not** select the final frontend framework.
>
> Framework choice remains:
>
> `TBD`
>
> The design shall remain implementable in any modern component-based frontend stack capable of consuming the baselined Sentinel API.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document is authoritative for frontend behavior and UX.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `01-vision-and-scope.md`
3. `02-srs.md`
4. `03-use-case-specification.md`
5. `04-system-architecture.md`
6. `05-uml-and-system-models.md`
7. `07-api-specification.md`
8. accepted ADRs

If this document conflicts with the API specification, the API contract takes precedence and this document shall be updated.

## 0.2 UI status vocabulary

| Status | Meaning |
|---|---|
| `CONFIRMED` | Required UX behavior |
| `PROPOSED` | Candidate interaction/layout |
| `TBD` | Unresolved |
| `DEFERRED` | Future feature |
| `REJECTED` | Explicitly excluded |

## 0.3 Product-positioning rule

Sentinel AI is an **operator-facing monitoring application**, not a decorative AI dashboard.

The interface shall prioritize:

1. current operational awareness;
2. event review;
3. evidence;
4. acknowledgement;
5. camera/rule configuration;
6. history;
7. analytics.

AI model internals are secondary.

---

# 1. UX Goals

## 1.1 UX-GOAL-01 — Immediate operational comprehension

An operator should be able to answer quickly:

- Which camera has an issue/event?
- What happened?
- When did it happen?
- What type of event is it?
- Is evidence available?
- Has anyone acknowledged it?
- Is the system/AI worker degraded?

## 1.2 UX-GOAL-02 — Low ambiguity

The UI shall distinguish:

```text
Detection
Event
Alert
Evidence
Acknowledgement
Camera Health
```

These concepts shall not be visually conflated.

## 1.3 UX-GOAL-03 — Transparent system state

The UI shall clearly show:

- loading;
- empty;
- offline;
- error;
- stale;
- reconnecting;
- unavailable evidence.

## 1.4 UX-GOAL-04 — Reproducible demo flow

The UI shall support the first vertical slice visibly:

```text
camera/source
→ intrusion event appears
→ evidence opens
→ operator acknowledges
→ acknowledgement persists
```

---

# 2. Primary Users

## 2.1 Administrator

Primary UX responsibilities:

- configure cameras;
- draw zones;
- configure rules;
- enable/disable monitoring.

## 2.2 Operator

Primary UX responsibilities:

- monitor events;
- inspect evidence;
- acknowledge;
- search history.

## 2.3 Reviewer / Supervisor

Proposed responsibilities:

- history;
- evidence;
- analytics;
- audit/review.

Exact permissions remain `TBD`.

---

# 3. Information Architecture

Recommended top-level navigation:

```text
Dashboard
Live View
Events
Cameras
Rules
Analytics
AI Models
Audit Log
Settings
```

Status:

| Navigation item | Status |
|---|---|
| Dashboard | `CONFIRMED` |
| Live View | `CONFIRMED` |
| Events | `CONFIRMED` |
| Cameras | `CONFIRMED` |
| Rules | `CONFIRMED` |
| Analytics | `CONFIRMED` |
| AI Models | `PROPOSED` |
| Audit Log | `PROPOSED` |
| Settings | `PROPOSED` |

## 3.1 Incident navigation

A separate `Incidents` page is **not** baselined because the event/incident domain relationship remains unresolved.

Do not add an `Incidents` navigation item until that relationship is defined.

---

# 4. Application Shell

## 4.1 Desktop shell

Recommended structure:

```text
┌───────────────────────────────────────────────────────────┐
│ Top Bar                                                   │
├──────────────┬────────────────────────────────────────────┤
│ Sidebar      │ Main Content                               │
│ Navigation   │                                            │
│              │                                            │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

## 4.2 Sidebar

Should contain:

- product name/logo;
- primary navigation;
- selected-item state;
- system-health indicator;
- current user/account action.

## 4.3 Top bar

May contain:

- current page title;
- contextual actions;
- real-time connection indicator;
- user menu.

---

# 5. Responsive Navigation

## Desktop

Persistent sidebar.

## Tablet

Collapsible sidebar.

## Mobile

Drawer navigation.

The desktop monitoring workflow has priority over a mobile-first surveillance layout because the course demo is expected to be desktop-centric.

Mobile support should remain functional but need not reproduce multi-camera desktop density.

---

# 6. Visual Design Principles

## 6.1 Academic-professional tone

Avoid:

- gaming-style neon effects;
- excessive gradients;
- decorative AI brain imagery;
- overuse of glowing red alerts;
- cinematic surveillance aesthetics.

Prefer:

- restrained interface;
- clear typography;
- consistent spacing;
- neutral surfaces;
- intentional alert emphasis.

## 6.2 Visual hierarchy

Priority order:

```text
Critical operational information
→ current event details
→ user action
→ contextual metadata
→ secondary diagnostics
```

## 6.3 Color semantics

Exact palette: `TBD`.

Semantic use should be consistent:

- critical/error;
- warning;
- healthy/success;
- informational;
- disabled/neutral.

Do not use color alone to communicate status.

---

# 7. Typography

Frontend framework/design system remains `TBD`.

Typography requirements:

- readable sans-serif;
- stable heading hierarchy;
- sufficient contrast;
- no decorative body font;
- tabular numbers where useful for timestamps/metrics.

Recommended hierarchy:

```text
Page title
Section title
Card title
Body
Metadata / caption
```

---

# 8. Iconography

Use one consistent icon family.

Icons should reinforce labels, not replace essential text.

Examples:

```text
camera
alert
clock
user
zone
rule
analytics
settings
```

Do not use ambiguous icons without accessible labels/tooltips.

---

# 9. Global Status Components

## 9.1 System health indicator

Should expose at least:

```text
Healthy
Degraded
Offline / Unavailable
```

Exact codes follow API.

## 9.2 Real-time connection indicator

Proposed states:

```text
Connected
Reconnecting
Disconnected
```

## 9.3 Camera health badge

Should distinguish:

```text
Enabled + Healthy
Enabled + Degraded
Enabled + Offline
Disabled
Unknown
```

---

# 10. Authentication Screen

Status: `TBD_DEPENDING_ON_AUTH_STRATEGY`.

If local login is used, page should include:

- product title;
- username/email field;
- password field;
- submit action;
- invalid-credential state;
- loading state.

Do not expose whether a specific username exists if security design avoids account enumeration.

---

# 11. Dashboard — Purpose

The Dashboard is the operator's overview page.

It should answer:

```text
What needs attention now?
What changed recently?
Which cameras are unavailable?
What event patterns are occurring?
```

---

# 12. Dashboard Layout

Recommended desktop structure:

```text
Page Header
↓
Operational KPI Row
↓
Active / Recent Alerts
↓
Camera Health Summary
↓
Event Trend
↓
Recent Event List
```

---

# 13. Dashboard KPI Cards

Potential cards:

```text
Unacknowledged Events
Events Today / Selected Period
Offline Cameras
Acknowledged Events
```

Exact period semantics: `TBD`.

All values must come from API/persisted data.

No hard-coded demo counters.

---

# 14. Dashboard KPI Interaction

Clicking a KPI should navigate/filter where useful.

Examples:

```text
Unacknowledged Events
→ Events page filtered acknowledged=false
```

```text
Offline Cameras
→ Cameras page filtered health=offline
```

---

# 15. Dashboard Active Alert Area

Show highest-priority recent events.

Each alert card/list item should include:

- event type;
- camera;
- occurrence time;
- acknowledgement state;
- evidence availability;
- action to open.

Optional:

- severity if eventually baselined.

---

# 16. Dashboard Camera Health Summary

Display:

- camera name;
- enabled state;
- health state;
- last frame / last health time where useful.

Avoid showing raw RTSP/local source locator to ordinary operators.

---

# 17. Dashboard Event Trend

A simple time-series chart is sufficient.

Required:

- axis labels;
- time range;
- event count meaning;
- empty state.

Do not add decorative charts without an operational question.

---

# 18. Dashboard Loading State

Use:

- skeleton;
- progress placeholder;
- section-level loading.

Do not block entire page if only one lower-priority analytics widget is loading.

---

# 19. Dashboard Error State

If one widget fails:

- show local error;
- preserve working sections.

If all backend data fails:

- show page-level error and retry.

---

# 20. Dashboard Empty State

If no events exist:

```text
No events recorded for this period.
```

This is not an error.

---

# 21. Live View — Purpose

Live View combines:

- active camera/source visibility;
- configured zones;
- current monitoring state;
- recent event context.

Exact browser video transport remains `TBD`.

---

# 22. Live View Layout

Recommended desktop layout:

```text
┌──────────────────────────────┬─────────────────────┐
│ Video / Camera View          │ Camera Details      │
│                              │ Health              │
│ Zone overlays                │ Active Rules        │
│ Optional detection overlay   │ Recent Events       │
│                              │                     │
└──────────────────────────────┴─────────────────────┘
```

---

# 23. Live View Camera Selector

If multiple cameras exist:

- searchable/selectable list;
- health badge;
- enabled state;
- selected state.

Do not autoplay many heavy streams by default unless performance is proven.

---

# 24. Video Canvas

Must support overlay layers.

Conceptual order:

```text
video
→ zone polygon
→ optional person boxes/tracks
→ event markers
```

## 24.1 Overlay control

Allow operator/admin to toggle:

- zones;
- detections/tracks if shown.

These overlays are operational aids.

---

# 25. Detection Overlay

Status: `PROPOSED`.

If displayed, each detection may show:

```text
Person
Track #N
Detector score
```

Do not show:

```text
Suspect
Threat
Criminal
```

---

# 26. Track Labels

Use temporary neutral terminology:

```text
Track 17
Person #17
```

Never imply identity.

---

# 27. Camera Offline Live View

If source unavailable:

- replace video area with explicit offline state;
- preserve camera metadata;
- show last frame time if available;
- show latest offline event link where useful.

Do not display a frozen frame as though it is current live video.

---

# 28. Camera Disabled Live View

Disabled differs from offline.

Display:

```text
Monitoring disabled
```

rather than:

```text
Camera offline
```

---

# 29. Camera Configuration Page

Purpose:

- create/edit camera source;
- enable/disable;
- inspect health;
- manage zones.

---

# 30. Camera List

Columns/cards:

```text
Name
Source Type
Enabled
Health
Last Frame
Zones
Rules
Actions
```

Do not expose secrets.

---

# 31. Add Camera Form

Fields depend on chosen source type.

Common:

```text
Name
Description
Source Type
Source Locator
Credential Reference if applicable
Enabled
```

## 31.1 Dynamic source fields

Only show fields relevant to selected source kind.

Do not present RTSP credential controls if MVP source is file-only.

---

# 32. Camera Form Validation

Frontend validates:

- required fields;
- obvious syntax;
- empty values.

Backend remains authoritative.

Validation messages should be field-local where possible.

---

# 33. Camera Save States

States:

```text
Idle
Submitting
Success
Validation Error
Server Error
```

Disable repeated submit while request is in flight unless request design supports idempotency.

---

# 34. Camera Detail Page

Suggested sections:

```text
Overview
Health
Zones
Rules
Recent Events
```

Potential tabbed layout.

---

# 35. Zone Editor — Purpose

The zone editor is a major Advanced Web Technologies feature.

It shall allow an authorized user to visually define a polygon over a camera frame/snapshot.

---

# 36. Zone Editor Layout

Recommended:

```text
┌──────────────────────────────────────────────┐
│ Camera Snapshot / Frame                     │
│                                              │
│   polygon overlay                            │
│                                              │
└──────────────────────────────────────────────┘

Zone Name
Zone Type
Enabled
[Reset] [Cancel] [Save]
```

---

# 37. Zone Polygon Creation

Proposed interaction:

1. enter edit mode;
2. click/tap to add vertex;
3. line connects vertices;
4. close polygon by clicking first vertex or explicit `Finish`;
5. show completed polygon;
6. save.

---

# 38. Zone Vertex Editing

After polygon closure:

- vertices may be draggable;
- selected vertex visually emphasized;
- optional remove-vertex action.

Minimum polygon validity must remain enforced.

---

# 39. Zone Coordinate Storage

Frontend should convert display coordinates into normalized values.

Proposed:

```text
x_norm = pointer_x / rendered_video_width
y_norm = pointer_y / rendered_video_height
```

Then send normalized coordinates.

Exact representation remains pending baseline, but normalized coordinates are the current proposed contract.

---

# 40. Zone Resize Behavior

When viewport/video element resizes:

```text
stored normalized coordinates
→ reproject into current display size
```

Polygon should remain aligned.

---

# 41. Zone Editor Geometry Validation

Reject:

- fewer than minimum valid polygon vertices;
- points outside canvas;
- malformed polygon.

Self-intersection policy: `TBD`.

---

# 42. Zone Editor Undo/Reset

At minimum provide:

```text
Reset
```

Optional:

```text
Undo last vertex
```

Useful for usability.

---

# 43. Zone Editor Unsaved Changes

If user navigates away after edits:

proposed:

```text
unsaved changes warning
```

Status: `PROPOSED`.

---

# 44. Zone List

Show:

```text
Name
Type
Enabled
Geometry Version
Associated Camera
Associated Rules
```

Geometry version may be hidden from ordinary operators and shown in admin/details.

---

# 45. Rule Management Page

Purpose:

- create;
- edit;
- enable/disable;
- understand rule configuration.

---

# 46. Rule List

Suggested columns:

```text
Rule Name
Type
Camera
Zone
Enabled
Version
Last Updated
```

---

# 47. Rule Creation — Type Selection

User first chooses:

```text
Restricted Area Intrusion
Loitering
Crowd Threshold
```

Then form changes based on type.

---

# 48. Intrusion Rule Form

Fields eventually include:

```text
Rule Name
Camera
Zone
Enabled
Position Method
Require Transition From Outside
Cooldown / Retrigger Setting
```

Unresolved fields remain hidden/disabled until semantics are finalized.

Do not expose a dropdown whose choices are not backed by a baselined rule contract.

---

# 49. Loitering Rule Form

Fields:

```text
Rule Name
Camera
Zone
Dwell Threshold
Track Loss Grace
Reset on Exit
Retrigger Setting
Enabled
```

Exact defaults: `TBD`.

Use human-friendly time input while API stores milliseconds.

---

# 50. Crowd Rule Form

Fields:

```text
Rule Name
Camera
Zone
Person Threshold
Counting Method
Retrigger Setting
Enabled
```

Counting-method choices remain `TBD`.

---

# 51. Rule Form Units

If API uses milliseconds, UI should display meaningful units:

```text
seconds
minutes
```

and convert explicitly.

Do not display raw milliseconds to ordinary users unless useful.

---

# 52. Rule Validation

Examples:

```text
threshold > 0
zone belongs to camera
required field present
supported counting method
```

Backend remains authoritative.

---

# 53. Event Feed Page

The `Events` page is the primary operational history/feed view.

It combines:

- current recent events;
- filtering;
- acknowledgement state;
- evidence availability.

---

# 54. Event List Structure

Recommended columns/cards:

```text
Time
Type
Camera
Acknowledged
Evidence
Status
Action
```

Optional:

```text
Severity
```

only after severity model exists.

---

# 55. Event Type Labels

Machine:

```text
restricted_area_intrusion
```

UI:

```text
Restricted Area Intrusion
```

Use stable human labels.

---

# 56. Event Type Icons

Optional.

Examples:

- intrusion → boundary/enter icon;
- loitering → clock/person;
- crowd → group;
- violence → alert;
- camera offline → camera-offline icon.

Icons must not carry meaning alone.

---

# 57. Event Filter Bar

Recommended filters:

```text
Date/Time Range
Camera
Event Type
Acknowledged
Status if baselined
```

---

# 58. Event Filter Behavior

Filters should:

- update query state;
- be shareable in URL query parameters if practical;
- have clear reset action.

Status: `PROPOSED`.

---

# 59. Event Pagination

UI consumes cursor pagination.

Controls may be:

```text
Load More
```

or:

```text
Next page
```

Do not expose cursor itself.

---

# 60. Event Sorting

Default:

```text
Newest first
```

No need for many sort modes unless useful.

---

# 61. Event Empty State

Examples:

```text
No events found.
```

or:

```text
No events match the selected filters.
```

---

# 62. Event Error State

Show:

- failure message;
- retry action.

Do not replace failed network response with stale mock data.

---

# 63. Event Detail Page

This is the authoritative operator review screen.

Recommended sections:

```text
Event Summary
Evidence
Event Context
Acknowledgement
Related Camera/Rule
Model Information where relevant
Timeline / Audit where available
```

---

# 64. Event Summary Header

Show prominently:

```text
Event Type
Camera
Occurrence Time
Acknowledgement State
Status
```

Potential:

```text
Severity
```

only if baselined.

---

# 65. Event Evidence Section

Should clearly distinguish:

```text
Available
Pending
Failed
Deleted
No Evidence
```

---

# 66. Evidence Snapshot Viewer

Requirements:

- fit image;
- preserve aspect ratio;
- optional full-screen/zoom;
- accessible alt text.

Do not distort.

---

# 67. Evidence Clip Viewer

Requirements:

- standard playback;
- play/pause;
- seek where browser supports;
- duration;
- loading/error state.

No autoplay with sound.

---

# 68. Evidence Failure State

Example:

```text
Evidence could not be generated for this event.
```

Do not hide the event.

---

# 69. Evidence Pending State

Show:

```text
Evidence processing…
```

Poll/realtime refresh according to implementation.

---

# 70. Event Context — Intrusion

Show:

```text
Rule
Zone
Track ID if useful
Trigger Position / Zone reference
Rule configuration snapshot where useful
```

Do not overwhelm operator with raw coordinate arrays in default view.

---

# 71. Event Context — Loitering

Show:

```text
Observed Dwell Time
Configured Threshold
Zone
Track ID
```

Use human-readable time.

---

# 72. Event Context — Crowd

Show:

```text
Observed Count
Configured Threshold
Counting Method
Zone
```

---

# 73. Event Context — Violence

Show:

```text
Model
Version
Output Label
Model Score
Threshold
Temporal Window
```

If score is uncalibrated, UI label should say:

```text
Model score
```

not:

```text
Probability
```

---

# 74. Event Context — Camera Offline

Show:

```text
Last Frame
Offline Criterion
Reason
Health Transition
```

---

# 75. Acknowledgement Action

Primary action:

```text
Acknowledge
```

After success:

```text
Acknowledged by <user>
<time>
```

---

# 76. Acknowledgement Loading State

Button becomes:

```text
Acknowledging…
```

and prevents duplicate submissions.

---

# 77. Acknowledgement Error

If failed:

- retain prior state;
- show error;
- allow retry.

Do not optimistically mark acknowledged permanently until backend confirms.

---

# 78. Multi-Acknowledgement UI

Because multi-user acknowledgement cardinality remains `TBD`, UI should not assume only one acknowledgement until baselined.

Current proposed display can support:

```text
Acknowledged by N users
```

with details.

---

# 79. False-Positive Feedback

Status: `PROPOSED`.

If implemented:

```text
Mark as False Positive
```

should be a secondary action, not the same as acknowledgement.

Potential confirmation/dialog:

- reason;
- optional notes.

---

# 80. False-Positive Feedback Warning

UI may explain:

```text
This records operator feedback and does not automatically retrain the AI model.
```

---

# 81. History Page

The Events page may serve as history.

A separate `History` page is not required if redundant.

Recommended:

```text
Events = live/recent + searchable historical event list
```

---

# 82. Analytics Page

Purpose:

summarize persisted event activity.

---

# 83. Analytics Layout

Recommended:

```text
Time Range
↓
KPI Summary
↓
Event Trend
↓
Events by Type
↓
Events by Camera
↓
Acknowledgement Summary
```

---

# 84. Analytics Time Range

User should be able to select:

```text
from
to
```

Quick presets are optional.

Avoid unsupported presets if backend query semantics are not ready.

---

# 85. Analytics Event Trend

Use:

- line or bar chart;
- consistent temporal buckets;
- zero/empty state.

---

# 86. Analytics Events by Type

Bar chart or table.

Avoid pie chart if many categories become difficult to compare.

---

# 87. Analytics Events by Camera

Bar chart/table.

Useful for identifying cameras with high event volume.

---

# 88. Analytics Acknowledgement Metrics

Potential:

```text
Acknowledged Events
Unacknowledged Events
Acknowledgement Rate
```

Only if semantics are baselined.

---

# 89. Analytics False-Positive Metrics

Status: `PROPOSED`.

Only show if feedback feature is implemented and data volume is meaningful.

---

# 90. Analytics Integrity Rule

UI shall never generate random/placeholder chart data in production/demo mode.

Development mocks must be isolated and clearly disabled in integrated demo.

---

# 91. AI Models Page

Status: `PROPOSED`.

Purpose:

show deployed model provenance/health rather than provide full ML experiment management.

---

# 92. AI Models Page Content

Potential:

```text
Task
Model Name
Version
Status
Source
License
Deployment Status
Last Loaded / Health
```

Optional:

- final measured metrics.

---

# 93. AI Models Page Limitations

Do not allow ordinary operators to change model weights from UI in MVP.

Model deployment/change remains controlled configuration.

---

# 94. Audit Log Page

Status: `PROPOSED`.

Potential columns:

```text
Time
Actor
Action
Target
Outcome
```

Requires audit backend.

---

# 95. Settings Page

Status: `PROPOSED`.

Potential settings:

- display preferences;
- application metadata;
- selected non-sensitive configuration.

Do not expose secrets.

---

# 96. Notification Pattern

Within app, new event should surface via:

- event feed insertion;
- alert toast/banner;
- badge count.

Avoid excessive simultaneous modalities.

---

# 97. Toast Notification

Proposed content:

```text
Restricted Area Intrusion
North Entrance
12:31:05
[View]
```

Toast should auto-dismiss only if event remains visible elsewhere.

---

# 98. Critical Event Persistence

A transient toast is never the only representation.

The event persists in:

```text
Events
```

---

# 99. Alert Sound

Status: `DEFERRED/TBD`.

Do not add intrusive sound without explicit UX decision.

---

# 100. New Event Animation

Subtle highlight is acceptable.

Avoid flashing/strobing effects.

---

# 101. Real-Time Connection Banner

If disconnected:

```text
Live updates disconnected. Reconnecting…
```

Do not silently continue to imply live state.

---

# 102. Stale Data Indicator

If page still displays last-known data while disconnected:

show:

```text
Last updated at <time>
```

or equivalent.

---

# 103. Reconnection

After reconnect:

- refetch persisted events;
- merge by event ID;
- remove duplicate UI items;
- clear stale warning.

---

# 104. Offline Browser/Network State

If browser itself detects offline:

show explicit network status.

Do not conflate:

```text
Browser network offline
```

with:

```text
Camera offline
```

---

# 105. Global Loading Indicator

Avoid permanent spinner covering whole interface.

Prefer:

- page skeleton;
- local loaders;
- button loaders.

---

# 106. Form Loading

On submit:

- disable relevant action;
- preserve entered data;
- display progress.

---

# 107. Optimistic Updates

Use cautiously.

Appropriate:

- perhaps local filter state.

Not appropriate without reconciliation:

- acknowledgement;
- camera enabled state;
- rule saved state.

Server remains authoritative.

---

# 108. Error Message Style

Good:

```text
Could not acknowledge this event. Try again.
```

Better with safe reason when available:

```text
This event was already updated by another user. Refreshing current state.
```

Avoid:

```text
SQLAlchemy IntegrityError...
```

---

# 109. Validation Message Style

Field-specific:

```text
Dwell threshold must be greater than 0.
```

not:

```text
Invalid input.
```

---

# 110. Empty State Style

Empty state should explain:

- what is empty;
- what user can do next.

Example cameras:

```text
No cameras configured.
Add a camera to begin monitoring.
```

---

# 111. Accessibility — Keyboard

Interactive controls shall be keyboard reachable.

Zone editor requires special consideration because pointer-only drawing can be inaccessible.

Minimum:

- keyboard accessible form fields/actions;
- polygon editor may provide coordinate list editing or documented limitation if full keyboard geometry editing is infeasible.

---

# 112. Accessibility — Focus

Visible focus indicator required.

Dialogs should:

- trap focus;
- restore focus on close.

---

# 113. Accessibility — Labels

Every form control has:

- programmatic label;
- error association.

Icons have accessible names where actionable.

---

# 114. Accessibility — Color

Status should use:

```text
icon + label + color
```

not color alone.

---

# 115. Accessibility — Contrast

Text and essential UI controls should meet commonly accepted accessible contrast targets.

Exact conformance claim should only be made if tested.

---

# 116. Accessibility — Motion

Avoid unnecessary animation.

Respect reduced-motion preferences where feasible.

---

# 117. Accessibility — Charts

Charts should have:

- text title;
- axis labels;
- accessible summary/table where feasible.

---

# 118. Responsive Breakpoints

Exact pixel breakpoints: `TBD`.

Behavioral breakpoints:

```text
Desktop
Tablet
Mobile
```

---

# 119. Desktop Priority

Desktop layout supports:

- sidebar;
- side-by-side live video/details;
- wide event tables;
- analytics charts.

---

# 120. Tablet

May:

- collapse sidebar;
- stack some dashboard cards;
- keep live video above metadata.

---

# 121. Mobile

Must preserve core actions:

- event list;
- event detail;
- acknowledge;
- evidence view;
- camera health.

Advanced admin configuration, especially polygon drawing, may be less convenient but should remain functional where feasible.

---

# 122. Table Responsiveness

On small screens:

- convert wide tables to cards;
- hide non-essential metadata;
- retain core fields.

---

# 123. Event Card Mobile Layout

Example:

```text
[Event Type]
Camera Name
Time

Acknowledged / Unacknowledged
Evidence Available

[Open]
```

---

# 124. Zone Editor Mobile

If touch support exists:

- large drag handles;
- avoid tiny vertices.

If mobile polygon editing is not reliable, document:

```text
Desktop/tablet recommended for zone configuration.
```

---

# 125. Frontend State Categories

Recommended separation:

```text
Server State
Local UI State
Authentication State
Real-Time Connection State
Transient Form State
```

---

# 126. Server State

Examples:

- cameras;
- zones;
- rules;
- events;
- analytics.

Should be fetched/cached/reconciled using a consistent data layer.

Framework/library: `TBD`.

---

# 127. Local UI State

Examples:

- sidebar open;
- selected tab;
- modal open;
- unsaved polygon vertices.

Do not push every UI state into backend.

---

# 128. Real-Time State

WebSocket messages should update or invalidate relevant server-state caches.

Do not maintain a completely separate duplicate event store unless necessary.

---

# 129. Cache Invalidation

Example:

```text
event.created
→ insert/invalidate event list
```

```text
event.acknowledged
→ update event detail/list state
```

---

# 130. Server Reconciliation Rule

If real-time message conflicts with subsequent REST response:

REST/persisted backend state is authoritative.

---

# 131. API Consumption — Dashboard

Potential endpoints:

```text
GET /analytics/overview
GET /analytics/events/timeseries
GET /cameras
GET /events
```

---

# 132. API Consumption — Live View

Potential:

```text
GET /cameras/{id}
GET /cameras/{id}/health
GET /cameras/{id}/zones
GET /rules?camera_id=...
GET /events?camera_id=...
```

Video endpoint/transport remains `TBD`.

---

# 133. API Consumption — Cameras

```text
GET /cameras
POST /cameras
GET /cameras/{id}
PATCH /cameras/{id}
POST /cameras/{id}/enable
POST /cameras/{id}/disable
```

---

# 134. API Consumption — Zones

```text
GET /cameras/{id}/zones
POST /cameras/{id}/zones
GET /zones/{id}
PATCH /zones/{id}
POST /zones/{id}/enable
POST /zones/{id}/disable
```

---

# 135. API Consumption — Rules

```text
GET /rules
POST /rules
GET /rules/{id}
PATCH /rules/{id}
POST /rules/{id}/enable
POST /rules/{id}/disable
```

---

# 136. API Consumption — Events

```text
GET /events
GET /events/{id}
POST /events/{id}/acknowledgements
GET /events/{id}/acknowledgements
POST /events/{id}/feedback
```

Feedback route only if implemented.

---

# 137. API Consumption — Evidence

```text
GET /events/{id}/evidence
GET /evidence/{id}
GET /evidence/{id}/content
```

---

# 138. API Consumption — Analytics

```text
GET /analytics/overview
GET /analytics/events/timeseries
GET /analytics/events/by-camera
```

---

# 139. API Consumption — Models

Potential:

```text
GET /models
GET /models/{id}/versions/{version_id}
```

Lower priority.

---

# 140. WebSocket Consumption

Proposed message types:

```text
event.created
event.updated
event.acknowledged
camera.health_changed
system.degraded
```

Frontend should handle unknown future message types safely:

- log/ignore;
- not crash.

---

# 141. Page Route Proposal

If frontend uses client/server routing, proposed paths:

```text
/
 /dashboard
 /live
 /events
 /events/:eventId
 /cameras
 /cameras/:cameraId
 /cameras/:cameraId/zones
 /rules
 /analytics
 /models
 /audit
 /settings
```

Exact route structure remains `PROPOSED`.

---

# 142. Route Guards

Protected routes require authentication if auth is baselined.

Admin-only configuration routes require backend authorization regardless of frontend route guard.

---

# 143. Breadcrumbs

Useful on detail/config pages.

Example:

```text
Cameras > North Entrance > Zones
```

Not required on flat top-level dashboard pages.

---

# 144. Browser Title

Set meaningful title:

```text
Events — Sentinel AI
```

---

# 145. URL State for Filters

Recommended:

```text
/events?camera_id=...&event_type=...
```

Benefits:

- refresh persistence;
- shareable view;
- predictable navigation.

---

# 146. Confirmation Dialogs

Use for destructive/high-impact actions:

- disable camera;
- disable rule;
- delete if deletion is ever implemented.

Avoid confirmation for harmless navigation.

---

# 147. No Hard Delete by Default

UI should not show delete actions for:

- cameras;
- rules;
- zones;
- events;

unless backend design explicitly permits.

Prefer disable.

---

# 148. Camera Disable Dialog

Explain impact:

```text
Monitoring will stop for this camera. Historical events will remain available.
```

---

# 149. Rule Disable Dialog

Explain:

```text
This rule will stop generating new events. Existing event history will remain.
```

---

# 150. Zone Disable Dialog

Explain:

```text
Rules depending on this zone may stop evaluating.
```

Exact dependency behavior must match backend.

---

# 151. Form Dirty State

Proposed for:

- camera edit;
- zone edit;
- rule edit.

If unsaved changes exist, warn before navigation.

---

# 152. Save Feedback

After save:

- inline success state or toast;
- update local cached resource.

Avoid ambiguous silent save.

---

# 153. Data Refresh

Provide explicit refresh action where useful:

- cameras;
- events.

Do not require full browser refresh.

---

# 154. Timestamp Display

Backend returns UTC.

UI should display:

- user's local time or selected timezone;
- optionally absolute date.

Exact timezone policy: `TBD`.

For event detail, include full date and time.

---

# 155. Relative Time

Useful secondary text:

```text
2 minutes ago
```

but do not replace exact event occurrence time entirely.

---

# 156. Number Formatting

Counts should be locale-friendly.

No unnecessary decimals.

---

# 157. Duration Formatting

Examples:

```text
30 s
1 min 15 s
```

not:

```text
75000 ms
```

for normal users.

---

# 158. Model Score Formatting

If shown:

```text
0.873
```

or:

```text
0.87
```

depending on score precision.

Do not append `%` unless semantics justify.

---

# 159. Loading Evidence

For video:

- show progress/spinner;
- maintain event details around it.

---

# 160. Missing Evidence

Differentiate:

```text
not generated
generation failed
deleted
access denied
```

where backend exposes these states.

---

# 161. Unauthorized State

If API returns 403:

show:

```text
You do not have permission to perform this action.
```

Do not endlessly retry.

---

# 162. Session Expiry

If auth expires:

- redirect/prompt login according to auth strategy;
- preserve safe return route if feasible.

---

# 163. Backend Unavailable

Global message:

```text
Sentinel backend is unavailable.
Some data may be stale.
```

---

# 164. AI Worker Degraded

If backend reports worker unavailable:

show:

```text
AI processing is degraded.
Existing history remains available.
```

This is distinct from total application outage.

---

# 165. Evidence Storage Degraded

If evidence subsystem unavailable:

show event feed normally;
show evidence warning.

---

# 166. Partial Degradation Principle

UI should degrade by subsystem where possible.

Do not blank entire application because one secondary component fails.

---

# 167. Demo Mode Integrity

If a development/demo mode uses:

- mock API;
- injected events;
- prerecorded replay;

it must be visually/operationally distinguishable during development.

Final demonstration should clearly state which mode is active.

---

# 168. Mock Badge

Optional development-only:

```text
Mock Data
```

Never visible in final integrated demo unless intentionally demonstrating mock behavior.

---

# 169. Test Fixture Playback

If the project supports replaying a known video:

label:

```text
Recorded test video
```

not:

```text
Live CCTV
```

---

# 170. Live vs Recorded Source Indicator

Camera/source view should display:

```text
Live
Recorded
Test
```

only if source metadata supports such distinction.

---

# 171. System Health Page

Optional lower-priority page.

Could show:

```text
Backend
Database
AI Worker
Evidence Storage
Real-Time Channel
```

Status: `PROPOSED`.

---

# 172. User Management UI

Status: `TBD`.

Do not implement unless auth/role requirements include user administration.

---

# 173. Role Display

If roles exist, show human labels:

```text
Administrator
Operator
Reviewer
```

not raw internal IDs.

---

# 174. Security UX

Sensitive actions should not expose secrets.

Examples:

- camera credentials masked;
- tokens never rendered;
- credential reference shown as configured/not configured.

---

# 175. Camera Credential Form

If required:

- password-style input;
- leave blank means unchanged where supported;
- never prefill stored secret.

---

# 176. Evidence Download

Status: `TBD`.

If enabled, require authorization.

Do not expose direct storage path.

---

# 177. Keyboard Shortcuts

Not required for MVP.

Could be added later for operator efficiency.

---

# 178. Search

Global search is not required.

Event filtering provides sufficient MVP discoverability.

---

# 179. Notifications Badge

Sidebar `Events` may show:

```text
unacknowledged count
```

if backend semantics support efficient count.

---

# 180. Badge Refresh

Update through:

- REST initial state;
- WebSocket event/ack updates.

---

# 181. Event Row Highlighting

Unacknowledged events may use stronger visual emphasis.

Acknowledged events remain visible.

---

# 182. Event Detail Deep Link

Each event should have a stable URL.

Useful for:

- review;
- debugging;
- demonstration.

---

# 183. Camera Deep Link

Each camera should have stable detail URL.

---

# 184. Rule Deep Link

Optional but recommended if rule detail page exists.

---

# 185. Zone Deep Link

May be nested under camera rather than global.

---

# 186. Analytics Accessibility

Provide data table fallback/summary for major charts where feasible.

---

# 187. Chart Tooltip

Tooltips should state:

```text
bucket
metric
value
```

not just number.

---

# 188. Chart Loading

Use skeleton/placeholder.

Do not render zero as if actual while data loads.

---

# 189. Chart Empty

Explicit:

```text
No event data for selected period.
```

---

# 190. Chart Error

Explicit:

```text
Could not load analytics.
```

---

# 191. Event Detail Timeline

Proposed.

Potential entries:

```text
Event created
Evidence available
Acknowledged
False-positive feedback
Resolved
```

Depends on lifecycle/audit features.

---

# 192. Event Lifecycle Controls

Do not implement:

```text
Investigating
Resolved
Reopen
```

until event lifecycle is baselined.

---

# 193. Severity Controls

Do not implement severity selector until severity semantics are defined.

---

# 194. Camera Health Polling

If WebSocket health updates are unavailable, UI may poll.

Exact interval: `TBD`.

Avoid aggressive polling.

---

# 195. Analytics Refresh

Analytics need not update every second.

A manual or reasonable refresh is sufficient.

---

# 196. Event Feed Refresh

Event feed should be near-live using the real-time channel once baselined.

---

# 197. Camera Source Preview

For zone editing, frontend may require a current snapshot.

Potential endpoint:

```text
GET /cameras/{id}/snapshot
```

Status: `PROPOSED_IF_NEEDED`.

---

# 198. Snapshot Staleness

Zone editor should show capture time if snapshot may be old.

---

# 199. Multi-Zone Rendering

If camera has several zones:

- different labels;
- distinguish selected zone;
- avoid unreadable overlapping fills.

Exact colors: `TBD`.

---

# 200. Polygon Fill

Use semi-transparent fill plus visible border.

Selected zone gets stronger emphasis.

---

# 201. Zone Label

Render zone name near polygon where practical.

Avoid obscuring important video content.

---

# 202. Detection Overlay Z-Order

Suggested:

```text
video
zone fill
zone border
detection box
track label
event indicator
```

---

# 203. Performance Consideration — Overlays

Use browser-efficient rendering.

Potential technologies:

- SVG;
- Canvas.

Exact approach: `TBD`.

For editable polygon geometry, SVG is a strong candidate because:

- DOM-addressable points;
- straightforward scaling;
- event handling.

---

# 204. Zone Editor Rendering Candidate

`PROPOSED: SVG overlay`

Reasons:

- normalized viewBox possible;
- easy polygon/vertex rendering;
- pointer events;
- academic visibility.

Not yet a framework decision.

---

# 205. Video Rendering Technology

`TBD`.

Potential:

- HTML5 `<video>`;
- image snapshots;
- HLS;
- WebRTC;
- MJPEG;
- custom stream.

Depends on source architecture.

---

# 206. Video Error State

If browser cannot play source:

show:

```text
Video preview unavailable.
Monitoring state may still be active.
```

Do not imply backend processing stopped unless known.

---

# 207. Operator Priority

During an event:

primary action:

```text
View / Acknowledge
```

Administrative editing actions should not dominate operator screens.

---

# 208. Admin Priority

During configuration:

primary action:

```text
Save / Enable / Disable
```

---

# 209. Destructive Action Styling

Use visually distinct but restrained destructive style.

Do not make routine cancel buttons look destructive.

---

# 210. Form Layout

Desktop:

- labels above fields or aligned consistently;
- sensible grouping.

Avoid extremely wide text fields unless content requires it.

---

# 211. Form Help Text

Use for technical settings.

Example:

```text
Dwell threshold determines how long a tracked person must remain in the zone before a loitering event is created.
```

---

# 212. Technical Terms

When exposing:

```text
Track Loss Grace
Cooldown
Counting Method
```

provide contextual explanation.

---

# 213. Default Values

Do not invent defaults.

If no default baselined:

- require explicit input; or
- mark field pending decision.

---

# 214. Disabled Configuration

If a feature is not available:

prefer hidden or clearly disabled with explanation.

Avoid fake clickable controls.

---

# 215. Error Recovery

For failed form submission:

- preserve user data;
- keep polygon;
- allow correction.

---

# 216. Network Retry

User-initiated retry is acceptable.

Automatic retries should not duplicate create actions.

---

# 217. Unsaved Polygon Recovery

Optional:

retain local unsaved geometry during validation error.

---

# 218. Frontend Logging

Client may log safe diagnostics.

Do not log:

- credentials;
- access tokens;
- full private evidence.

---

# 219. Frontend Error Boundary

A rendering failure in one component should not necessarily crash entire app.

Framework-specific implementation: `TBD`.

---

# 220. Browser Compatibility

Supported browsers: `TBD`.

At minimum final demo browser must be explicitly tested.

Do not claim broad cross-browser compatibility without testing.

---

# 221. Browser Test Matrix

| Browser | Version | Status |
|---|---|---|
| Chrome/Chromium | `TBD` | `NOT_YET_TESTED` |
| Firefox | `TBD` | `NOT_YET_TESTED` |
| Edge | `TBD` | `NOT_YET_TESTED` |
| Safari | `TBD` | `NOT_YET_TESTED` |

---

# 222. Resolution Test Matrix

| Viewport | Purpose | Status |
|---|---|---|
| Desktop widescreen | primary | `NOT_YET_TESTED` |
| Laptop | primary | `NOT_YET_TESTED` |
| Tablet | secondary | `NOT_YET_TESTED` |
| Mobile | secondary | `NOT_YET_TESTED` |

---

# 223. Accessibility Test Matrix

At minimum test:

- keyboard navigation;
- visible focus;
- form labels;
- status not color-only;
- modal focus;
- chart labels.

---

# 224. UX Test Scenarios

## UX-TC-001

Operator finds newest unacknowledged event.

## UX-TC-002

Operator opens evidence.

## UX-TC-003

Operator acknowledges event.

## UX-TC-004

Admin creates polygon zone.

## UX-TC-005

Admin edits loitering threshold.

## UX-TC-006

Operator sees camera offline state.

## UX-TC-007

Operator sees AI worker degraded state.

## UX-TC-008

Client disconnects/reconnects and event state reconciles.

---

# 225. UI-to-Use-Case Traceability

| UI area | Use cases |
|---|---|
| Login | UC-AUTH-001 |
| Cameras | UC-CAM-001 through UC-CAM-004 |
| Zone editor | UC-ZONE-001/002 |
| Rule forms | UC-RULE-001 through UC-RULE-004 |
| Dashboard/live event feed | UC-MON-001 |
| Event detail | UC-EVT-006/007 |
| Evidence viewer | UC-EVD-001 |
| Event filters/history | UC-HIST-001/002 |
| Analytics | UC-ANL-001 |
| Degraded state | UC-SYS-001 |
| Reconnect | UC-SYS-004 |

---

# 226. UI-to-SRS Traceability

| UI area | Requirement families |
|---|---|
| auth | FR-AUTH-* |
| cameras | FR-CAM-* |
| zones | FR-ZONE-* |
| rules | FR-RULE-* |
| event feed | FR-EVT-*, FR-ALT-* |
| evidence | FR-EVD-* |
| history | FR-HIST-* |
| analytics | FR-ANL-* |
| real-time | FR-UI-005, NFR-REL-* |
| accessibility/usability | NFR-USAB-* |
| security | NFR-SEC-* |
| privacy | NFR-PRIV-* |

---

# 227. Frontend File Structure — Framework Neutral

Suggested:

```text
frontend/
└── src/
    ├── app/
    ├── pages/
    ├── components/
    ├── features/
    │   ├── cameras/
    │   ├── zones/
    │   ├── rules/
    │   ├── events/
    │   ├── evidence/
    │   └── analytics/
    ├── api/
    ├── realtime/
    ├── auth/
    ├── hooks/
    ├── utils/
    └── styles/
```

Exact framework may reorganize this.

---

# 228. Component Ownership

Suggested:

## Shared

- Button
- Input
- Select
- Modal
- Badge
- EmptyState
- ErrorState
- LoadingState

## Domain

- CameraCard
- CameraHealthBadge
- ZoneEditor
- RuleForm
- EventCard
- EventTable
- EventContextPanel
- EvidenceViewer
- AcknowledgeButton
- AnalyticsChart

---

# 229. Reusable Status Components

Avoid every page inventing its own badge colors/text.

Create shared components for:

```text
Camera Health
Event Acknowledgement
Evidence Status
Connection Status
```

---

# 230. Form Schema Reuse

Frontend validation schema should align with API contract.

If generated API types are available, reuse them where practical.

---

# 231. No Backend Logic Duplication

Frontend may validate for UX.

It shall not be the only place enforcing:

- zone-camera relationship;
- role permissions;
- threshold constraints;
- lifecycle transitions.

---

# 232. No Rule Engine in Frontend

Frontend may preview:

```text
zone geometry
```

but must not become authoritative intrusion/loitering/crowd evaluator.

---

# 233. No Local-Only Acknowledgement

Acknowledgement must persist through backend.

---

# 234. No Mock Analytics in Final Build

Hard-coded chart arrays are prohibited in final integrated mode.

---

# 235. No Direct Database Access

Frontend communicates only through backend/API.

---

# 236. No Direct AI Worker Access

Frontend shall not call the AI worker directly.

---

# 237. No Secret Exposure

Frontend bundle/config must not contain:

- DB credentials;
- AI-worker secrets;
- private storage credentials;
- camera credentials.

---

# 238. Environment Configuration

Public frontend configuration may contain:

- API base URL;
- WebSocket base URL.

Secret values shall remain server-side.

---

# 239. Build-Time vs Runtime Configuration

Exact approach depends on frontend framework.

Document in deployment guide.

---

# 240. Design Tokens

Recommended:

```text
spacing
radius
font sizes
semantic colors
shadows
```

defined consistently.

Exact values: `TBD`.

---

# 241. Spacing

Prefer consistent spacing scale.

Avoid arbitrary per-component margins.

---

# 242. Border Radius

Use restrained consistent radius.

Avoid excessive rounded-card aesthetic if it reduces information density.

---

# 243. Shadows

Use lightly for elevation/modal separation.

Do not rely on heavy shadows for hierarchy.

---

# 244. Dense vs Comfortable Layout

Monitoring applications benefit from moderate information density.

Provide sufficient spacing without making event lists excessively tall.

---

# 245. Dashboard Card Density

KPI cards should remain compact.

Operational lists deserve more vertical space.

---

# 246. Live View Priority

Video should occupy the largest area on the Live View page.

---

# 247. Event Detail Priority

Evidence + event facts should dominate.

Analytics/model internals should remain secondary.

---

# 248. Admin Configuration Priority

Form correctness and clear dependencies should dominate decorative design.

---

# 249. Naming Consistency

Use one term consistently:

```text
Camera
Zone
Rule
Event
Evidence
Acknowledgement
```

Do not alternate:

```text
Camera / Device / Feed / Sensor
```

unless they mean different things.

---

# 250. "Alert" Terminology

UI may use:

```text
Alert
```

for operator-facing urgent event presentation.

Database/API may model it as an event projection.

Documentation should remain clear that:

```text
event ≠ separate alert entity
```

unless architecture changes.

---

# 251. "Incident" Terminology

Avoid using `Incident` in UI until domain relationship is baselined.

---

# 252. "AI Confidence" Terminology

Avoid generic:

```text
AI Confidence
```

Prefer:

```text
Detector score
Violence model score
```

---

# 253. "Live" Terminology

Do not label recorded replay as:

```text
Live
```

---

# 254. "Offline" Terminology

Do not label intentionally disabled camera as offline.

---

# 255. "Resolved" Terminology

Do not show resolved lifecycle before state model exists.

---

# 256. User Feedback on Actions

Every major action should produce clear outcome:

- saved;
- failed;
- acknowledged;
- disabled;
- enabled.

---

# 257. Preventing Double Actions

Disable action while request is active.

Examples:

- acknowledge;
- save rule;
- add camera.

---

# 258. Data Race UX

If backend returns conflict:

- inform user;
- refresh authoritative state.

Example:

```text
This rule was updated elsewhere. Reloaded latest version.
```

---

# 259. Version Display

Admin rule detail may show:

```text
Version 3
```

Useful for debugging.

Not required in ordinary operator views.

---

# 260. Model Version Display

Violence event detail should show model version for traceability.

---

# 261. Zone Geometry Version Display

Can be hidden under technical details.

---

# 262. Technical Details Disclosure

Use expandable section:

```text
Technical Details
```

for:

- IDs;
- model version;
- correlation ID;
- geometry version.

Keeps main UI readable.

---

# 263. Correlation ID Display

Not needed by default.

Useful for developer/admin diagnostics.

---

# 264. Copy ID Action

Optional for event/camera IDs in technical detail.

---

# 265. Event Export

Deferred.

No CSV/PDF export required for MVP unless faculty specifically requests.

---

# 266. Analytics Export

Deferred.

---

# 267. Evidence Download

TBD.

---

# 268. Print Layout

Not required.

---

# 269. Dark Mode

Optional.

Do not prioritize over core event workflow.

---

# 270. Theme

One professional theme is sufficient.

---

# 271. Localization

Not required.

English-only UI is acceptable for MVP unless course requires otherwise.

---

# 272. Timezone

Display timezone should be visible or predictable.

Exact policy: `TBD`.

---

# 273. Accessibility Conformance Claim

Do not claim formal WCAG compliance unless tested.

Can state:

> The interface was designed with keyboard accessibility, visible focus, semantic labeling, and non-color-only status indicators.

if actually implemented.

---

# 274. UI Test Evidence

For each key screen retain:

- screenshot;
- test ID;
- browser;
- viewport;
- pass/fail.

---

# 275. Screenshot Naming

Recommended:

```text
UI-DASHBOARD-001.png
UI-LIVE-001.png
UI-EVENT-DETAIL-001.png
UI-ZONE-EDITOR-001.png
```

---

# 276. UI Review Checklist — Dashboard

- [ ] KPI data from API.
- [ ] Recent alerts visible.
- [ ] Camera health visible.
- [ ] Empty state.
- [ ] Loading state.
- [ ] Error state.
- [ ] No fake metrics.

---

# 277. UI Review Checklist — Live View

- [ ] Camera selector.
- [ ] Video/snapshot area.
- [ ] Health state.
- [ ] Zone overlay.
- [ ] Disabled state.
- [ ] Offline state.
- [ ] No frozen-frame-as-live deception.

---

# 278. UI Review Checklist — Zone Editor

- [ ] Add vertices.
- [ ] Close polygon.
- [ ] Edit vertices.
- [ ] Normalize coordinates.
- [ ] Resize projection.
- [ ] Validation.
- [ ] Cancel/reset.
- [ ] Save.
- [ ] Error recovery.

---

# 279. UI Review Checklist — Rules

- [ ] Type-specific forms.
- [ ] Camera/zone relationship clear.
- [ ] Units clear.
- [ ] No invented defaults.
- [ ] Enable/disable.
- [ ] Validation.
- [ ] Save feedback.

---

# 280. UI Review Checklist — Events

- [ ] Newest first.
- [ ] Filters.
- [ ] Acknowledgement state.
- [ ] Evidence state.
- [ ] Empty/error/loading states.
- [ ] Pagination.
- [ ] Deep link.

---

# 281. UI Review Checklist — Event Detail

- [ ] Event type.
- [ ] Camera.
- [ ] exact time.
- [ ] evidence.
- [ ] context.
- [ ] acknowledgement.
- [ ] model details where relevant.
- [ ] unauthorized behavior.
- [ ] evidence failure.

---

# 282. UI Review Checklist — Analytics

- [ ] Time range.
- [ ] chart labels.
- [ ] source data from backend.
- [ ] empty state.
- [ ] error state.
- [ ] no fake values.

---

# 283. UI Review Checklist — Real-Time

- [ ] connected state.
- [ ] disconnected state.
- [ ] reconnecting state.
- [ ] reconcile persisted events.
- [ ] duplicate handling.
- [ ] stale data indication.

---

# 284. UI Review Checklist — Responsive

- [ ] Desktop.
- [ ] Laptop.
- [ ] Tablet.
- [ ] Mobile event workflow.
- [ ] no horizontal overflow on core screens.

---

# 285. UI Review Checklist — Accessibility

- [ ] Keyboard.
- [ ] Focus.
- [ ] Labels.
- [ ] Modal focus handling.
- [ ] Non-color-only statuses.
- [ ] Chart labels/summary.
- [ ] Semantic buttons/links.

---

# 286. Open UI Decisions

| ID | Decision | Status |
|---|---|---|
| UI-OD-001 | Frontend framework | `TBD` |
| UI-OD-002 | Component/design system | `TBD` |
| UI-OD-003 | Exact navigation set | `PROPOSED` |
| UI-OD-004 | Authentication UI | `TBD` |
| UI-OD-005 | Video playback transport | `TBD` |
| UI-OD-006 | Zone editor uses SVG vs Canvas | `PROPOSED: SVG` |
| UI-OD-007 | Exact semantic color palette | `TBD` |
| UI-OD-008 | Exact typography | `TBD` |
| UI-OD-009 | Event lifecycle controls | `TBD` |
| UI-OD-010 | Severity display | `TBD` |
| UI-OD-011 | Multi-user acknowledgement presentation | `TBD` |
| UI-OD-012 | False-positive feedback inclusion | `PROPOSED` |
| UI-OD-013 | AI Models page inclusion | `PROPOSED` |
| UI-OD-014 | Audit page inclusion | `PROPOSED` |
| UI-OD-015 | Evidence download | `TBD` |
| UI-OD-016 | Dark mode | `DEFERRED` |
| UI-OD-017 | Mobile polygon editing expectations | `TBD` |
| UI-OD-018 | Timezone display policy | `TBD` |
| UI-OD-019 | Dashboard KPI period | `TBD` |
| UI-OD-020 | Alert sound | `DEFERRED/TBD` |

---

# 287. Frontend Baseline Checklist

Before this document becomes `BASELINED`:

- [ ] Frontend framework selected.
- [ ] Navigation accepted.
- [ ] Role/authorization UX aligned with backend.
- [ ] Dashboard structure accepted.
- [ ] Live View behavior accepted.
- [ ] Video source/playback method selected.
- [ ] Zone editor rendering method selected.
- [ ] Normalized coordinate contract confirmed.
- [ ] Rule forms match API semantics.
- [ ] Event list/detail accepted.
- [ ] Acknowledgement semantics accepted.
- [ ] Evidence states accepted.
- [ ] Analytics charts accepted.
- [ ] Real-time endpoint/message handling confirmed.
- [ ] Disconnect/reconnect behavior accepted.
- [ ] Error/loading/empty states defined.
- [ ] Responsive expectations accepted.
- [ ] Accessibility minimum accepted.
- [ ] No unresolved domain feature is presented as complete.

---

# 288. AI Assistant Frontend Rules

Once baselined, an AI assistant shall not:

1. invent a page absent from this specification;
2. invent API fields;
3. invent event lifecycle controls;
4. invent severity values;
5. call detector score a probability;
6. call track IDs person identity;
7. label recorded video as live;
8. label disabled camera as offline;
9. create frontend-only event logic;
10. persist acknowledgement only in client state;
11. expose raw camera credentials;
12. expose media storage paths;
13. insert random analytics data into final mode;
14. add a hidden mock fallback when API fails;
15. change normalized polygon coordinate convention;
16. silently introduce a new frontend dependency without project review;
17. add facial recognition UI;
18. add deferred features to impress the demo.

---

# 289. First Frontend Vertical Slice

The frontend implementation order should begin with:

```text
1. application shell
2. camera/source selection
3. event list
4. event detail
5. WebSocket/new-event handling
6. acknowledgement
7. persisted refresh
8. zone editor
```

The first integrated milestone should demonstrate:

```text
recorded/live source
→ intrusion event
→ event appears
→ open detail
→ view evidence/status
→ acknowledge
→ refresh
→ acknowledgement remains
```

---

# 290. Suggested Frontend Development Order

## Days 1–2

- framework setup;
- shell;
- routes;
- shared components;
- mock contract types.

## Days 3–5

- cameras;
- event list;
- event detail;
- dashboard shell.

## Days 6–8

- real-time events;
- acknowledgement;
- zone editor;
- first vertical slice.

## Days 9–11

- rule configuration;
- evidence viewer;
- offline/degraded states.

## Days 12–14

- analytics;
- responsive/accessibility;
- polish;
- test screenshots.

---

# 291. Frontend Definition of Ready

A UI feature is ready for implementation when:

- use case exists;
- API contract exists;
- permission expectation known;
- data fields known;
- loading/error/empty behavior defined;
- acceptance criteria known.

---

# 292. Frontend Definition of Done

A UI feature is done when:

- functional behavior implemented;
- API integrated;
- loading state implemented;
- empty state implemented;
- error state implemented;
- unauthorized state handled where relevant;
- responsive behavior checked;
- keyboard/basic accessibility checked;
- automated/manual tests executed;
- screenshots/evidence captured;
- docs updated.

---

# 293. Final UI/UX Rule

> **Sentinel AI's interface shall make operational truth clearer, not more dramatic.**
>
> The UI is successful when an authorized user can determine:
>
> - what happened;
> - where it happened;
> - when it happened;
> - what evidence exists;
> - whether the event was acknowledged;
> - whether the system is healthy;
> - whether displayed information is live, stale, recorded, pending, or failed.
>
> The frontend shall never compensate for missing backend/domain decisions by inventing behavior locally.
>
> If the API or domain model still says:
>
> `TBD`
>
> the frontend specification shall also say:
>
> `TBD`
>
> rather than creating a plausible-looking control with no authoritative meaning.
