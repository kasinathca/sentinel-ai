---
title: "Sentinel AI — Operator and Administrator Manual"
document_id: "SEN-OPS"
version: "0.1.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
last_updated: "2026-08-20"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "operator workflows"
  - "administrator workflows"
  - "faculty demonstration walkthrough"
  - "camera monitoring procedures"
  - "zone and rule configuration procedures"
  - "event review and acknowledgement"
  - "evidence review"
  - "history and analytics usage"
  - "offline and degraded-state handling"
---

# Sentinel AI — Operator and Administrator Manual

> **Document purpose**
>
> This manual explains how an authorized user operates Sentinel AI.
>
> It is written for:
>
> - Operators
> - Administrators
> - Reviewers/Supervisors where applicable
> - Faculty/reviewers observing the project demonstration
>
> It intentionally avoids implementation internals unless they directly affect user actions.
>
> This manual shall be updated to match the final UI exactly before submission.

---

# 0. Manual Status

## 0.1 Current state

Sentinel AI is still under implementation.

Therefore some workflows in this manual are:

```text
CONFIRMED
PROPOSED
TBD
```

depending on whether the corresponding backend/UI decision has been baselined.

## 0.2 Important rule

If a screen, button, field, or workflow is not present in the implemented application, this manual must not pretend that it exists.

Before final submission:

```text
manual
→ compare against actual UI
→ remove obsolete steps
→ capture final screenshots
→ verify wording
```

---

# 1. What Sentinel AI Does

Sentinel AI is a web-based CCTV monitoring and event-management system.

It is designed to:

- monitor configured video sources;
- detect persons;
- track persons temporarily;
- detect restricted-area entry;
- detect loitering using dwell-time rules;
- detect crowd-threshold conditions;
- detect violence/fighting through a temporal AI model;
- detect camera-offline conditions;
- generate events;
- attach evidence where available;
- notify operators;
- allow acknowledgement;
- maintain searchable history;
- display analytics.

---

# 2. What Sentinel AI Does Not Do

Sentinel AI does not:

- perform facial recognition;
- identify people by name;
- infer criminal intent;
- decide guilt;
- automatically punish or escalate;
- permanently track identities across cameras;
- automatically retrain itself from operator feedback;
- provide legal or law-enforcement judgement.

Temporary labels such as:

```text
Track 17
```

refer only to computational tracking within a camera/video session.

---

# 3. User Roles

Exact permissions remain subject to final RBAC design.

## 3.1 Administrator

Expected responsibilities:

- add/edit cameras;
- enable/disable cameras;
- create/edit zones;
- configure rules;
- inspect system health;
- review events;
- review analytics.

## 3.2 Operator

Expected responsibilities:

- monitor dashboard;
- monitor cameras;
- review events;
- inspect evidence;
- acknowledge alerts/events;
- search event history.

## 3.3 Reviewer / Supervisor

Proposed responsibilities:

- review history;
- review analytics;
- inspect evidence;
- review audit information where implemented.

---

# 4. Main Navigation

Proposed main navigation:

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

The final implemented navigation may include only a subset.

Core pages expected for MVP:

```text
Dashboard
Live View
Events
Cameras
Rules
Analytics
```

---

# 5. Starting the Application

Application startup is handled using:

```text
16-deployment-guide.md
```

The operator normally does not start backend/database/AI services manually unless they are also acting as developer/admin.

Before opening the browser, required services should be healthy.

---

# 6. Opening Sentinel AI

Open the configured frontend address in the approved browser.

Frontend URL:

```text
TBD
```

Example only:

```text
http://localhost:<PORT>
```

Do not copy an example port into final documentation until the actual port is selected.

---

# 7. Login

Authentication workflow:

```text
TBD
```

If local login is selected:

1. Open Sentinel AI.
2. Enter authorized username/email.
3. Enter password.
4. Select **Sign In**.
5. Wait for the dashboard.

## 7.1 Invalid login

If credentials are invalid:

```text
Invalid credentials.
```

or equivalent safe error should appear.

Do not repeatedly retry with random credentials.

## 7.2 Session expired

If the session expires:

1. save any non-sensitive local notes if necessary;
2. sign in again;
3. return to the previous workflow.

---

# 8. Dashboard Overview

The Dashboard is the main operational overview.

It should show the most important current information.

Typical sections:

```text
Unacknowledged Events
Recent Events
Camera Health
Event Trends
Offline Cameras
Acknowledgement Summary
```

---

# 9. Reading Dashboard KPI Cards

Potential cards include:

## Unacknowledged Events

