import unittest
from fastapi.testclient import TestClient
from app.main import create_app
class HealthTests(unittest.TestCase):
 def test_health(self):
  r=TestClient(create_app()).get('/api/v1/health'); self.assertEqual(r.status_code,200); self.assertEqual(r.json()['data']['service'],'sentinel-api')
