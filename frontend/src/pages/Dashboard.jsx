import { useEffect, useState } from "react";
import { getEvents } from "../services/eventService";
import { getCameras } from "../services/cameraService";
import { getHealth } from "../services/healthService";
import EventCard from "../components/EventCard";
import CameraCard from "../components/CameraCard";
import EventDetails from "./EventDetails";
import EventHistory from "./EventHistory";
import CameraMonitoring from "./CameraMonitoring";

function Dashboard() {
  const [events, setEvents] = useState([]);
  const [cameras, setCameras] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const [health, setHealth] = useState(null);
  const [healthError, setHealthError] = useState(null);

  const [showHistory, setShowHistory] = useState(false);
  const [showCameras, setShowCameras] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboardData() {
      setLoading(true);
      setError(null);
      setHealthError(null);

      const [eventResult, cameraResult, healthResult] =
        await Promise.allSettled([
          getEvents(),
          getCameras(),
          getHealth(),
        ]);

      if (eventResult.status === "fulfilled") {
        setEvents(eventResult.value);
      } else {
        console.error("Failed to load events:", eventResult.reason);
        setEvents([]);
        setError("Unable to load event information.");
      }

      if (cameraResult.status === "fulfilled") {
        setCameras(cameraResult.value);
      } else {
        console.error(
          "Failed to load cameras:",
          cameraResult.reason
        );
        setCameras([]);
        setError((currentError) =>
          currentError ||
          "Unable to load camera information."
        );
      }

      if (healthResult.status === "fulfilled") {
        setHealth(healthResult.value);
        setHealthError(null);
      } else {
        console.error(
          "Failed to load backend health:",
          healthResult.reason
        );
        setHealth(null);
        setHealthError(
          "Backend health information is unavailable."
        );
      }

      setLoading(false);
    }

    loadDashboardData();
  }, []);

  const attentionEvents = events.filter(
    (event) => event.requires_attention
  );

  const acknowledgedEvents = events.filter(
    (event) => event.acknowledgement?.acknowledged === true
  );

  function getSystemStatus() {
    if (healthError) {
      return "Unavailable";
    }

    if (health?.status === "ok") {
      return "Backend Connected";
    }

    return "Unknown";
  }

  if (showHistory) {
    return (
      <EventHistory
        events={events}
        onBack={() => setShowHistory(false)}
        onSelectEvent={(event) => {
          setSelectedEvent(event);
          setShowHistory(false);
        }}
      />
    );
  }

  if (showCameras) {
    return (
      <CameraMonitoring
        cameras={cameras}
        onBack={() => setShowCameras(false)}
      />
    );
  }

  if (selectedEvent) {
    return (
      <EventDetails
        event={selectedEvent}
        onBack={() => setSelectedEvent(null)}
      />
    );
  }

  if (loading) {
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <div>
            <h1>Sentinel AI</h1>
            <p>Operator Dashboard</p>
          </div>

          <div className="system-status">
            System Status: Loading
          </div>
        </header>

        <main>
          <section className="state-card">
            <h2>Loading dashboard</h2>
            <p>
              Camera, event, and backend health information
              is being loaded.
            </p>
          </section>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <div>
            <h1>Sentinel AI</h1>
            <p>Operator Dashboard</p>
          </div>

          <div className="system-status">
            System Status: {getSystemStatus()}
          </div>
        </header>

        <main>
          <section className="state-card error-state">
            <h2>Unable to load dashboard data</h2>
            <p>{error}</p>

            {healthError && (
              <p>{healthError}</p>
            )}

            <p>
              Please check the backend connection and try
              again.
            </p>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>Sentinel AI</h1>
          <p>Operator Dashboard</p>
        </div>

        <div className="dashboard-actions">
          <button
            className="history-button"
            onClick={() => setShowCameras(true)}
          >
            Camera Monitoring
          </button>

          <button
            className="history-button"
            onClick={() => setShowHistory(true)}
          >
            Event History
          </button>

          <div className="system-status">
            System Status: {getSystemStatus()}
          </div>
        </div>
      </header>

      <main>
        {healthError && (
          <section className="state-card error-state">
            <h3>Backend health unavailable</h3>
            <p>{healthError}</p>
          </section>
        )}

        <section className="dashboard-summary">
          <div className="summary-card">
            <span>Total Events</span>
            <strong>{events.length}</strong>
          </div>

          <div className="summary-card">
            <span>Requires Attention</span>
            <strong>{attentionEvents.length}</strong>
          </div>

          <div className="summary-card">
            <span>Acknowledged</span>
            <strong>{acknowledgedEvents.length}</strong>
          </div>
        </section>

        <section className="cameras-section">
          <div className="section-heading">
            <h2>Cameras</h2>
            <span>{cameras.length} cameras</span>
          </div>

          {cameras.length === 0 ? (
            <div className="state-card">
              <h3>No cameras available</h3>
              <p>
                No camera information is currently available
                from the backend.
              </p>
            </div>
          ) : (
            <div className="camera-grid">
              {cameras.map((camera) => (
                <CameraCard
                  key={camera.id}
                  camera={camera}
                />
              ))}
            </div>
          )}
        </section>

        <section className="attention-section">
          <div className="section-heading">
            <h2>Attention Required</h2>
            <span>{attentionEvents.length} events</span>
          </div>

          {attentionEvents.length === 0 ? (
            <div className="state-card">
              <h3>No events require attention</h3>
              <p>
                There are currently no events requiring
                operator attention.
              </p>
            </div>
          ) : (
            <div className="event-list">
              {attentionEvents.map((event) => (
                <EventCard
                  key={event.id}
                  event={event}
                  onSelect={setSelectedEvent}
                />
              ))}
            </div>
          )}
        </section>

        <section className="events-section">
          <div className="section-heading">
            <h2>Recent Events</h2>
            <span>{events.length} events</span>
          </div>

          {events.length === 0 ? (
            <div className="state-card">
              <h3>No events recorded</h3>
              <p>
                No security events are currently available
                from the backend.
              </p>
            </div>
          ) : (
            <div className="event-list">
              {events.map((event) => (
                <EventCard
                  key={event.id}
                  event={event}
                  onSelect={setSelectedEvent}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;