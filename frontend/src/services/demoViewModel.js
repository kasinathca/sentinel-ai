export function describeRollingCondition(ai = {}) {
  if (!ai.complete_history) return "Insufficient history";
  return ai.candidate_condition ? "Currently qualifying" : "Not currently qualifying";
}

export function describeSessionDetection(ai = {}) {
  return ai.session_violence_detected ? "YES" : "No";
}

export function describeThresholdPolicy(ai = {}) {
  return ai.policy_mode === "experimental"
    ? "Experimental event threshold"
    : "Frozen event threshold";
}

export function formatThreshold(ai = {}) {
  if (typeof ai.threshold !== "number") return "Not available";
  return ai.policy_mode === "experimental"
    ? ai.threshold.toFixed(2)
    : String(ai.threshold);
}

export function isClipSelectable(clip) {
  return clip?.state === "ready";
}
