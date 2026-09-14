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

  return (
    <button
      className="event-card"
      onClick={() => onSelect(event)}
      type="button"
    >
      <div className="event-card-header">
        <h3>{eventLabel}</h3>

        <span className={`event-status ${event.status}`}>
          {event.status}
        </span>
      </div>

      <p>
        <strong>Camera:</strong> {event.camera.name}
      </p>

      <p>
        <strong>Time:</strong>{" "}
        {new Date(event.occurred_at).toLocaleString()}
      </p>

      <p>
        <strong>Attention:</strong>{" "}
        {event.requires_attention ? "Required" : "Not required"}
      </p>

      <p>
        <strong>Acknowledged:</strong>{" "}
        {event.acknowledgement.acknowledged ? "Yes" : "No"}
      </p>
    </button>
  );
}

export default EventCard;