Shows events still requiring operator attention.

Selecting the card may open:

```text
Events filtered by acknowledged = false
```

## Offline Cameras

Shows cameras currently considered offline.

## Events in Selected Period

Shows event count for the active analytics/dashboard period.

Exact period:

```text
TBD
```

---

# 10. Recent Events

Recent-event entries should include:

- event type;
- camera name;
- occurrence time;
- acknowledgement status;
- evidence state.

Select an event to open its detailed record.

---

# 11. Camera Health Summary

A camera may show states such as:

```text
Healthy
Degraded
Offline
Unknown
Disabled
```

Important:

```text
Disabled ≠ Offline
```

A disabled camera has been intentionally turned off from monitoring.

An offline camera is expected to be active but is not providing a healthy source according to configured criteria.

---

# 12. Real-Time Connection Indicator

If real-time updates are enabled, the UI may show:

```text
Connected
Reconnecting
Disconnected
```

## Connected

New events should appear without manual page refresh.

## Reconnecting

The client is attempting to restore the live connection.

## Disconnected

Displayed data may be stale.

Use the latest update time and wait for reconnection or manually refresh.

---

# 13. Live View

The Live View page is used to inspect a selected camera/video source.

Typical layout:

```text
Video / Snapshot
Zone Overlays
Optional Person/Track Overlays
Camera Health
Active Rules
Recent Events
```

---

# 14. Selecting a Camera

1. Open **Live View**.
2. Select the required camera from the camera selector.
3. Confirm the camera name.
4. Check the health badge.
5. Verify whether the source is:
   - live;
   - recorded;
   - test/replay.

The UI shall not label a recorded fixture as live.

---

# 15. Video and Overlay Interpretation

The visual area may contain:

## Zone polygon

Shows configured monitored area.

## Person bounding box

Optional display from person detector.

## Track label

Example:

```text
Track 17
```

This is not identity recognition.

## Event marker

May indicate where a rule condition was triggered.

---

# 16. Camera Offline in Live View

If a camera becomes offline:

- video area should show an offline state;
- camera metadata remains visible;
- last frame time may be displayed;
- historical events remain accessible.

Do not assume the frozen last frame is still current.

---

# 17. Disabled Camera in Live View

If intentionally disabled:

```text
Monitoring disabled
```

should be displayed.

This is not a system failure.

---

# 18. Cameras Page

Administrators use the Cameras page to manage configured sources.

Typical information:

```text
Camera Name
Source Type
Enabled
Health
Last Frame
Zones
Rules
```

---

# 19. Adding a Camera

Admin-only workflow.

1. Open **Cameras**.
2. Select **Add Camera**.
3. Enter:
   - camera name;
   - description;
   - source type;
   - source configuration.
4. Configure credentials only through the approved credential input if required.
5. Choose whether monitoring should be enabled.
6. Select **Save**.
7. Confirm camera appears in the list.
8. Check health.

Exact source types remain:

```text
TBD
```

Potential:

```text
Recorded file
Webcam
RTSP/IP stream
Uploaded video
```

Only implemented source types should be selectable.

---

# 20. Camera Configuration Safety

Do not:

- paste private passwords into camera description;
- share credentials in screenshots;
- expose source URLs containing embedded passwords;
- invent unsupported source types.

---

# 21. Editing a Camera

1. Open **Cameras**.
2. Select the camera.
3. Select **Edit**.
4. Change only required fields.
5. Save.
6. Verify updated state.

If changing a source configuration, check health afterward.

---

# 22. Disabling a Camera

1. Open camera details.
2. Select **Disable**.
3. Confirm action if prompted.
4. Verify:

```text
Enabled = false
```

Historical events remain.

---

# 23. Re-Enabling a Camera

1. Open camera.
2. Select **Enable**.
3. Verify source reconnects.
4. Check health.

A camera may require a short time before becoming healthy.

---

# 24. Zone Management

Zones represent monitored spatial regions.

Typical uses:

- restricted area;
- loitering area;
- crowd counting area.

Zones are linked to a camera.

---

# 25. Opening the Zone Editor

1. Open **Cameras**.
2. Select the camera.
3. Open **Zones**.
4. Choose **Add Zone** or edit an existing zone.
5. Wait for the camera snapshot/frame to load.

---

# 26. Creating a Zone Polygon

Proposed interaction:

1. Enter a zone name.
2. Select zone type if required.
3. Click on the image to create the first vertex.
4. Continue clicking to add vertices.
5. Close the polygon:
   - select the first point;
   - or use **Finish Polygon**.
