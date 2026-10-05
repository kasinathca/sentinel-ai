import { apiGet } from "./apiClient";

export async function getCameras() {
  const body = await apiGet("/cameras");

  if (!Array.isArray(body?.data)) {
    throw new Error("Invalid cameras response from backend");
  }

  return body.data;
}

export async function getCameraById(cameraId) {
  const body = await apiGet(`/cameras/${cameraId}`);

  if (!body?.data) {
    throw new Error("Invalid camera response from backend");
  }

  return body.data;
}