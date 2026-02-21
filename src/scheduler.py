from abc import ABC, abstractmethod
from typing import List, Optional

import pandas as pd

from job import Job


class PeriodicTaskSetScheduler(ABC):
    """Abstract class for periodic task-set schedulers.

    """

    @abstractmethod
    def select_next_job_from_active(self, active_jobs: List[Job]) -> Optional[Job]:
        """Return the Job to execute next, or `None` if no job should run."""
        raise NotImplementedError()

    @abstractmethod
    def is_scheduable(self, tasks: pd.DataFrame) -> bool:
        """Return whether the given `tasks` DataFrame is schedulable under this algorithm."""
        raise NotImplementedError()

    @abstractmethod
    def get_least_upper_bound(self, n: int) -> float:
        """Return the analytic least upper bound on utilization for `n` tasks."""
        raise NotImplementedError()

    def get_utilization(self, tasks: pd.DataFrame) -> float:
        """Compute total utilization (sum C_i / T_i) for a task set."""
        return float(sum(tasks['C_i'] / tasks['T_i']))