6. Review shape.
7. Adjust vertices if needed.
8. Save.

---

# 27. Editing Zone Vertices

If supported:

1. Select existing zone.
2. Choose **Edit**.
3. Drag a vertex.
4. Confirm polygon still represents intended region.
5. Save.

---

# 28. Resetting a Zone

If drawing becomes incorrect:

1. Select **Reset**.
2. Redraw polygon.
3. Save only after confirming geometry.

---

# 29. Zone Placement Guidance

Good zone:

- covers exactly intended physical area;
- avoids unnecessary surrounding space;
- aligns with camera perspective;
- is tested using controlled movement.

Poor zone:

- crosses unrelated pathways;
- includes large irrelevant areas;
- has points outside the visible image;
- overlaps unpredictably with other zones.

---

# 30. Zone Geometry and Video Resizing

Sentinel is designed to use normalized coordinates so the polygon remains aligned when the video display size changes.

If a zone shifts after browser resize:

```text
report as UI defect
```

rather than manually redrawing to compensate.

---

# 31. Rules Page

Rules convert tracked observations into deterministic events.

MVP rule types:

```text
Restricted Area Intrusion
Loitering
Crowd Threshold
```

Violence uses a separate AI model/event policy.

Camera Offline uses health monitoring.

---

# 32. Creating a Restricted-Area Intrusion Rule

1. Open **Rules**.
2. Select **Add Rule**.
3. Choose:

```text
Restricted Area Intrusion
```

4. Enter rule name.
5. Select camera.
6. Select restricted zone.
7. Configure any baselined position/retrigger settings.
8. Enable rule.
9. Save.
10. Run a controlled crossing test.

---

# 33. Intrusion Interpretation

An intrusion event should generally occur when a tracked person transitions from outside to inside the configured zone.

Exact boundary/retrigger semantics are defined by the final rule policy.

---

# 34. Creating a Loitering Rule

1. Open **Rules**.
2. Select **Add Rule**.
3. Choose:

```text
Loitering
```

4. Select camera.
5. Select zone.
6. Enter dwell threshold.
7. Configure track-loss grace/reset settings if exposed.
8. Enable.
9. Save.

---

# 35. Loitering Threshold

The UI should display human-friendly time units.

Example:

```text
30 seconds
```

not:

```text
30000 ms
```

unless technical details are shown.

Exact production/demo threshold:

```text
TBD
```

---

# 36. Loitering Interpretation

Loitering requires:

```text
tracked person
+
remaining in configured zone
+
meeting dwell-time threshold
```

A brief detector miss or track change may affect timer behavior depending on tracking/grace configuration.

---

# 37. Creating a Crowd Rule

1. Open **Rules**.
2. Select **Add Rule**.
3. Choose:

```text
Crowd Threshold
```

4. Select camera.
5. Select zone.
6. Enter person threshold.
7. Select counting method if implemented.
8. Enable.
9. Save.

---

# 38. Crowd Interpretation

The event occurs when the configured counting policy reaches/exceeds the threshold according to final semantics.

Observed count may depend on:

- person detection;
- track continuity;
- zone geometry.

---

# 39. Enabling and Disabling Rules

Disabled rule:

```text
does not generate new events
```

Existing history remains.

Use disabling instead of deleting when possible.

---

# 40. Editing a Rule

1. Open rule.
2. Select **Edit**.
3. Change required value.
4. Save.
5. Confirm updated version/config.
6. Re-test affected behavior.

Important:

Changing detector/tracker/rule thresholds can alter event behavior.

---

# 41. Events Page

The Events page is the main operational event list and history view.

Typical columns:

```text
Time
Type
Camera
Acknowledged
Evidence
Status
```

---

# 42. Event Types

MVP event types:

```text
Restricted Area Intrusion
Loitering
Crowd Threshold
Violence/Fighting
Camera Offline
```

---

# 43. Opening an Event

1. Open **Events**.
2. Select an event.
3. Review:
   - event type;
   - camera;
   - occurrence time;
   - event context;
   - evidence;
   - acknowledgement state.

---

# 44. Event Time

Event detail should show exact occurrence time.

Relative time such as:

```text
2 minutes ago
```

may appear as secondary information.

---

# 45. Intrusion Event Detail

Expected information:

```text
Camera
Zone
Rule
Occurrence Time
Track ID if displayed
Trigger Position/Context
Evidence
Acknowledgement
```

Track ID is temporary.

---

# 46. Loitering Event Detail

Expected:

```text
Observed Dwell Time
Configured Threshold
Zone
Camera
Track ID
Evidence
```

---

