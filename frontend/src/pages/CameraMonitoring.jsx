import { useEffect, useMemo, useState } from "react";
import {
  getDemoClips,
  getDemoStatus,
  restartDemoSource,
  selectDemoClip,
  startDemoSource,
  stopDemoSource,
} from "../services/demoService";
import { describeRollingCondition, describeSessionDetection, isClipSelectable } from "../services/demoViewModel";

const DEMO_CAMERA_ID = "02b1cbc6-d4a3-5630-8c4e-27cdcc062d57";
const ACTIVE_STATES = new Set(["starting", "playing", "loop-restarting"]);

function CameraMonitoring({ cameras = [], onBack }) {
  const camera = useMemo(
    () => cameras.find((item) => item.id === DEMO_CAMERA_ID) || null,
    [cameras]
  );
  const [clips, setClips] = useState([]);
  const [status, setStatus] = useState(null);
  const [selectedClipId, setSelectedClipId] = useState("");
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  async function refreshVideos() {
    const availableClips = await getDemoClips();
    setClips(availableClips);
    setSelectedClipId((current) => {
      const currentReady = availableClips.some(
        (clip) => clip.clip_id === current && isClipSelectable(clip)
      );
      return currentReady
        ? current
        : availableClips.find(isClipSelectable)?.clip_id || "";
    });
    return availableClips;
  }

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [availableClips, currentStatus] = await Promise.all([
          getDemoClips(),
          getDemoStatus(),
        ]);
        if (!cancelled) {
          setClips(availableClips);
          setStatus(currentStatus);
          setSelectedClipId(currentStatus.clip_id || availableClips[0]?.clip_id || "");
          setError(null);
        }
      } catch (loadError) {
        if (!cancelled) setError(loadError.message);
      }
    }
    load();
    const poll = window.setInterval(async () => {
      try {
        const currentStatus = await getDemoStatus();
        if (!cancelled) {
          setStatus(currentStatus);
          setError(null);
        }
      } catch (pollError) {
        if (!cancelled) setError(pollError.message);
      }
    }, 1000);
    return () => {
      cancelled = true;
      window.clearInterval(poll);
    };
  }, []);

  useEffect(() => {
    if (!clips.some((clip) => ["waiting_for_file", "validating", "transcoding"].includes(clip.state))) return undefined;
    let cancelled = false;
    const poll = window.setInterval(async () => {
      try {
        const availableClips = await getDemoClips();
        if (!cancelled) setClips(availableClips);
      } catch (pollError) {
        if (!cancelled) setError(pollError.message);
      }
    }, 1000);
    return () => {
      cancelled = true;
      window.clearInterval(poll);
    };
  }, [clips]);

  async function run(action) {
    setBusy(true);
    setError(null);
    try {
      await action();
      setStatus(await getDemoStatus());
    } catch (actionError) {
      setError(actionError.message);
    } finally {
      setBusy(false);
    }
  }

  async function start() {
    await run(async () => {
      if (status?.clip_id !== selectedClipId) await selectDemoClip(selectedClipId);
      return startDemoSource();
    });
  }

  if (!camera) {
    return (
      <div className="camera-monitoring">
        <button className="back-button" onClick={onBack}>← Back to Dashboard</button>
        <section className="state-card error-state"><h2>DEMO-CAM-01 unavailable</h2><p>The canonical virtual camera is not initialized in the backend.</p></section>
      </div>
    );
  }

  const active = ACTIVE_STATES.has(status?.state);
  const ai = status?.ai || {};
  const selectedClip = clips.find((clip) => clip.clip_id === selectedClipId);
  const pendingClips = clips.filter((clip) => clip.state !== "ready");

  return (
    <div className="camera-monitoring">
      <button className="back-button" onClick={onBack}>← Back to Dashboard</button>
      <header className="camera-monitoring-header">
        <div><p className="details-label">Single Virtual CCTV</p><h1>{camera.name}</h1><p>Controlled prerecorded footage presented as a looping virtual camera.</p></div>
        <div className={`camera-health-badge ${active ? "online" : "stopped"}`}>{status?.state || "unavailable"}</div>
      </header>

      {error && <section className="state-card error-state"><strong>Demo unavailable</strong><p>{error}</p></section>}

      <section className="demo-control-panel">
        <div className="demo-panel-heading">
          <div><h2>Available Videos</h2><p>Drop a supported video into the controlled source directory, then refresh.</p></div>
          <button type="button" disabled={busy || active} onClick={() => run(refreshVideos)}>Refresh Videos</button>
        </div>
        <label>Sentinel source
          <select value={selectedClipId} disabled={busy || active} onChange={(event) => setSelectedClipId(event.target.value)}>
            {!clips.length && <option value="">No videos discovered</option>}
            {clips.map((clip) => <option key={clip.clip_id} value={clip.clip_id} disabled={!isClipSelectable(clip)}>{clip.display_name} — {clip.state.replaceAll("_", " ")}</option>)}
          </select>
        </label>
        {pendingClips.length > 0 && <div className="ingest-list">{pendingClips.map((clip) => <p key={clip.clip_id}><strong>{clip.display_name}</strong>: {clip.reason || clip.state.replaceAll("_", " ")}</p>)}</div>}
        {selectedClip?.media && <p className="prepared-media">Sentinel source: {selectedClip.normalization === "transcoded" ? "Prepared" : "Validated directly"} · {selectedClip.media.width}×{selectedClip.media.height} · {selectedClip.media.codec.toUpperCase()} · {selectedClip.media.fps} FPS</p>}
        <div className="demo-actions">
          <button type="button" disabled={busy || active || !selectedClipId} onClick={start}>Start</button>
          <button type="button" disabled={busy || !active} onClick={() => run(stopDemoSource)}>Stop</button>
          <button type="button" disabled={busy || !active} onClick={() => run(restartDemoSource)}>Restart</button>
        </div>
      </section>

      {ai.event_id && status?.session_id === ai.source_session_id && (
        <section className="violence-alert" role="alert"><strong>Qualified violence / fighting alert</strong><span>Persisted event {ai.event_id}</span></section>
      )}

      <section className="camera-live-panel">
        <div className="camera-viewer-header"><div><h2>{selectedClip?.display_name || "No source selected"}</h2><p>Source session: {status?.session_id || "none"}</p></div><span>Loops completed: {status?.loop_count ?? 0}</span></div>
        <div className="live-video-frame">
          {active ? <img src={`/api/v1/cameras/${camera.id}/stream`} alt={`${camera.name} virtual CCTV stream`} /> : <div><h3>Source stopped</h3><p>Select an approved clip and start the virtual camera.</p></div>}
        </div>
      </section>

      <section className="ai-status-panel">
        <h2>Frozen Violence AI</h2>
        <div className="details-grid">
          <div><span>Runtime state</span><strong>{ai.state || "unavailable"}</strong></div>
          <div><span>Processed windows (session)</span><strong>{ai.processed_windows_total ?? ai.processed_windows ?? 0}</strong></div>
          <div><span>Analyzed replay passes</span><strong>{ai.analyzed_passes ?? 0}</strong></div>
          <div><span>Latest violence score</span><strong>{ai.latest_score == null ? "Not available" : ai.latest_score.toFixed(6)}</strong></div>
          <div><span>Latest observation</span><strong>{ai.latest_score == null ? "Not available" : ai.latest_score_positive ? "Positive" : "Negative"}</strong></div>
          <div><span>History</span><strong>{ai.history_count ?? 0} / {ai.m_history ?? 5} observations</strong></div>
          <div><span>Current rolling window</span><strong>{ai.positive_count ?? 0} / {ai.m_history ?? 5} positive</strong></div>
          <div><span>Current rolling qualification</span><strong>{describeRollingCondition(ai)}</strong></div>
          <div><span>Positive observations this session</span><strong>{ai.positive_windows_total ?? 0} / {ai.processed_windows_total ?? 0}</strong></div>
          <div><span>Strongest rolling result observed</span><strong>{ai.max_positive_count_observed_in_any_5_window ?? 0} / {ai.m_history ?? 5} positive</strong></div>
          <div><span>Violence detected this session</span><strong>{describeSessionDetection(ai)}</strong></div>
          <div><span>First qualified at</span><strong>{ai.first_qualified_at || "Not detected"}</strong></div>
          <div><span>Persisted event</span><strong>{ai.event_id || "None"}</strong></div>
          <div><span>Frozen threshold</span><strong>{ai.threshold ?? 0.906}</strong></div>
          <div><span>Score meaning</span><strong>{ai.score_semantics || "uncalibrated fighting score"}</strong></div>
        </div>
        {ai.error && <p className="ai-error">{ai.error}</p>}
      </section>
    </div>
  );
}

export default CameraMonitoring;
