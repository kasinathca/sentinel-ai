from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Camera


def create_camera(
    session: Session,
    name: str,
    source_kind: str,
    description: str | None = None,
    enabled: bool = True,
) -> Camera:
    camera = Camera(
        name=name,
        source_kind=source_kind,
        description=description,
        enabled=enabled,
    )

    session.add(camera)
    session.flush()

    return camera


def get_camera(
    session: Session,
    camera_id: UUID,
) -> Camera | None:
    return session.get(Camera, camera_id)


def list_cameras(
    session: Session,
    enabled: bool | None = None,
) -> list[Camera]:
    statement = select(Camera).order_by(Camera.created_at, Camera.id)

    if enabled is not None:
        statement = statement.where(Camera.enabled == enabled)

    return list(session.scalars(statement).all())


def update_camera(
    session: Session,
    camera_id: UUID,
    *,
    name: str | None = None,
    source_kind: str | None = None,
    description: str | None = None,
    enabled: bool | None = None,
) -> Camera | None:
    camera = session.get(Camera, camera_id)

    if camera is None:
        return None

    if name is not None:
        camera.name = name

    if source_kind is not None:
        camera.source_kind = source_kind

    if description is not None:
        camera.description = description

    if enabled is not None:
        camera.enabled = enabled

    session.flush()

    return camera