# 47. Crowd Event Detail

Expected:

```text
Observed Count
Configured Threshold
Counting Method
Zone
Camera
```

---

# 48. Violence Event Detail

Expected:

```text
Model Name
Model Version
Output Label
Model Score
Configured Event Threshold
Temporal Window
Evidence
```

Important:

```text
Model score ≠ guaranteed probability
```

unless calibration is explicitly documented.

---

# 49. Camera Offline Event Detail

Expected:

```text
Camera
Last Frame Time
Offline Criterion
Reason
Health Transition
```

---

# 50. Evidence

Evidence may include:

```text
Snapshot
Short Video Clip
```

Evidence status may be:

```text
Pending
Available
Failed
Deleted
```

---

# 51. Viewing a Snapshot

1. Open event.
2. Locate **Evidence**.
3. Select snapshot.
4. Inspect image.
5. Return to event detail.

Do not download/share restricted evidence without permission.

---

# 52. Viewing a Video Clip

1. Open event.
2. Select evidence clip.
3. Use play/pause controls.
4. Review event context.
5. Close/return.

No autoplay with sound should be assumed.

---

# 53. Evidence Pending

If evidence shows:

```text
Processing…
```

the event is still valid.

Wait for evidence update or refresh later.

---

# 54. Evidence Failed

If evidence generation fails:

```text
Evidence unavailable / generation failed
```

should be shown.

Do not assume event itself is invalid.

---

# 55. Evidence Deleted

If retention/manual deletion removed media:

event metadata may remain.

The UI should not show a broken media link.

---

# 56. Acknowledging an Event

Acknowledgement records that an authorized user has reviewed/responded to an event.

Workflow:

1. Open event.
2. Review event details and evidence.
3. Select **Acknowledge**.
4. Add comment if required/desired.
5. Submit.
6. Wait for confirmation.
7. Verify acknowledged state.

---

# 57. Acknowledgement Meaning

Acknowledgement does **not** mean:

```text
event was true
incident resolved
person guilty
model correct
```

It means:

```text
an authorized user reviewed/accepted responsibility for the event workflow
```

---

# 58. Acknowledgement Persistence

After acknowledgement:

1. refresh page;
2. verify event remains acknowledged.

If it reverts:

```text
report as persistence defect
```

---

# 59. Acknowledgement Error

If acknowledgement fails:

- UI should show error;
- do not assume it was saved;
- retry after checking backend/network.

---

# 60. Multiple Acknowledgements

Exact cardinality remains `TBD`.

If UI supports multiple users, it may show:

```text
Acknowledged by 2 users
```

Do not assume single-user acknowledgement until finalized.

---

# 61. False-Positive Feedback

Status: `PROPOSED`.

If implemented:

1. open event;
2. select **Mark as False Positive**;
3. choose reason if available;
4. add optional notes;
5. submit.

---

# 62. False-Positive Meaning

False-positive feedback is:

```text
operator review feedback
```

It does not automatically retrain the model.

---

# 63. Searching Event History

Open **Events**.

Use filters such as:

```text
Date/Time Range
Camera
Event Type
Acknowledged
Status
```

Only baselined filters should appear.

---

# 64. Filtering by Camera

1. Open filter bar.
2. Select camera.
3. Apply.
4. Review results.

---

# 65. Filtering by Event Type

Select one or more supported event types if multi-select exists.

Examples:

```text
Loitering
Violence/Fighting
```

---

# 66. Filtering by Acknowledgement

Typical:

```text
All
Acknowledged
Unacknowledged
```

---

# 67. Clearing Filters

Use:

```text
Reset Filters
```

or equivalent.

If no results appear, distinguish:

```text
No events match filters
```

from:

```text
Could not load events
```

---

# 68. Event Pagination

The UI may use:

```text
Load More
Next
```

The operator should never need to handle raw cursor values.

---

# 69. Analytics Page

Analytics summarizes persisted event data.

Typical sections:

```text
Event Trend
Events by Type
Events by Camera
Acknowledged vs Unacknowledged
```

---

# 70. Selecting Analytics Time Range

1. Open **Analytics**.
2. Choose start/end period.
3. Apply.
4. Review charts.

Exact quick presets remain `TBD`.

---

# 71. Reading Event Trend

The chart shows event counts over time buckets.

Confirm:

- selected time range;
- x-axis time;
- y-axis event count.

Do not interpret a spike without checking underlying events.

---

# 72. Events by Type

Useful for understanding which rule/event family occurs most frequently.

A high count may indicate:

- genuine activity;
- overly broad zone;
- low threshold;
- detector/tracker issue;
- duplicate suppression problem.

