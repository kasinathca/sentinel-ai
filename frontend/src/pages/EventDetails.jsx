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

function getStatusLabel(status, acknowledged) {
  if (acknowledged) {
    return "Acknowledged";
  }

  if (!status) {
    return "No lifecycle status";
  }

  return status;
}

function EventDetails({ event, onBack }) {
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
    event.acknowledgement?.acknowledged === true;

  const statusLabel = getStatusLabel(
    event.status,
    acknowledged
  );

  const evidence = event.evidence || {};

  const cameraName =
    event.camera?.name || "Unavailable";

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
            acknowledged
              ? "acknowledged"
              : event.status || ""
          }`}
        >
          {statusLabel}
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
            <strong>{cameraName}</strong>
          </div>

          <div>
            <span>Occurred At</span>
            <strong>
              {event.occurred_at
                ? new Date(
                    event.occurred_at
                  ).toLocaleString()
                : "Unavailable"}
            </strong>
          </div>

          <div>
            <span>Created At</span>
            <strong>
              {event.created_at
                ? new Date(
                    event.created_at
                  ).toLocaleString()
                : "Unavailable"}
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

          <div>
            <span>Severity</span>
            <strong>
              {event.severity || "Not set"}
            </strong>
          </div>

          <div>
            <span>Lifecycle Status</span>
            <strong>
              {event.status || "No lifecycle status"}
            </strong>
          </div>
        </div>

        <div className="acknowledgement-section">
          {acknowledged ? (
            <>
              <div className="acknowledgement-success">
                Event acknowledged by the backend.
              </div>

              {event.acknowledgement
                ?.first_acknowledged_at && (
                <p>
                  Acknowledged at{" "}
                  {new Date(
                    event.acknowledgement
                      .first_acknowledged_at
                  ).toLocaleString()}
                </p>
              )}
            </>
          ) : (
            <p>
              Event acknowledgement is not available in the
              current backend integration.
            </p>
          )}
        </div>
      </section>

      <section className="details-card">
        <h2>Evidence</h2>

        <div className="evidence-summary">
          <div>
            <span>Available</span>
            <strong>
              {evidence.available_count ?? 0}
            </strong>
          </div>

          <div>
            <span>Pending</span>
            <strong>
              {evidence.pending_count ?? 0}
            </strong>
          </div>

          <div>
            <span>Failed</span>
            <strong>
              {evidence.failed_count ?? 0}
            </strong>
          </div>
        </div>
      </section>

      <section className="details-card">
        <h2>Event Context</h2>

        {contextEntries.length === 0 ? (
          <p>No additional event context is available.</p>
        ) : (
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
        )}
      </section>
    </div>
  );
}

export default EventDetails;