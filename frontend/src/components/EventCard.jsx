const EVENT_LABELS = {
  restricted_area_intrusion: "Restricted Area Intrusion",
  loitering: "Loitering",
  crowd_threshold: "Crowd Threshold",
  violence_fighting: "Violence / Fighting",
  camera_offline: "Camera Offline",
};

function EventCard({ event, onSelect }) {
  const eventLabel =
    EVENT_LABELS[event.event_type] || event.event_type;

  const acknowledged =
    event.acknowledgement?.acknowledged === true;

  const statusLabel = event.status || "No lifecycle status";

  const cameraName =
    event.camera?.name || "Unavailable";

  const occurredAt = event.occurred_at
    ? new Date(event.occurred_at).toLocaleString()
    : "Unavailable";

  return (
    <button
      className="event-card"
      onClick={() => onSelect(event)}
      type="button"
    >
      <div className="event-card-header">
        <h3>{eventLabel}</h3>

        <span
          className={`event-status ${
            acknowledged
              ? "acknowledged"
              : event.status || ""
          }`}
        >
          {acknowledged
            ? "Acknowledged"
            : statusLabel}
        </span>
      </div>

      <p>
        <strong>Camera:</strong> {cameraName}
      </p>

      <p>
        <strong>Time:</strong> {occurredAt}
      </p>

      <p>
        <strong>Attention:</strong>{" "}
        {event.requires_attention
          ? "Required"
          : "Not required"}
      </p>

      <p>
        <strong>Acknowledged:</strong>{" "}
        {acknowledged ? "Yes" : "No"}
      </p>
    </button>
  );
}

export default EventCard;