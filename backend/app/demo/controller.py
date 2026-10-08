"""Process-local control boundary for the single virtual CCTV source.

The actual paced decoder/replay adapter is owned by the media/AI integration
work. This module owns safe clip selection and lifecycle state, and accepts an
adapter through a narrow interface when that implementation is available.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import threading
from typing import Callable, Protocol
from uuid import UUID, uuid4

from app.demo.clip_catalog import (
    DemoCatalogError,
    DemoClip,
    DemoClipCatalog,
    DemoClipNotFound,
)


class DemoSourceState(str, Enum):
    IDLE = "idle"
    READY = "ready"
    STARTING = "starting"
    PLAYING = "playing"
    LOOP_RESTARTING = "loop-restarting"
    STOPPED = "stopped"
    FAILED = "failed"


class DemoControllerError(RuntimeError):
    """Safe application error for an invalid or unavailable source action."""

    def __init__(self, code: str, message: str, http_status: int) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.http_status = http_status


class PlaybackCallbacks(Protocol):
    """Events a replay adapter reports without exposing its media internals."""

    def first_frame(self, position_ms: int = 0) -> None: ...

    def position_changed(self, position_ms: int) -> None: ...

    def loop_restart_started(self) -> None: ...

    def loop_restart_completed(self) -> None: ...

    def failed(self) -> None: ...


class ReplayAdapter(Protocol):
    """Non-blocking control interface for the independently owned replay source."""

    def start(self, clip: DemoClip, callbacks: PlaybackCallbacks) -> None: ...

    def stop(self) -> None: ...

    def restart(self, callbacks: PlaybackCallbacks) -> None: ...


@dataclass(frozen=True)
class DemoSourceSnapshot:
    state: DemoSourceState
    clip_id: str | None
    position_ms: int | None
    loop_count: int
    session_id: UUID | None

    def to_public_dict(self) -> dict[str, object]:
        return {
            "state": self.state.value,
            "clip_id": self.clip_id,
            "position_ms": self.position_ms,
            "loop_count": self.loop_count,
            "session_id": str(self.session_id) if self.session_id else None,
        }


class _SessionCallbacks:
    def __init__(self, controller: "VirtualCameraController", generation: int) -> None:
        self._controller = controller
        self._generation = generation

    def first_frame(self, position_ms: int = 0) -> None:
        self._controller._first_frame(self._generation, position_ms)

    def position_changed(self, position_ms: int) -> None:
        self._controller._position_changed(self._generation, position_ms)

    def loop_restart_started(self) -> None:
        self._controller._loop_restart_started(self._generation)

    def loop_restart_completed(self) -> None:
        self._controller._loop_restart_completed(self._generation)

    def failed(self) -> None:
        self._controller._failed(self._generation)


class VirtualCameraController:
    """Own exactly one process-local virtual-camera selection and session."""

    _ACTIVE_STATES = {
        DemoSourceState.STARTING,
        DemoSourceState.PLAYING,
        DemoSourceState.LOOP_RESTARTING,
    }

    def __init__(
        self,
        catalog_factory: Callable[[], DemoClipCatalog],
        replay_adapter: ReplayAdapter | None = None,
    ) -> None:
        self._catalog_factory = catalog_factory
        self._replay_adapter = replay_adapter
        self._state = DemoSourceState.IDLE
        self._clip: DemoClip | None = None
        self._position_ms: int | None = None
        self._loop_count = 0
        self._session_id: UUID | None = None
        self._last_frame_at: datetime | None = None
        self._generation = 0
        self._state_lock = threading.RLock()
        self._operation_lock = threading.Lock()

    def list_clips(self) -> list[DemoClip]:
        return self._catalog_factory().list_clips()

    def select_source(self, clip_id: str) -> DemoSourceSnapshot:
        with self._operation_lock:
            with self._state_lock:
                if self._state in self._ACTIVE_STATES:
                    raise DemoControllerError(
                        "DEMO_SOURCE_STATE_CONFLICT",
                        "Stop the current source before selecting another clip.",
                        409,
                    )
            clip = self._catalog_factory().get_clip(clip_id)
            with self._state_lock:
                self._generation += 1
                self._clip = clip
                self._position_ms = 0
                self._loop_count = 0
                self._session_id = None
                self._state = DemoSourceState.READY
                return self.snapshot()

    def start(self) -> DemoSourceSnapshot:
        with self._operation_lock:
            with self._state_lock:
                if self._clip is None:
                    raise DemoControllerError(
                        "DEMO_SOURCE_STATE_CONFLICT",
                        "Select an approved clip before starting the source.",
                        409,
                    )
                if self._state in self._ACTIVE_STATES:
                    raise DemoControllerError(
                        "DEMO_SOURCE_STATE_CONFLICT",
                        "The virtual camera source is already active.",
                        409,
                    )
                clip_id = self._clip.clip_id

            try:
                clip = self._catalog_factory().get_clip(clip_id)
            except DemoClipNotFound as exc:
                with self._state_lock:
                    self._state = DemoSourceState.FAILED
                    self._position_ms = None
                raise DemoControllerError(
                    "DEMO_CLIP_NOT_FOUND", "The selected demo clip is unavailable.", 404
                ) from exc
            except DemoCatalogError as exc:
                with self._state_lock:
                    self._state = DemoSourceState.FAILED
                    self._position_ms = None
                raise DemoControllerError(
                    "SOURCE_UNAVAILABLE", "The selected demo source is unavailable.", 503
                ) from exc

            if self._replay_adapter is None:
                with self._state_lock:
                    self._state = DemoSourceState.FAILED
                    self._position_ms = None
                raise DemoControllerError(
                    "SOURCE_UNAVAILABLE",
                    "The replay source adapter is not configured.",
                    503,
                )

            with self._state_lock:
                self._generation += 1
                generation = self._generation
                self._clip = clip
                self._state = DemoSourceState.STARTING
                self._position_ms = 0
                self._loop_count = 0
                self._session_id = uuid4()
            try:
                self._replay_adapter.start(clip, _SessionCallbacks(self, generation))
            except Exception as exc:
                self._failed(generation)
                raise DemoControllerError(
                    "SOURCE_UNAVAILABLE", "The replay source could not be started.", 503
                ) from exc
            return self.snapshot()

    def stop(self) -> DemoSourceSnapshot:
        with self._operation_lock:
            with self._state_lock:
                should_stop_adapter = self._state in self._ACTIVE_STATES or (
                    self._state == DemoSourceState.FAILED
                )
                self._generation += 1
                self._state = DemoSourceState.STOPPED
                self._position_ms = None
                self._session_id = None
            if should_stop_adapter and self._replay_adapter is not None:
                try:
                    self._replay_adapter.stop()
                except Exception as exc:
                    with self._state_lock:
                        self._state = DemoSourceState.FAILED
                    raise DemoControllerError(
                        "SOURCE_UNAVAILABLE", "The replay source could not be stopped.", 503
                    ) from exc
            return self.snapshot()

    def restart(self) -> DemoSourceSnapshot:
        with self._operation_lock:
            with self._state_lock:
                if self._clip is None or self._state not in self._ACTIVE_STATES:
                    raise DemoControllerError(
                        "DEMO_SOURCE_STATE_CONFLICT",
                        "Restart requires an active selected source.",
                        409,
                    )
                if self._replay_adapter is None:
                    raise DemoControllerError(
                        "SOURCE_UNAVAILABLE",
                        "The replay source adapter is not configured.",
                        503,
                    )
                self._generation += 1
                generation = self._generation
                self._state = DemoSourceState.STARTING
                self._position_ms = 0
                self._loop_count = 0
                callbacks = _SessionCallbacks(self, generation)
            try:
                self._replay_adapter.restart(callbacks)
            except Exception as exc:
                self._failed(generation)
                raise DemoControllerError(
                    "SOURCE_UNAVAILABLE", "The replay source could not be restarted.", 503
                ) from exc
            return self.snapshot()

    def snapshot(self) -> DemoSourceSnapshot:
        with self._state_lock:
            return DemoSourceSnapshot(
                state=self._state,
                clip_id=self._clip.clip_id if self._clip else None,
                position_ms=self._position_ms,
                loop_count=self._loop_count,
                session_id=self._session_id,
            )

    @property
    def last_frame_at(self) -> datetime | None:
        with self._state_lock:
            return self._last_frame_at

    @property
    def replay_adapter(self) -> ReplayAdapter | None:
        return self._replay_adapter

    def _first_frame(self, generation: int, position_ms: int) -> None:
        with self._state_lock:
            if generation == self._generation and self._state == DemoSourceState.STARTING:
                self._state = DemoSourceState.PLAYING
                self._position_ms = max(position_ms, 0)
                self._last_frame_at = datetime.now(timezone.utc)

    def _position_changed(self, generation: int, position_ms: int) -> None:
        with self._state_lock:
            if generation == self._generation and self._state == DemoSourceState.PLAYING:
                self._position_ms = max(position_ms, 0)
                self._last_frame_at = datetime.now(timezone.utc)

    def _loop_restart_started(self, generation: int) -> None:
        with self._state_lock:
            if generation == self._generation and self._state == DemoSourceState.PLAYING:
                self._state = DemoSourceState.LOOP_RESTARTING

    def _loop_restart_completed(self, generation: int) -> None:
        with self._state_lock:
            if generation == self._generation and self._state == DemoSourceState.LOOP_RESTARTING:
                self._loop_count += 1
                self._position_ms = 0
                self._state = DemoSourceState.PLAYING

    def _failed(self, generation: int) -> None:
        with self._state_lock:
            if generation == self._generation:
                self._state = DemoSourceState.FAILED
                self._position_ms = None
