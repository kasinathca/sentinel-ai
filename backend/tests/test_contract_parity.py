import importlib.util,unittest
from pathlib import Path
from app.ai_integration import constants as b
class ParityTests(unittest.TestCase):
 def test_worker_constants_match(self):
  root=Path(__file__).resolve().parents[2]; p=root/'ai_worker'/'sentinel_violence_runtime'/'constants.py'
  if not p.exists(): self.skipTest('ai_worker source not beside backend')
  spec=importlib.util.spec_from_file_location('wc',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
  self.assertEqual(b.MODEL_VERSION_ID,m.MODEL_VERSION_ID); self.assertEqual(b.LIVE_THRESHOLD,m.LIVE_SCORE_THRESHOLD); self.assertEqual(b.LIVE_N_REQUIRED,m.LIVE_N_REQUIRED); self.assertEqual(b.LIVE_M_HISTORY,m.LIVE_M_HISTORY); self.assertEqual(b.SCORE_SEMANTICS,m.SCORE_SEMANTICS)
