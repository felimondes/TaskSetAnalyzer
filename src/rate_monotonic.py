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
        hyperbolic_product = self.get_least_upper_bound(tasks)
        return hyperbolic_product <= 2
    
    def get_least_upper_bound(self, tasks: pd.DataFrame) -> float:
        utilizations = tasks['C_i'] / tasks['T_i']
        hyperbolic_product = 1.0
        for u in utilizations:
            hyperbolic_product *= (u + 1)
        return hyperbolic_product
    
    def __str__(self):
        return f"RateMonotonic"
