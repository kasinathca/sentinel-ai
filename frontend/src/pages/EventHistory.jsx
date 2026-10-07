import { useState } from "react";

const EVENT_LABELS = {
  restricted_area_intrusion: "Restricted Area Intrusion",
  loitering: "Loitering",
  crowd_threshold: "Crowd Threshold",
  violence_fighting: "Violence / Fighting",
  camera_offline: "Camera Offline",
};

function EventHistory({
  events = [],
  onBack,
  onSelectEvent,
}) {
  const [eventType, setEventType] = useState("all");
  const [status, setStatus] = useState("all");
  const [acknowledged, setAcknowledged] = useState("all");

  const filteredEvents = events.filter((event) => {
    const matchesType =
      eventType === "all" ||
      event.event_type === eventType;

    const matchesStatus =
      status === "all" ||
      event.status === status;

    const matchesAcknowledgement =
      acknowledged === "all" ||
      (acknowledged === "yes" &&
        event.acknowledgement.acknowledged) ||
      (acknowledged === "no" &&
        !event.acknowledgement.acknowledged);

    return (
      matchesType &&
      matchesStatus &&
      matchesAcknowledgement
    );
  });

  return (
    <div className="event-history">
      <button className="back-button" onClick={onBack}>
        ← Back to Dashboard
      </button>

      <header className="history-header">
        <div>
          <p className="details-label">Event Management</p>
          <h1>Event History</h1>
        </div>

        <span className="history-count">
          {filteredEvents.length} events
        </span>
      </header>

      <section className="filters-card">
        <h2>Filters</h2>

        <div className="filters-grid">
          <label>
            Event Type
            <select
              value={eventType}
              onChange={(event) =>
                setEventType(event.target.value)
              }
            >
              <option value="all">All Events</option>
              <option value="restricted_area_intrusion">
                Restricted Area Intrusion
              </option>
              <option value="loitering">
                Loitering
              </option>
              <option value="crowd_threshold">
                Crowd Threshold
              </option>
              <option value="violence_fighting">
                Violence / Fighting
              </option>
              <option value="camera_offline">
                Camera Offline
              </option>
            </select>
          </label>

          <label>
            Status
            <select
              value={status}
              onChange={(event) =>
                setStatus(event.target.value)
              }
            >
              <option value="all">All Statuses</option>
              <option value="open">Open</option>
              <option value="acknowledged">
                Acknowledged
              </option>
              <option value="resolved">Resolved</option>
            </select>
          </label>

          <label>
            Acknowledgement
            <select
              value={acknowledged}
              onChange={(event) =>
                setAcknowledged(event.target.value)
              }
            >
              <option value="all">All</option>
              <option value="yes">Acknowledged</option>
              <option value="no">Not Acknowledged</option>
            </select>
          </label>
        </div>
      </section>

      <section className="history-card">
        <div className="history-table">
          <div className="history-row history-row-header">
            <span>Event</span>
            <span>Camera</span>
            <span>Time</span>
            <span>Status</span>
            <span>Acknowledged</span>
          </div>

          {filteredEvents.length === 0 ? (
            <div className="empty-history">
              No events match the selected filters.
            </div>
          ) : (
            filteredEvents.map((event) => (
              <button
                className="history-row history-row-button"
                key={event.id}
                onClick={() => onSelectEvent(event)}
                type="button"
              >
                <span>
                  {EVENT_LABELS[event.event_type] ||
                    event.event_type}
                </span>

                <span>{event.camera.name}</span>

                <span>
                  {new Date(
                    event.occurred_at
                  ).toLocaleString()}
                </span>

                <span>
                  <span
                    className={`event-status ${event.status}`}
                  >
                    {event.status}
                  </span>
                </span>

                <span>
                  {event.acknowledgement.acknowledged
                    ? "Yes"
                    : "No"}
                </span>
              </button>
            ))
          )}
        </div>
      </section>
    </div>
  );
}

export default EventHistory;