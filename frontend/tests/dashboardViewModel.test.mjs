import test from "node:test";
import assert from "node:assert/strict";
import {
  currentSessionAttentionEvents,
  historicalAttentionEvents,
} from "../src/services/dashboardViewModel.js";

const events = [
  { id: "old", correlation_id: "old-session", requires_attention: true },
  { id: "live", correlation_id: "active-session", requires_attention: true },
  { id: "normal", correlation_id: "active-session", requires_attention: false },
];

test("dashboard presents only the active source session as live", () => {
  const status = { session_id: "active-session" };
  assert.deepEqual(currentSessionAttentionEvents(events, status).map(({ id }) => id), ["live"]);
  assert.deepEqual(historicalAttentionEvents(events, status).map(({ id }) => id), ["old"]);
});

test("dashboard presents no historical record as live before source start", () => {
  assert.deepEqual(currentSessionAttentionEvents(events, { session_id: null }), []);
  assert.deepEqual(historicalAttentionEvents(events, { session_id: null }).map(({ id }) => id), ["old", "live"]);
});
