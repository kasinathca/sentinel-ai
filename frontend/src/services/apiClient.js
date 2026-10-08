const API_BASE_PATH = "/api/v1";

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_PATH}${path}`, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });

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

export function apiGet(path) {
  return apiRequest(path);
}
