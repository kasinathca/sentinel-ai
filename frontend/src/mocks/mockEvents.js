import { EVENT_TYPES } from "../types/event";

export const mockEvents = [
  {
    id: "evt-001",
    event_type: EVENT_TYPES.VIOLENCE,
    camera: {
      id: "cam-001",
      name: "Main Entrance",
    },
    occurred_at: "2026-09-14T00:42:15Z",
    created_at: "2026-09-14T00:42:18Z",
    requires_attention: true,
    severity: "high",
    status: "open",
    acknowledgement: {
      acknowledged: false,
      acknowledged_by: null,
      first_acknowledged_at: null,
    },
    evidence: {
      available_count: 1,
      pending_count: 0,
      failed_count: 0,
    },
    context: {
      model_version: {
        id: "EXP-VIO-TEMPORAL-001",
        name: "MODEL-VIO-BIGRU-ATTN-XD-V1",
        version: "V1",
      },
      output_label: "violence",
      score: 0.94,
      event_threshold: 0.906,
      score_semantics: "model_score",
      window_started_at: "2026-09-14T00:42:10Z",
      window_ended_at: "2026-09-14T00:42:15Z",
    },
  },

  {
    id: "evt-002",
    event_type: EVENT_TYPES.INTRUSION,
    camera: {
      id: "cam-002",
      name: "Restricted Area",
    },
    occurred_at: "2026-09-14T00:35:02Z",
    created_at: "2026-09-14T00:35:03Z",
    requires_attention: true,
    severity: "medium",
    status: "acknowledged",
    acknowledgement: {
      acknowledged: true,
      acknowledged_by: "operator-001",
      first_acknowledged_at: "2026-09-14T00:36:10Z",
    },
    evidence: {
      available_count: 1,
      pending_count: 0,
      failed_count: 0,
    },
    context: {
      rule_id: "rule-001",
      zone_id: "zone-001",
      geometry_version: 1,
      track_id: "track-42",
      trigger_position: {
        x: 0.63,
        y: 0.41,
      },
      position_method: "normalized",
      cooldown: false,
    },
  },

  {
    id: "evt-003",
    event_type: EVENT_TYPES.CROWD,
    camera: {
      id: "cam-003",
      name: "Waiting Area",
    },
    occurred_at: "2026-09-14T00:21:44Z",
    created_at: "2026-09-14T00:21:45Z",
    requires_attention: true,
    severity: "medium",
    status: "open",
    acknowledgement: {
      acknowledged: false,
      acknowledged_by: null,
      first_acknowledged_at: null,
    },
    evidence: {
      available_count: 0,
      pending_count: 1,
      failed_count: 0,
    },
    context: {
      rule_id: "rule-003",
      zone_id: "zone-003",
      geometry_version: 1,
      observed_count: 18,
      threshold_count: 15,
      counting_method: "person_detection",
    },
  },

  {
    id: "evt-004",
    event_type: EVENT_TYPES.LOITERING,
    camera: {
      id: "cam-001",
      name: "Main Entrance",
    },
    occurred_at: "2026-09-14T00:10:31Z",
    created_at: "2026-09-14T00:10:33Z",
    requires_attention: false,
    severity: "low",
    status: "resolved",
    acknowledgement: {
      acknowledged: true,
      acknowledged_by: "operator-001",
      first_acknowledged_at: "2026-09-14T00:12:00Z",
    },
    evidence: {
      available_count: 1,
      pending_count: 0,
      failed_count: 0,
    },
    context: {
      rule_id: "rule-002",
      zone_id: "zone-002",
      geometry_version: 1,
      track_id: "track-18",
      observed_dwell_ms: 125000,
      threshold_ms: 120000,
      track_loss_grace_ms: 5000,
      retrigger_after_ms: 60000,
    },
  },

  {
    id: "evt-005",
    event_type: EVENT_TYPES.CAMERA_OFFLINE,
    camera: {
      id: "cam-004",
      name: "Parking Area",
    },
    occurred_at: "2026-09-14T00:03:12Z",
    created_at: "2026-09-14T00:03:13Z",
    requires_attention: true,
    severity: "high",
    status: "open",
    acknowledgement: {
      acknowledged: false,
      acknowledged_by: null,
      first_acknowledged_at: null,
    },
    evidence: {
      available_count: 0,
      pending_count: 0,
      failed_count: 0,
    },
    context: {
      last_frame_at: "2026-09-14T00:01:42Z",
      offline_after_ms: 90000,
      reason: "frame_timeout",
      health_state_before: "healthy",
      health_state_after: "offline",
    },
  },
];