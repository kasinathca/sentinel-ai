import { useCallback, useEffect, useState } from "react";
import { getEvents } from "../services/eventService";
import { getCameras } from "../services/cameraService";
import { getHealth } from "../services/healthService";
import { getDemoStatus } from "../services/demoService";
import {
  currentSessionAttentionEvents,
  historicalAttentionEvents,
} from "../services/dashboardViewModel";
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
  const [demoStatus, setDemoStatus] = useState(null);

  const [showHistory, setShowHistory] = useState(false);
  const [showCameras, setShowCameras] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboardData = useCallback(async (showLoading = true) => {
    if (showLoading) setLoading(true);
    setError(null);
    setHealthError(null);

    const [eventResult, cameraResult, healthResult, demoResult] =
      await Promise.allSettled([
        getEvents(),
        getCameras(),
        getHealth(),
        getDemoStatus(),
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

      if (demoResult.status === "fulfilled") {
        setDemoStatus(demoResult.value);
      } else {
        console.error("Failed to load demo status:", demoResult.reason);
        setDemoStatus(null);
      }

    setLoading(false);
  }, []);

  useEffect(() => {
    // oxlint-disable-next-line react/set-state-in-effect -- loading external API state is the effect's purpose.
    loadDashboardData();
  }, [loadDashboardData]);

  const currentAttentionEvents = currentSessionAttentionEvents(events, demoStatus);
  const historicalAttention = historicalAttentionEvents(events, demoStatus);

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
        onBack={() => {
          setShowCameras(false);
          loadDashboardData(false);
        }}
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
            <span>Persisted Events</span>
            <strong>{events.length}</strong>
          </div>

          <div className="summary-card">
            <span>Current Session Alerts</span>
            <strong>{currentAttentionEvents.length}</strong>
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
            <h2>Current Live Session</h2>
            <span>{currentAttentionEvents.length} alerts</span>
          </div>

          {currentAttentionEvents.length === 0 ? (
            <div className="state-card">
              <h3>No qualified alert in the current session</h3>
              <p>
                Historical records are listed separately below and are not
                presented as live alerts.
              </p>
            </div>
          ) : (
            <div className="event-list">
              {currentAttentionEvents.map((event) => (
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
            <h2>Persisted Event History</h2>
            <span>{events.length} events · {historicalAttention.length} historical attention records</span>
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
