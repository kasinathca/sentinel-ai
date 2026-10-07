import { useState } from "react";

function CameraMonitoring({
  cameras = [],
  onBack,
}) {
  const [selectedCamera, setSelectedCamera] = useState(
    cameras[0] || null
  );

  if (!selectedCamera) {
    return (
      <div className="camera-monitoring">
        <button className="back-button" onClick={onBack}>
          ← Back to Dashboard
        </button>

        <section className="state-card">
          <h2>No cameras available</h2>
          <p>
            No camera information is currently available
            from the backend.
          </p>
        </section>
      </div>
    );
  }

  const health = selectedCamera.health || {};

  return (
    <div className="camera-monitoring">
      <button className="back-button" onClick={onBack}>
        ← Back to Dashboard
      </button>

      <header className="camera-monitoring-header">
        <div>
          <p className="details-label">Camera Monitoring</p>
          <h1>{selectedCamera.name}</h1>
          <p>
            {selectedCamera.description ||
              "No camera description available."}
          </p>
        </div>

        <div className="camera-health-badge">
          {health.state || "unknown"}
        </div>
      </header>

      <section className="camera-monitoring-layout">
        <aside className="camera-list-panel">
          <h2>Cameras</h2>

          {cameras.length === 0 ? (
            <p>No cameras available.</p>
          ) : (
            <div className="camera-monitoring-list">
              {cameras.map((camera) => (
                <button
                  key={camera.id}
                  type="button"
                  className={`camera-list-item ${
                    selectedCamera.id === camera.id
                      ? "selected"
                      : ""
                  }`}
                  onClick={() => setSelectedCamera(camera)}
                >
                  <strong>{camera.name}</strong>

                  <span>
                    {camera.health?.state || "unknown"}
                  </span>
                </button>
              ))}
            </div>
          )}
        </aside>

        <main className="camera-view-panel">
          <section className="camera-stream-placeholder">
            <div>
              <h2>Video stream unavailable</h2>

              <p>
                Video stream not connected in current
                integration.
              </p>

              <p>
                The current backend provides camera metadata
                and health information, but no live video
                stream or snapshot endpoint is available to
                this frontend.
              </p>
            </div>
          </section>

          <section className="details-card">
            <h2>Camera Information</h2>

            <div className="details-grid">
              <div>
                <span>Camera ID</span>
                <strong>{selectedCamera.id}</strong>
              </div>

              <div>
                <span>Name</span>
                <strong>{selectedCamera.name}</strong>
              </div>

              <div>
                <span>Source Kind</span>
                <strong>
                  {selectedCamera.source_kind ||
                    "Not set"}
                </strong>
              </div>

              <div>
                <span>Enabled</span>
                <strong>
                  {selectedCamera.enabled ? "Yes" : "No"}
                </strong>
              </div>

              <div>
                <span>Health</span>
                <strong>
                  {health.state || "unknown"}
                </strong>
              </div>

              <div>
                <span>Last Frame</span>
                <strong>
                  {health.last_frame_at
                    ? new Date(
                        health.last_frame_at
                      ).toLocaleString()
                    : "Unavailable"}
                </strong>
              </div>

              <div>
                <span>Last Health Check</span>
                <strong>
                  {health.last_health_check_at
                    ? new Date(
                        health.last_health_check_at
                      ).toLocaleString()
                    : "Unavailable"}
                </strong>
              </div>
            </div>
          </section>
        </main>
      </section>
    </div>
  );
}

export default CameraMonitoring;