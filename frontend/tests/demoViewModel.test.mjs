import test from "node:test";
import assert from "node:assert/strict";

import {
  describeRollingCondition,
  describeSessionDetection,
  describeThresholdPolicy,
  formatThreshold,
  isClipSelectable,
} from "../src/services/demoViewModel.js";

test("incomplete history remains distinct from a positive latest observation", () => {
  const ai = { complete_history: false, latest_score_positive: true, candidate_condition: false };
  assert.equal(describeRollingCondition(ai), "Insufficient history");
  assert.equal(describeSessionDetection(ai), "No");
});

test("session detection stays visible after current rolling qualification ends", () => {
  const ai = { complete_history: true, candidate_condition: false, session_violence_detected: true };
  assert.equal(describeRollingCondition(ai), "Not currently qualifying");
  assert.equal(describeSessionDetection(ai), "YES");
});

test("only validated ready media can be selected", () => {
  assert.equal(isClipSelectable({ state: "ready" }), true);
  assert.equal(isClipSelectable({ state: "transcoding" }), false);
  assert.equal(isClipSelectable({ state: "rejected" }), false);
});

test("threshold policy label follows backend mode", () => {
  assert.equal(describeThresholdPolicy({ policy_mode: "experimental" }), "Experimental event threshold");
  assert.equal(describeThresholdPolicy({ policy_mode: "qualified" }), "Frozen event threshold");
  assert.equal(formatThreshold({ policy_mode: "experimental", threshold: 0.8 }), "0.80");
  assert.equal(formatThreshold({ policy_mode: "qualified", threshold: 0.906 }), "0.906");
});
