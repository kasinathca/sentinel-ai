const API_BASE_PATH = "/api/v1";

export async function apiGet(path) {
  const response = await fetch(`${API_BASE_PATH}${path}`);

  let body = null;

  try {
    body = await response.json();
  } catch {
    body = null;
  }

  if (!response.ok) {
    const message =
      body?.error?.message ||
      body?.detail ||
      `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return body;
}