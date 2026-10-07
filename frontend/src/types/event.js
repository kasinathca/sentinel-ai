// Event data shape based on the current Sentinel AI API specification.
// This file is for frontend development and mock data only.

export const EVENT_TYPES = {
  INTRUSION: "restricted_area_intrusion",
  LOITERING: "loitering",
  CROWD: "crowd_threshold",
  VIOLENCE: "violence_fighting",
  CAMERA_OFFLINE: "camera_offline",
};

export const EVENT_SEVERITIES = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  CRITICAL: "critical",
};

export const EVENT_STATUSES = {
  OPEN: "open",
  ACKNOWLEDGED: "acknowledged",
  RESOLVED: "resolved",
};

export const CAMERA_HEALTH_STATES = {
  UNKNOWN: "unknown",
  HEALTHY: "healthy",
  DEGRADED: "degraded",
  OFFLINE: "offline",
};