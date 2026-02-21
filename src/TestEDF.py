import unittest
import pandas as pd
from simulator import Simulator
from earliest_deadline_first import EDF


class TestEDF(unittest.TestCase):

    def setUp(self):
        self.sim = Simulator()
        self.scheduler = EDF()

    def test_edf_example_1(self):
        task_set = pd.DataFrame({
            'task_id': ['A', 'B'],
            'T_i': [4, 5],
            'D_i': [4, 5],
            'C_i': [1, 3],
        })

        results = self.sim.start(task_set, self.scheduler, True)

        expected_response = {
            'A': [('A_0', 1), ('A_4', 1), ('A_8', 1), ('A_12', 2), ('A_16', 3)],
            'B': [('B_0', 4), ('B_5', 3), ('B_10', 3), ('B_15', 3)]
        }

        expected_activation = {
            'A': [('A_0', 0), ('A_4', 4), ('A_8', 8), ('A_12', 12), ('A_16', 16)],
            'B': [('B_0', 0), ('B_5', 5), ('B_10', 10), ('B_15', 15)]
        }

        expected_completion = {
            'A': [('A_0', 1), ('A_4', 5), ('A_8', 9), ('A_12', 14), ('A_16', 19)],
            'B': [('B_0', 4), ('B_5', 8), ('B_10', 13), ('B_15', 18)]
        }

        self.assertEqual(results["job_response_times_by_task"], expected_response)
        self.assertEqual(results["activation_times_by_task"], expected_activation)
        self.assertEqual(results["completion_times_by_task"], expected_completion)
        self.assertTrue(results["schedulable_simulator"][0])
        self.assertEqual(results["hyperperiod"], 20)


    def test_edf_example_2(self):
        task_set = pd.DataFrame({
            'task_id': ['A', 'B'],
            'T_i': [4, 5],
            'D_i': [4, 5],
            'C_i': [1, 4],
        })

        results = self.sim.start(task_set, self.scheduler, True)

        expected_response = {
            'A': [('A_0', 1), ('A_4', 2), ('A_8', 3), ('A_12', 4), ('A_16', 1)],
            'B': [('B_0', 5), ('B_5', 5), ('B_10', 5), ('B_15', 6)]
        }

        expected_activation = {
            'A': [('A_0', 0), ('A_4', 4), ('A_8', 8), ('A_12', 12), ('A_16', 16)],
            'B': [('B_0', 0), ('B_5', 5), ('B_10', 10), ('B_15', 15)]
        }

        expected_completion = {
            'A': [('A_0', 1), ('A_4', 6), ('A_8', 11), ('A_12', 16), ('A_16', 17)],
            'B': [('B_0', 5), ('B_5', 10), ('B_10', 15), ('B_15', 21)]
        }

        self.assertEqual(results["job_response_times_by_task"], expected_response)
        self.assertEqual(results["activation_times_by_task"], expected_activation)
        self.assertEqual(results["completion_times_by_task"], expected_completion)
        self.assertFalse(results["schedulable_simulator"][0])
        self.assertEqual(results["hyperperiod"], 20)


if __name__ == "__main__":
    unittest.main()