import { useState } from "react";
import { mockEvents } from "../mocks/mockEvents";
import { mockCameras } from "../mocks/mockCameras";
import EventCard from "../components/EventCard";
import CameraCard from "../components/CameraCard";
import EventDetails from "./EventDetails";
import EventHistory from "./EventHistory";
import CameraMonitoring from "./CameraMonitoring";

function Dashboard() {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [showCameras, setShowCameras] = useState(false);

  const attentionEvents = mockEvents.filter(
    (event) => event.requires_attention
  );

  const acknowledgedEvents = mockEvents.filter(
    (event) => event.acknowledgement.acknowledged
  );

  if (showHistory) {
    return (
      <EventHistory
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
            System Status: Operational
          </div>
        </div>
      </header>

      <main>
        <section className="dashboard-summary">
          <div className="summary-card">
            <span>Total Events</span>
            <strong>{mockEvents.length}</strong>
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
            <span>{mockCameras.length} cameras</span>
          </div>

          <div className="camera-grid">
            {mockCameras.map((camera) => (
              <CameraCard
                key={camera.id}
                camera={camera}
              />
            ))}
          </div>
        </section>

        <section className="attention-section">
          <div className="section-heading">
            <h2>Attention Required</h2>
            <span>{attentionEvents.length} events</span>
          </div>

          <div className="event-list">
            {attentionEvents.map((event) => (
              <EventCard
                key={event.id}
                event={event}
                onSelect={setSelectedEvent}
              />
            ))}
          </div>
        </section>

        <section className="events-section">
          <div className="section-heading">
            <h2>Recent Events</h2>
            <span>{mockEvents.length} events</span>
          </div>

          <div className="event-list">
            {mockEvents.map((event) => (
              <EventCard
                key={event.id}
                event={event}
                onSelect={setSelectedEvent}
              />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;