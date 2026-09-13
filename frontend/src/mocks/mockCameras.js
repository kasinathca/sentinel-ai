export const mockCameras = [
  {
    id: "cam-001",
    name: "Main Entrance",
    description: "Primary entrance camera",
    source_kind: "camera",
    enabled: true,
    health: {
      state: "healthy",
      last_frame_at: "2026-09-14T00:42:15Z",
      last_health_check_at: "2026-09-14T00:42:20Z",
    },
  },
  {
    id: "cam-002",
    name: "Restricted Area",
    description: "Restricted access monitoring",
    source_kind: "camera",
    enabled: true,
    health: {
      state: "healthy",
      last_frame_at: "2026-09-14T00:41:58Z",
      last_health_check_at: "2026-09-14T00:42:20Z",
    },
  },
  {
    id: "cam-003",
    name: "Waiting Area",
    description: "Waiting area monitoring",
    source_kind: "camera",
    enabled: true,
    health: {
      state: "degraded",
      last_frame_at: "2026-09-14T00:39:12Z",
      last_health_check_at: "2026-09-14T00:42:20Z",
    },
  },
  {
    id: "cam-004",
    name: "Parking Area",
    description: "Parking area monitoring",
    source_kind: "camera",
    enabled: true,
    health: {
      state: "offline",
      last_frame_at: "2026-09-14T00:01:42Z",
      last_health_check_at: "2026-09-14T00:42:20Z",
    },
  },
];