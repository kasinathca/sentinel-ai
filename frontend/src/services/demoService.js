import { apiGet, apiRequest } from "./apiClient";

function data(body, label) {
  if (!body?.data) {
    throw new Error(`Invalid ${label} response from backend`);
  }
  return body.data;
}

export async function getDemoClips() {
  const body = await apiGet("/demo/clips");
  if (!Array.isArray(body?.data)) {
    throw new Error("Invalid demo clips response from backend");
  }
  return body.data;
}

export async function getDemoStatus() {
  return data(await apiGet("/demo/source/status"), "demo status");
}

export async function selectDemoClip(clipId) {
  return data(
    await apiRequest("/demo/source", {
      method: "PUT",
      body: JSON.stringify({ clip_id: clipId }),
    }),
    "source selection"
  );
}

export async function startDemoSource() {
  return data(
    await apiRequest("/demo/source/start", { method: "POST" }),
    "source start"
  );
}

export async function stopDemoSource() {
  return data(
    await apiRequest("/demo/source/stop", { method: "POST" }),
    "source stop"
  );
}

export async function restartDemoSource() {
  return data(
    await apiRequest("/demo/source/restart", { method: "POST" }),
    "source restart"
  );
}
