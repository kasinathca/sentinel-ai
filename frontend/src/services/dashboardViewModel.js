export function currentSessionAttentionEvents(events, demoStatus) {
  const sessionId = demoStatus?.session_id;
  if (!sessionId) return [];
  return events.filter(
    (event) => event.requires_attention && event.correlation_id === sessionId
  );
}

export function historicalAttentionEvents(events, demoStatus) {
  const currentIds = new Set(
    currentSessionAttentionEvents(events, demoStatus).map((event) => event.id)
  );
  return events.filter(
    (event) => event.requires_attention && !currentIds.has(event.id)
  );
}