Analytics alone does not explain cause.

---

# 73. Events by Camera

Useful for identifying which cameras generate most events.

High event volume should be reviewed, not automatically treated as higher risk.

---

# 74. Acknowledgement Analytics

If implemented:

```text
Acknowledged
Unacknowledged
Acknowledgement rate
```

These reflect workflow, not model accuracy.

---

# 75. AI Models Page

Status: `PROPOSED`.

If available, it may show:

```text
Task
Model
Version
Status
License/Source
Measured Metrics
```

This page is informational.

Operators should not upload/change model files through UI in MVP.

---

# 76. Model Health

Potential states:

```text
Ready
Loading
Degraded
Failed
```

Exact states depend on worker implementation.

---

# 77. Audit Log

Status: `PROPOSED`.

If available, administrators/reviewers may see:

```text
Time
Actor
Action
Target
Outcome
```

Examples:

- camera updated;
- rule disabled;
- event acknowledged.

---

# 78. Settings

Status: `PROPOSED`.

Do not expect settings to expose:

- secrets;
- raw DB connection;
- model filesystem path;
- camera password.

---

# 79. Operator Handling — Camera Offline

When camera shows offline:

1. verify it is enabled;
2. open camera details;
3. inspect last frame time;
4. inspect recent offline event;
5. if authorized, check source configuration;
6. report technical issue if source should be active.

Do not repeatedly enable/disable without understanding cause.

---

# 80. Administrator Handling — Camera Offline

Check:

```text
camera enabled?
source exists?
network/source available?
decoder working?
credentials valid?
health policy?
```

Use deployment troubleshooting guide if technical debugging is required.

---

# 81. AI Worker Degraded

If UI shows AI processing degraded:

Operators should:

- continue reviewing existing history;
- understand new AI-dependent events may not be generated correctly;
- avoid assuming absence of events means normal activity.

Administrators/developers should inspect worker health.

---

# 82. Backend Unavailable

If backend is unavailable:

- live operational state cannot be trusted;
- avoid assuming displayed cached/stale information is current;
- wait for recovery or restart services according to deployment guide.

---

# 83. Real-Time Disconnected

If real-time channel disconnects:

- UI should indicate it;
- history may still be queried through REST if backend is reachable;
- after reconnect, the client should reconcile missed events.

---

# 84. Stale Data

If last update time is old:

treat current page as stale until refreshed/reconnected.

---

# 85. Common Operator Mistake — Recorded vs Live

Do not describe a replayed test video as live CCTV.

Correct phrase:

```text
Recorded test video processed through the live event pipeline
```

---

# 86. Common Operator Mistake — Track Identity

Do not say:

```text
This is person 17.
```

Say:

```text
This is temporary Track 17 within the current stream/session.
```

---

# 87. Common Operator Mistake — Model Score

Do not say:

```text
87% probability of violence
```

unless explicitly calibrated.

Say:

```text
Violence model score = 0.87
```

---

# 88. Common Operator Mistake — Acknowledgement

Do not say:

```text
Acknowledged means resolved.
```

unless lifecycle semantics explicitly define that.

---

# 89. Common Administrator Mistake — Huge Zone

Avoid drawing a zone covering nearly the entire camera when only a doorway is restricted.

Poor zone geometry increases false events.

---

# 90. Common Administrator Mistake — Very Low Threshold

Do not lower detector/event thresholds simply to force demo events.

Thresholds should be selected through test/evaluation.

---

# 91. Common Administrator Mistake — Hidden Demo Rule

Do not create backend-only hidden rules that are not visible/configurable through documented workflow.

---

# 92. Common Administrator Mistake — Secret in Source URL

Do not expose:

```text
username:password
```

inside screenshots/UI logs.

---

# 93. Common Administrator Mistake — Deleting History

Prefer disable over destructive delete where supported.

Historical events are useful for testing and traceability.

---

# 94. Recommended Daily Operator Workflow

```text
1. Sign in
2. Check Dashboard
3. Check offline/degraded cameras
4. Review unacknowledged events
5. Open evidence
6. Acknowledge reviewed events
7. Inspect unusual event spikes
8. Use history filters if investigating
```

---

# 95. Recommended Daily Administrator Workflow

```text
1. Check system health
2. Check cameras
3. Verify enabled rules
4. Review zones/configuration
5. Review unusual event volume
6. Investigate recurring false positives
7. Avoid changing thresholds without testing
```

---

# 96. First-Time Administrator Setup

Recommended order:

