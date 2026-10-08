from __future__ import annotations

import unittest
from uuid import UUID, uuid4

from sqlalchemy import select

from app.cameras.constants import (
    DEMO_CAMERA_DESCRIPTION,
    DEMO_CAMERA_ID,
    DEMO_CAMERA_NAME,
    DEMO_CAMERA_SOURCE_KIND,
)
from app.db.base import Base
from app.db.models import Camera
from app.db.seed import seed_demo_camera
from app.db.session import build_engine, build_session_factory


class DemoCameraSeedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.sessions = build_session_factory(self.engine)

    def tearDown(self) -> None:
        self.engine.dispose()

    def cameras(self) -> list[Camera]:
        with self.sessions() as session:
            return list(session.scalars(select(Camera).order_by(Camera.id)))

    def test_clean_database_gets_canonical_demo_camera(self) -> None:
        seed_demo_camera(self.sessions)

        camera, = self.cameras()
        self.assertEqual(camera.id, DEMO_CAMERA_ID)
        self.assertEqual(camera.name, DEMO_CAMERA_NAME)
        self.assertEqual(camera.source_kind, DEMO_CAMERA_SOURCE_KIND)
        self.assertEqual(camera.description, DEMO_CAMERA_DESCRIPTION)
        self.assertTrue(camera.enabled)

    def test_repeated_seed_is_idempotent_and_preserves_operational_state(self) -> None:
        seed_demo_camera(self.sessions)
        with self.sessions.begin() as session:
            camera = session.get(Camera, DEMO_CAMERA_ID)
            camera.enabled = False
        seed_demo_camera(self.sessions)

        camera, = self.cameras()
        self.assertEqual(camera.id, DEMO_CAMERA_ID)
        self.assertFalse(camera.enabled)

    def test_noncanonical_uuid_with_demo_name_fails_without_duplicate(self) -> None:
        conflicting_id = uuid4()
        with self.sessions.begin() as session:
            session.add(
                Camera(
                    id=conflicting_id,
                    name=DEMO_CAMERA_NAME,
                    source_kind=DEMO_CAMERA_SOURCE_KIND,
                    enabled=True,
                )
            )

        with self.assertRaisesRegex(RuntimeError, "non-canonical UUID"):
            seed_demo_camera(self.sessions)

        self.assertEqual([camera.id for camera in self.cameras()], [conflicting_id])

    def test_canonical_uuid_with_wrong_name_fails(self) -> None:
        with self.sessions.begin() as session:
            session.add(
                Camera(
                    id=DEMO_CAMERA_ID,
                    name="Another Camera",
                    source_kind=DEMO_CAMERA_SOURCE_KIND,
                    enabled=True,
                )
            )

        with self.assertRaisesRegex(RuntimeError, "different camera name"):
            seed_demo_camera(self.sessions)

    def test_canonical_uuid_with_wrong_source_kind_fails(self) -> None:
        with self.sessions.begin() as session:
            session.add(
                Camera(
                    id=DEMO_CAMERA_ID,
                    name=DEMO_CAMERA_NAME,
                    source_kind="rtsp",
                    enabled=True,
                )
            )

        with self.assertRaisesRegex(RuntimeError, "non-canonical source_kind"):
            seed_demo_camera(self.sessions)

    def test_unrelated_camera_is_preserved(self) -> None:
        unrelated_id = UUID("33333333-3333-4333-8333-333333333333")
        with self.sessions.begin() as session:
            session.add(
                Camera(
                    id=unrelated_id,
                    name="Existing Camera",
                    source_kind="file",
                    enabled=False,
                )
            )

        seed_demo_camera(self.sessions)

        cameras = {camera.id: camera for camera in self.cameras()}
        self.assertEqual(set(cameras), {DEMO_CAMERA_ID, unrelated_id})
        self.assertEqual(cameras[unrelated_id].name, "Existing Camera")
        self.assertFalse(cameras[unrelated_id].enabled)


if __name__ == "__main__":
    unittest.main()
