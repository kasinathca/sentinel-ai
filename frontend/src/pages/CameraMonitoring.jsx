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

        <h2>No cameras available</h2>
      </div>
    );
  }

  return (
    <div className="camera-monitoring">
      <button className="back-button" onClick={onBack}>
        ← Back to Dashboard
      </button>

      <header className="monitoring-header">
        <div>
          <p className="details-label">Live Surveillance</p>
          <h1>Camera Monitoring</h1>
        </div>

        <span className="camera-count">
          {cameras.length} cameras
        </span>
      </header>

      <section className="camera-viewer">
        <div className="camera-viewer-header">
          <div>
            <h2>{selectedCamera.name}</h2>
            <p>{selectedCamera.description}</p>
          </div>

          <span
            className={`camera-health ${selectedCamera.health.state}`}
          >
            {selectedCamera.health.state}
          </span>
        </div>

        <div className="video-placeholder">
          <div className="video-placeholder-content">
            <div className="camera-icon">CAM</div>

            <h3>Camera Feed</h3>

            <p>
              Live video integration will be connected
              through the backend camera/stream contract.
            </p>

            <span>
              Camera ID: {selectedCamera.id}
            </span>
          </div>
        </div>

        <div className="camera-viewer-info">
          <div>
            <span>Source</span>
            <strong>
              {selectedCamera.source_kind}
            </strong>
          </div>

          <div>
            <span>Enabled</span>
            <strong>
              {selectedCamera.enabled ? "Yes" : "No"}
            </strong>
          </div>

          <div>
            <span>Last Frame</span>
            <strong>
              {selectedCamera.health.last_frame_at
                ? new Date(
                    selectedCamera.health.last_frame_at
                  ).toLocaleString()
                : "Unavailable"}
            </strong>
          </div>
        </div>
      </section>

      <section className="camera-selector-section">
        <div className="section-heading">
          <h2>Available Cameras</h2>
          <span>{cameras.length} cameras</span>
        </div>

        <div className="camera-selector-grid">
          {cameras.map((camera) => (
            <button
              key={camera.id}
              type="button"
              className={`camera-selector ${
                selectedCamera.id === camera.id
                  ? "selected"
                  : ""
              }`}
              onClick={() => setSelectedCamera(camera)}
            >
              <div className="camera-selector-header">
                <strong>{camera.name}</strong>

                <span
                  className={`camera-health ${camera.health.state}`}
                >
                  {camera.health.state}
                </span>
              </div>

              <span>{camera.id}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

export default CameraMonitoring;