```text
1. Create/login admin user
2. Add camera/source
3. Verify camera health
4. Create zone
5. Create intrusion rule
6. Run controlled intrusion test
7. Verify event
8. Verify evidence
9. Acknowledge
10. Add loitering/crowd rules
```

---

# 97. Golden Demo Preparation

Before faculty presentation:

- verify exact repository commit;
- start all services;
- verify camera/source;
- verify golden fixture;
- verify zone;
- verify intrusion rule;
- clear irrelevant stale alerts if appropriate;
- verify evidence path;
- verify login;
- verify browser.

---

# 98. Faculty Demo — Short Walkthrough

Recommended 5–8 minute demonstration:

## Step 1 — Dashboard

Explain:

> Sentinel AI is a web-based CCTV monitoring and event-management system. The dashboard summarizes current camera health and recent security-relevant events.

## Step 2 — Live View

Open configured test camera.

Explain:

> This is a recorded test video being processed through the same monitoring pipeline used by the application.

Show restricted zone.

## Step 3 — Trigger Intrusion

Start/replay the golden fixture.

Wait for person to enter zone.

Explain:

> The AI subsystem detects and tracks the person, while the backend rule engine evaluates the restricted-area polygon.

## Step 4 — Event Appears

Open the new event.

Explain:

> The low-level person detection is not itself the alert. The backend converts the tracked zone-entry condition into a persistent domain event.

## Step 5 — Evidence

Show snapshot/clip or evidence status.

Explain:

> Evidence is stored separately from the event metadata and remains access-controlled.

## Step 6 — Acknowledge

Select **Acknowledge**.

Explain:

> Acknowledgement records operator review; it does not mean the AI is always correct or that the event is legally resolved.

## Step 7 — Refresh

Refresh page.

Show acknowledgement persists.

Explain:

> The acknowledgement is persisted in the backend rather than being a temporary frontend state.

## Step 8 — History / Analytics

Show event history and one analytics view.

Explain:

> The same persisted events can be searched and aggregated for operational review.

---

# 99. Faculty Demo — Optional AI Explanation

If asked how AI works:

Use:

> Person detection and tracking provide observations. Intrusion, loitering, and crowd conditions are deterministic rules built on those observations. Violence/fighting is handled by a separate temporal video model. This prevents the system from using one opaque model for every event type.

---

# 100. Faculty Demo — Optional Privacy Explanation

Use:

> The MVP explicitly excludes facial recognition. Track IDs are temporary and are not mapped to real identities. Evidence access is controlled, and the design minimizes unnecessary persistence of raw frame-level data.

---

# 101. Faculty Demo — Optional Failure Demonstration

If time allows:

stop/disable a camera or worker in a controlled manner.

Show:

```text
Camera Offline
```

or:

```text
AI Processing Degraded
```

Explain:

> The application distinguishes system degradation from normal negative inference instead of silently pretending everything is healthy.

---

# 102. Faculty Demo — Avoid These Claims

Do not say:

```text
100% accurate
crime prediction
recognizes criminals
real-time on any number of cameras
production ready
legally compliant
```

unless independently and properly proven.

---

# 103. Demonstrating Violence Detection

If final model is ready:

1. select approved test clip;
2. run through violence model;
3. open event;
4. show:
   - model version;
   - label;
   - model score;
   - threshold;
   - evidence.

Explain limitations honestly.

---

# 104. Demonstrating a Negative Violence Sample

If time permits:

run a negative sample.

Expected:

```text
no violence event
```

or document known false-positive behavior if it occurs.

Do not hide a model error.

---

# 105. Demonstrating Loitering

Use controlled threshold:

1. person enters zone;
2. remains;
3. threshold reached;
4. event appears.

Explain:

> Loitering is based on tracked dwell time, not a separate loitering neural network.

---

# 106. Demonstrating Crowd Threshold

Use controlled scene with visible people.

Explain:

> The system counts qualifying person observations/tracks in the configured zone and applies a deterministic threshold.

---

# 107. Demonstrating Camera Offline

1. begin with healthy source;
2. stop source;
3. wait for configured offline criterion;
4. show event/state.

Do not confuse intentional disable with offline failure.

---

# 108. Operator Troubleshooting — Event Not Appearing

Check:

```text
camera healthy?
rule enabled?
correct camera/zone?
person detected?
track active?
event type configured?
real-time connected?
history API working?
```

If technical debugging is required, use deployment guide.

---

# 109. Operator Troubleshooting — Evidence Not Appearing

Check evidence state:

```text
Pending
Failed
Deleted
Unavailable
```

If failed, report to admin/developer.

