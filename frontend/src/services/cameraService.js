import { mockCameras } from "../mocks/mockCameras";

export async function getCameras() {
  return Promise.resolve(mockCameras);
}

export async function getCameraById(cameraId) {
  const camera = mockCameras.find(
    (item) => item.id === cameraId
  );

  return Promise.resolve(camera || null);
}