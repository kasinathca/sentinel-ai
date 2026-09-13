function CameraCard({ camera }) {
  const healthState = camera.health.state;

  return (
    <div className="camera-card">
      <div className="camera-card-header">
        <div>
          <h3>{camera.name}</h3>
          <p>{camera.description}</p>
        </div>

        <span className={`camera-health ${healthState}`}>
          {healthState}
        </span>
      </div>

      <div className="camera-info">
        <p>
          <strong>Camera ID:</strong> {camera.id}
        </p>

        <p>
          <strong>Enabled:</strong>{" "}
          {camera.enabled ? "Yes" : "No"}
        </p>

        <p>
          <strong>Last frame:</strong>{" "}
          {camera.health.last_frame_at
            ? new Date(
                camera.health.last_frame_at
              ).toLocaleString()
            : "Unavailable"}
        </p>
      </div>
    </div>
  );
}

export default CameraCard;