Do not repeatedly refresh indefinitely.

---

# 110. Operator Troubleshooting — Acknowledge Button Missing

Possible reasons:

- insufficient permission;
- event already acknowledged;
- feature disabled;
- auth issue.

Do not manually alter browser state.

---

# 111. Operator Troubleshooting — Event List Empty

Check:

- active filters;
- date/time range;
- camera filter;
- backend connection.

Use **Reset Filters** before assuming there are no events.

---

# 112. Operator Troubleshooting — Analytics Empty

Check:

- time range;
- persisted events exist;
- filters;
- backend health.

Analytics is derived from stored events, not live detections alone.

---

# 113. Operator Troubleshooting — Wrong Camera Time

Check:

- system clock;
- timezone display policy;
- event occurrence time vs current time.

Report recurring timezone inconsistency.

---

# 114. Administrator Troubleshooting — Rule Saves but Does Not Trigger

Check:

- enabled;
- camera/zone relationship;
- threshold;
- geometry;
- rule type;
- selected position/counting method.

Then run a controlled fixture.

---

# 115. Administrator Troubleshooting — Zone Misaligned

Check:

- browser resize;
- source aspect ratio;
- normalized-coordinate conversion;
- selected camera snapshot.

Do not keep manually redrawing if the same zone shifts after resize.

---

# 116. Administrator Troubleshooting — Repeated Duplicate Events

Potential causes:

- retrigger policy;
- transition state;
- track ID instability;
- duplicate suppression bug.

Report with:

- event IDs;
- timestamps;
- camera;
- fixture.

---

# 117. Administrator Troubleshooting — False Intrusion Event

Check:

- zone geometry;
- detector false person;
- bottom-center/position method;
- tracker;
- rule threshold/cooldown.

Do not assume the AI detector is always the root cause.

---

# 118. Administrator Troubleshooting — False Loitering Event

Check:

- zone membership;
- timer reset;
- track reassociation;
- threshold;
- re-trigger behavior.

---

# 119. Administrator Troubleshooting — Crowd Count Wrong

Check:

- observed track count;
- detector misses;
- duplicate tracks;
- counting method;
- zone boundaries.

---

# 120. Administrator Troubleshooting — Violence False Positive

Record:

- event ID;
- model version;
- score;
- threshold;
- sample/clip;
- visible context.

Use false-positive feedback if implemented.

Do not silently change model metric records.

---

# 121. Safe Use of Evidence

Evidence may contain identifiable people.

Do not:

- post to social media;
- add to public Git repository;
- share outside project purpose;
- include in presentation without permission/terms review.

---

# 122. Safe Use of Screenshots

Before using a screenshot in report or PPT:

1. inspect visible people;
2. inspect source URLs;
3. inspect tokens/credentials;
4. inspect private paths;
5. crop/redact where appropriate.

---

# 123. Safe Use of Logs

Do not send screenshots containing:

- passwords;
- tokens;
- database URL;
- camera credential;
- private model/dataset path if sensitive.

---

# 124. Event Terminology Reference

## Detection

A low-level model observation.

## Track

Temporary association of an object across frames.

## Event

A persisted domain occurrence.

## Alert

Operator-facing presentation of an event requiring attention.

## Evidence

Snapshot/clip related to an event.

## Acknowledgement

Record that a user reviewed/accepted the event workflow.

## Incident

Not yet formally baselined as a separate domain object.

---

# 125. Event Type Reference

| UI Label | Meaning |
|---|---|
| Restricted Area Intrusion | person entered configured restricted polygon |
| Loitering | tracked person exceeded dwell-time rule |
| Crowd Threshold | configured person count criterion met |
| Violence/Fighting | temporal model criterion met |
| Camera Offline | active camera/source became unavailable under health policy |

---

# 126. Status Reference

## Camera

```text
Healthy
Degraded
Offline
Unknown
Disabled
```

## Evidence

```text
Pending
Available
Failed
Deleted
```

## Connection

```text
Connected
Reconnecting
Disconnected
```

---

# 127. What to Record When Reporting a Bug

Include:

```text
Date/time
Page
Camera/Event ID
Steps
Expected result
Actual result
Screenshot if safe
Browser
Commit/build if known
```

---

# 128. Bug Report Example

```text
Page: Events
Event ID: ...
Expected: acknowledgement remains after refresh
Actual: acknowledgement disappears after refresh
Steps:
1. Open event
2. Acknowledge
3. Refresh page
Browser: ...
```

Do not include password/token.

---

# 129. Operator Definition of Successful Review

