export function describeRollingCondition(ai = {}) {
  if (!ai.complete_history) return "Insufficient history";
  return ai.candidate_condition ? "Currently qualifying" : "Not currently qualifying";
}

export function describeSessionDetection(ai = {}) {
  return ai.session_violence_detected ? "YES" : "No";
}

export function isClipSelectable(clip) {
  return clip?.state === "ready";
}
