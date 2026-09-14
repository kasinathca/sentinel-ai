import { mockEvents } from "../mocks/mockEvents";

export async function getEvents() {
  return Promise.resolve(mockEvents);
}

export async function getEventById(eventId) {
  const event = mockEvents.find(
    (item) => item.id === eventId
  );

  return Promise.resolve(event || null);
}

export async function acknowledgeEvent(eventId) {
  const event = mockEvents.find(
    (item) => item.id === eventId
  );

  if (!event) {
    throw new Error("Event not found");
  }

  return Promise.resolve({
    event_id: event.id,
    acknowledged: true,
    acknowledged_by: "operator-001",
    acknowledged_at: new Date().toISOString(),
  });
}