An operator has successfully reviewed an event when:

- event detail opened;
- event context understood;
- evidence checked if available;
- acknowledgement submitted if appropriate;
- system confirms persisted state.

---

# 130. Administrator Definition of Successful Camera Setup

A camera setup is complete when:

- source saved;
- camera enabled;
- health understood;
- live/recorded state accurate;
- at least one controlled test completed.

---

# 131. Administrator Definition of Successful Rule Setup

A rule is complete when:

- rule linked to correct camera/zone;
- configuration saved;
- rule enabled;
- controlled positive case tested;
- controlled negative case tested;
- no duplicate flood observed.

---

# 132. Operator Manual Review Checklist

Before final submission:

- [ ] Final screenshots added if required.
- [ ] Frontend URL updated.
- [ ] Navigation matches implementation.
- [ ] Login steps match auth.
- [ ] Camera source types match actual support.
- [ ] Zone editor steps match UI.
- [ ] Rule fields match API.
- [ ] Event detail labels match UI.
- [ ] Evidence states match backend.
- [ ] Acknowledgement semantics match implementation.
- [ ] Analytics screens match implementation.
- [ ] No unimplemented page is described as available.
- [ ] No placeholder metric is shown.
- [ ] No sensitive screenshot included.
- [ ] Faculty demo walkthrough tested once.

---

# 133. Open Operator-Manual Decisions

| ID | Decision | Status |
|---|---|---|
| OPS-OD-001 | Final login workflow | `TBD` |
| OPS-OD-002 | Final navigation | `TBD` |
| OPS-OD-003 | Final frontend URL/port | `TBD` |
| OPS-OD-004 | Supported camera source kinds | `TBD` |
| OPS-OD-005 | Final zone editor interaction | `PROPOSED` |
| OPS-OD-006 | Final rule fields/defaults | `TBD` |
| OPS-OD-007 | Event lifecycle/status display | `TBD` |
| OPS-OD-008 | Multi-ack behavior | `TBD` |
| OPS-OD-009 | False-positive feedback availability | `PROPOSED` |
| OPS-OD-010 | Evidence download availability | `TBD` |
| OPS-OD-011 | AI Models page availability | `PROPOSED` |
| OPS-OD-012 | Audit page availability | `PROPOSED` |
| OPS-OD-013 | Final analytics views | `PROPOSED` |
| OPS-OD-014 | Final demo fixture identity | `TBD` |
| OPS-OD-015 | Final demo browser | `TBD` |

---

# 134. Use-Case Traceability

| Manual workflow | Use Case |
|---|---|
| Login | UC-AUTH-001 |
| Logout | UC-AUTH-002 |
| Add/edit camera | UC-CAM-001/003 |
| View camera health | UC-CAM-002 |
| Enable/disable camera | UC-CAM-004 |
| Create/edit zone | UC-ZONE-001/002 |
| Configure rules | UC-RULE-001/002/003/004 |
| Monitor feed | UC-MON-001 |
| Review/acknowledge event | UC-EVT-006 |
| False-positive feedback | UC-EVT-007 |
| Review evidence | UC-EVD-001 |
| Search history | UC-HIST-001/002 |
| Analytics | UC-ANL-001 |
| AI degraded | UC-SYS-001 |
| Reconnect | UC-SYS-004 |

---

# 135. SRS Traceability

| Manual area | Requirement families |
|---|---|
| authentication | FR-AUTH-* |
| users/roles | FR-USER-* |
| cameras | FR-CAM-* |
| zones | FR-ZONE-* |
| rules | FR-RULE-* |
| intrusion | FR-INT-* |
| loitering | FR-LOIT-* |
| crowd | FR-CROWD-* |
| violence | FR-VIO-* |
| events | FR-EVT-* |
| alerts/acknowledgement | FR-ALT-* |
| evidence | FR-EVD-* |
| history | FR-HIST-* |
| analytics | FR-ANL-* |
| UI | FR-UI-* |
| usability | NFR-USAB-* |
| privacy | NFR-PRIV-* |

---

# 136. Final Operator Rule

> **Sentinel AI should help the operator understand operational events clearly, not encourage blind trust in AI.**
>
> The correct operator workflow is:
>
> ```text
> observe
> → open event
> → inspect context
> → review evidence
> → acknowledge where appropriate
> → use history/analytics for follow-up
> ```
>
> The operator shall never assume:
>
> ```text
> model output = certainty
> track ID = identity
> acknowledgement = guilt
> no event = guaranteed safety
> ```
>
> The application is a monitoring and decision-support system with human review at the center of the workflow.
