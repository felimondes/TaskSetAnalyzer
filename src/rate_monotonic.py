from scheduler import PeriodicTaskSetScheduler
import pandas as pd
from simulator import Simulator


class RateMonotonic(PeriodicTaskSetScheduler):
    """Rate Monotonic priority scheduler: shorter period == higher priority."""

    def select_next_job_from_active(self, active_jobs: list):
        if not active_jobs:
            return None
        return min(active_jobs, key=lambda job: job.T)

    def is_scheduable(self, tasks: pd.DataFrame) -> bool:
        #The below is the Liu & Layland bound for RM schedulability
        #TODO implement hyperbolic bound instead
        utilization = sum(tasks['C_i'] / tasks['T_i'])
        n = len(tasks)
        rm_bound = n * (2 ** (1 / n) - 1)
        return utilization <= rm_bound
    
    
    def get_least_upper_bound(self, n: int) -> float:
        return n * (2 ** (1 / n) - 1)


if __name__ == "__main__":
    sim = Simulator()
    rate_monotonic_scheduler = RateMonotonic()

    # Example 1: schedulable
    task_set = pd.DataFrame({
        'task_id': ['A', 'B'],
        'T_i': [4, 5],
        'D_i': [4, 5],
        'C_i': [1, 3],
    })

    print(task_set)
    results = sim.start(task_set, rate_monotonic_scheduler)
    print("Job response times by task:", results.get("job_response_times_by_task"))
    print("Activation times by task:", results.get("activation_times_by_task"))
    print("Completion times by task:", results.get("completion_times_by_task"))
    print("Schedulable (analysis):", results.get("schedulable_analysis"))
    print("Schedulable (simulator):", results.get("schedulable_simulator"))


    print("\n\n\n")

    # Example 2: not schedulable
    task_set = pd.DataFrame({
        'task_id': ['A', 'B'],
        'T_i': [4, 5],
        'D_i': [4, 5],
        'C_i': [1, 4],
    })

    print(task_set)
    results = sim.start(task_set, rate_monotonic_scheduler)
    print("Job response times by task:", results.get("job_response_times_by_task"))
    print("Activation times by task:", results.get("activation_times_by_task"))
    print("Completion times by task:", results.get("completion_times_by_task"))
    print("Schedulable (analysis):", results.get("schedulable_analysis"))
    print("Schedulable (simulator):", results.get("schedulable_simulator"))
    print("Hyperperiod:", results.get("hyperperiod"))