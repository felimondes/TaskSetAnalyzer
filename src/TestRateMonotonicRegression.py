import unittest
import pandas as pd
from simulator import Simulator
from rate_monotonic import RateMonotonic


class TestRateMonotonic(unittest.TestCase):

    def setUp(self):
        self.sim = Simulator()
        self.scheduler = RateMonotonic()
    
    def test_scheduable(self):
        task_set = pd.DataFrame({
            'task_id': ['A', 'B'],
            'T_i': [4, 5],
            'D_i': [4, 5],
            'C_i': [1, 3],
        })

        results = self.sim.start(task_set, self.scheduler, True)

        expected_response = {
            'A': [('A_0', 1), ('A_4', 1), ('A_8', 1), ('A_12', 1), ('A_16', 1)],
            'B': [('B_0', 4), ('B_5', 3), ('B_10', 4), ('B_15', 4)]
        }

        expected_activation = {
            'A': [('A_0', 0), ('A_4', 4), ('A_8', 8), ('A_12', 12), ('A_16', 16)],
            'B': [('B_0', 0), ('B_5', 5), ('B_10', 10), ('B_15', 15)]
        }

        expected_completion = {
            'A': [('A_0', 1), ('A_4', 5), ('A_8', 9), ('A_12', 13), ('A_16', 17)],
            'B': [('B_0', 4), ('B_5', 8), ('B_10', 14), ('B_15', 19)]
        }

        self.assertEqual(results.job_response_times_by_task, expected_response)
        self.assertEqual(results.job_activation_times_by_task, expected_activation)
        self.assertEqual(results.job_completion_times_by_task, expected_completion)

    def test_unscheduable(self):
        task_set = pd.DataFrame({
            'task_id': ['A', 'B'],
            'T_i': [4, 5],
            'D_i': [4, 5],
            'C_i': [1, 4],
        })

        results = self.sim.start(task_set, self.scheduler, True)

        expected_response = {
            'A': [('A_0', 1), ('A_4', 1), ('A_8', 1), ('A_12', 1), ('A_16', 1)],
            'B': [('B_0', 6), ('B_5', 6), ('B_10', 6), ('B_15', 6)]
        }

        expected_activation = {
            'A': [('A_0', 0), ('A_4', 4), ('A_8', 8), ('A_12', 12), ('A_16', 16)],
            'B': [('B_0', 0), ('B_5', 5), ('B_10', 10), ('B_15', 15)]
        }

        expected_completion = {
            'A': [('A_0', 1), ('A_4', 5), ('A_8', 9), ('A_12', 13), ('A_16', 17)],
            'B': [('B_0', 6), ('B_5', 11), ('B_10', 16), ('B_15', 21)]
        }

        self.assertEqual(results.job_response_times_by_task, expected_response)
        self.assertEqual(results.job_activation_times_by_task, expected_activation)
        self.assertEqual(results.job_completion_times_by_task, expected_completion)


    


if __name__ == "__main__":
    unittest.main()