import copy,unittest
from datetime import datetime,timedelta,timezone
from app.ai_integration.errors import WorkerContractValidationError,WorkerReportedFailure,OutOfOrderWorkerObservation
from app.ai_integration.service import ViolenceWorkerResultService
from app.events.violence_conditions import RecordingViolenceConditionConsumer
BASE={'schema_version': '1', 'job_id': '11111111-1111-4111-8111-111111111111', 'correlation_id': '22222222-2222-4222-8222-222222222222', 'camera_id': '33333333-3333-4333-8333-333333333333', 'window': {'started_at': '2026-09-12T07:00:00.000Z', 'ended_at': '2026-09-12T07:00:02.667Z'}, 'status': 'success', 'model': {'model_version_id': '6d22f83d-17f8-5ecf-9f0f-246fa326ec72', 'task': 'violence_fighting'}, 'result': {'label': 'fighting', 'score': 0.94, 'score_semantics': 'uncalibrated sigmoid score for the fighting positive class from EXP-VIO-TEMPORAL-001; higher means more fighting-like'}}
def payload(score,i,camera="33333333-3333-4333-8333-333333333333"):
    p=copy.deepcopy(BASE); p['camera_id']=camera; s=datetime(2026,9,12,7,0,tzinfo=timezone.utc)+timedelta(seconds=i); e=s+timedelta(seconds=1)
    p['window']['started_at']=s.isoformat().replace('+00:00','Z'); p['window']['ended_at']=e.isoformat().replace('+00:00','Z'); p['result']['score']=score; p['job_id']=f"11111111-1111-4111-8111-{i:012d}"; return p
class IntegrationTests(unittest.TestCase):
    def svc(self): c=RecordingViolenceConditionConsumer(); return ViolenceWorkerResultService(condition_consumer=c),c
    def test_valid(self): s,c=self.svc(); r=s.consume_payload(copy.deepcopy(BASE)); self.assertEqual(r.score,.94); self.assertEqual(len(c.evaluations),1)
    def test_extra_rejected(self): s,_=self.svc(); p=copy.deepcopy(BASE); p['x']=1; self.assertRaises(WorkerContractValidationError,s.consume_payload,p)
    def test_failure_does_not_update(self):
        s,c=self.svc(); p={'schema_version':'1','job_id':BASE['job_id'],'correlation_id':BASE['correlation_id'],'camera_id':BASE['camera_id'],'status':'failed','error':{'code':'INFERENCE_FAILED','message':'Inference failed.'}}
        self.assertRaises(WorkerReportedFailure,s.consume_payload,p); self.assertEqual(c.evaluations,[])
    def test_three_of_five(self):
        s,_=self.svc(); states=[s.consume_payload(payload(x,i)) for i,x in enumerate([.896,.982,.987,.610,.996])]; self.assertTrue(states[4].candidate_condition); self.assertEqual(states[4].positive_count,3)
    def test_normal_never(self):
        s,_=self.svc(); states=[s.consume_payload(payload(x,i)) for i,x in enumerate([.01,.02,.005,.1,.03,.02])]; self.assertFalse(any(x.candidate_condition for x in states))
    def test_camera_isolation(self):
        s,_=self.svc(); A=BASE['camera_id']; B='44444444-4444-4444-8444-444444444444'
        for i,x in enumerate([.99,.99,.99,0]): s.consume_payload(payload(x,i,A))
        self.assertEqual(s.consume_payload(payload(.99,0,B)).history_count,1); self.assertTrue(s.consume_payload(payload(0,4,A)).candidate_condition)
    def test_out_of_order(self):
        s,_=self.svc(); s.consume_payload(payload(.1,10)); self.assertRaises(OutOfOrderWorkerObservation,s.consume_payload,payload(.1,5))
