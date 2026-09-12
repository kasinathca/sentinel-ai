from __future__ import annotations
import unittest
from sqlalchemy import inspect
from app.db.base import Base
from app.db import models
from app.db.session import build_engine
EXPECTED={"cameras","models","model_versions","violence_event_policies","events","violence_event_context"}
class Phase2MSchemaTests(unittest.TestCase):
    def test_expected_metadata_tables(self): self.assertEqual(set(Base.metadata.tables),EXPECTED)
    def test_create_all_tables(self):
        engine=build_engine("sqlite+pysqlite:///:memory:")
        try: Base.metadata.create_all(engine); actual=set(inspect(engine).get_table_names())
        finally: engine.dispose()
        self.assertEqual(actual,EXPECTED)
