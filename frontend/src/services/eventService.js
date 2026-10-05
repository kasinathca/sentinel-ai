import { apiGet } from "./apiClient";

export async function getEvents() {
  const body = await apiGet("/events");

  if (!Array.isArray(body?.data)) {
    throw new Error("Invalid events response from backend");
  }

  return body.data;
}

export async function getEventById(eventId) {
  const body = await apiGet(`/events/${eventId}`);

  if (!body?.data) {
    throw new Error("Invalid event response from backend");
  }

  return body.data;
}