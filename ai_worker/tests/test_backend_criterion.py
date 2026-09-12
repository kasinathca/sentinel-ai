from __future__ import annotations

import unittest

from sentinel_violence_runtime.backend_criterion import RollingViolenceCriterion


class CriterionTests(unittest.TestCase):
    def test_requires_complete_five_window_history(self):
        c = RollingViolenceCriterion()
        for score in [0.99, 0.99, 0.99, 0.1]:
            state = c.observe(camera_id="cam-a", score=score)
            self.assertFalse(state.qualified)
            self.assertFalse(state.complete_history)

        state = c.observe(camera_id="cam-a", score=0.1)
        self.assertTrue(state.complete_history)
        self.assertTrue(state.qualified)
        self.assertEqual(state.positive_count, 3)

    def test_threshold_is_inclusive(self):
        c = RollingViolenceCriterion()
        states = [
            c.observe(camera_id="cam-a", score=s)
            for s in [0.906, 0.0, 0.906, 0.0, 0.906]
        ]
        self.assertTrue(states[-1].qualified)

    def test_two_of_five_does_not_qualify(self):
        c = RollingViolenceCriterion()
        states = [
            c.observe(camera_id="cam-a", score=s)
            for s in [0.99, 0.1, 0.99, 0.1, 0.1]
        ]
        self.assertFalse(states[-1].qualified)

    def test_camera_histories_are_independent(self):
        c = RollingViolenceCriterion()
        for s in [0.99, 0.99, 0.99, 0.1]:
            c.observe(camera_id="cam-a", score=s)

        b = c.observe(camera_id="cam-b", score=0.99)
        self.assertEqual(b.history_count, 1)

        a = c.observe(camera_id="cam-a", score=0.1)
        self.assertTrue(a.qualified)

    def test_reset_removes_history(self):
        c = RollingViolenceCriterion()
        for s in [0.99] * 5:
            state = c.observe(camera_id="cam-a", score=s)
        self.assertTrue(state.qualified)

        c.reset("cam-a")
        state = c.observe(camera_id="cam-a", score=0.1)
        self.assertEqual(state.history_count, 1)
        self.assertFalse(state.qualified)


if __name__ == "__main__":
    unittest.main()
