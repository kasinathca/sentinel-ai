const EVENT_LABELS = {
  restricted_area_intrusion: "Restricted Area Intrusion",
  loitering: "Loitering",
  crowd_threshold: "Crowd Threshold",
  violence_fighting: "Violence / Fighting",
  camera_offline: "Camera Offline",
};

const CONTEXT_LABELS = {
  rule_id: "Rule ID",
  zone_id: "Zone ID",
  geometry_version: "Geometry Version",
  track_id: "Track ID",
  observed_count: "Observed Count",
  threshold_count: "Threshold Count",
  counting_method: "Counting Method",
  observed_dwell_ms: "Observed Dwell Time",
  threshold_ms: "Threshold Time",
  track_loss_grace_ms: "Track Loss Grace",
  retrigger_after_ms: "Retrigger After",
  position_method: "Position Method",
  cooldown: "Cooldown",
  output_label: "Output Label",
  score: "Model Score",
  event_threshold: "Event Threshold",
  score_semantics: "Score Semantics",
  window_started_at: "Window Started",
  window_ended_at: "Window Ended",
  last_frame_at: "Last Frame",
  offline_after_ms: "Offline After",
  reason: "Reason",
  health_state_before: "Health Before",
  health_state_after: "Health After",
};

function formatContextValue(key, value) {
  if (value === null || value === undefined) {
    return "Unavailable";
  }

  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }

  if (
    typeof value === "string" &&
    (key.endsWith("_at") ||
      key.includes("started") ||
      key.includes("ended"))
  ) {
    return new Date(value).toLocaleString();
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

function EventDetails({
  event,
  onBack,
  onAcknowledge,
}) {
  if (!event) {
    return (
      <div className="event-details">
        <h2>Event not found</h2>

        <button className="back-button" onClick={onBack}>
          ← Back to Dashboard
        </button>
      </div>
    );
  }

  const eventLabel =
    EVENT_LABELS[event.event_type] || event.event_type;

  const contextEntries = Object.entries(event.context || {});

  const acknowledged =
    event.acknowledgement?.acknowledged ?? false;

  return (
    <div className="event-details">
      <button className="back-button" onClick={onBack}>
        ← Back to Dashboard
      </button>

      <header className="event-details-header">
        <div>
          <p className="details-label">Security Event</p>
          <h1>{eventLabel}</h1>
        </div>

        <span
          className={`event-status ${
            acknowledged ? "acknowledged" : event.status
          }`}
        >
          {acknowledged ? "acknowledged" : event.status}
        </span>
      </header>

      <section className="details-card">
        <h2>Event Information</h2>

        <div className="details-grid">
          <div>
            <span>Event ID</span>
            <strong>{event.id}</strong>
          </div>

          <div>
            <span>Camera</span>
            <strong>{event.camera.name}</strong>
          </div>

          <div>
            <span>Occurred At</span>
            <strong>
              {new Date(event.occurred_at).toLocaleString()}
            </strong>
          </div>

          <div>
            <span>Created At</span>
            <strong>
              {new Date(event.created_at).toLocaleString()}
            </strong>
          </div>

          <div>
            <span>Requires Attention</span>
            <strong>
              {event.requires_attention ? "Yes" : "No"}
            </strong>
          </div>

          <div>
            <span>Acknowledged</span>
            <strong>
              {acknowledged ? "Yes" : "No"}
            </strong>
          </div>
        </div>

        {!acknowledged && (
          <div className="acknowledgement-section">
            <button
              className="acknowledge-button"
              onClick={() => onAcknowledge(event.id)}
              type="button"
            >
              Acknowledge Event
            </button>

            <p>
              This is a frontend mock action. Backend
              acknowledgement integration will be connected
              after the API contract is baselined.
            </p>
          </div>
        )}

        {acknowledged && (
          <div className="acknowledgement-success">
            Event acknowledged.
          </div>
        )}
      </section>

      <section className="details-card">
        <h2>Evidence</h2>

        <div className="evidence-summary">
          <div>
            <span>Available</span>
            <strong>{event.evidence.available_count}</strong>
          </div>

          <div>
            <span>Pending</span>
            <strong>{event.evidence.pending_count}</strong>
          </div>

          <div>
            <span>Failed</span>
            <strong>{event.evidence.failed_count}</strong>
          </div>
        </div>
      </section>

      <section className="details-card">
        <h2>Event Context</h2>

        <div className="context-grid">
          {contextEntries.map(([key, value]) => (
            <div className="context-item" key={key}>
              <span>
                {CONTEXT_LABELS[key] || key}
              </span>

              <strong>
                {formatContextValue(key, value)}
              </strong>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default EventDetails;