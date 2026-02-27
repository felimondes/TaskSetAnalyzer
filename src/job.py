import pandas as pd
from typing import Optional


class Job:
    """Represents a single job (release) of a periodic task.

    Attributes are intentionally simple and typed so the simulator can
    inspect and aggregate stats.
    """

    def __init__(self, tasktype: pd.Series, activation: int, wcet: bool) -> None:
        self.job_id: str = f"{tasktype['task_id']}_{activation}"
        self.task_id: str = tasktype['task_id']

        # Task parameters
        self.T: int = int(tasktype['T_i'])
        relative_deadline = int(tasktype['D_i'])
        execution_time = self._calculate_execution_time(tasktype, wcet) 

        # Dynamic state
        self.remaining_time_till_done: int = execution_time
        self.d: int = activation + relative_deadline  # absolute deadline
        self.a: int = activation                      # activation time
        self.s: Optional[int] = None                  # start time
        self.f: Optional[int] = None                  # finish time

        # Derived metrics (filled by simulator)
        self.lateness: Optional[int] = None
        self.response_time: Optional[int] = None
        self.isExecuting: bool = False

    def _calculate_execution_time(self, tasktype: pd.Series, wcet: bool):
        if wcet:
            return tasktype["C_i"]
        elif "C_i_min" in tasktype:
            from random import randrange
            return randrange(tasktype["C_i_min"], tasktype['C_i']+1)
        else:
            raise ValueError("calculation of execution_time not working")

    def is_complete(self) -> bool:
        if self.remaining_time_till_done < 0:
            raise ValueError(
                f"Job {self.task_id} over-executed by {-self.remaining_time_till_done} time units"
            )
        return self.remaining_time_till_done == 0

    def execute(self, time_units: int) -> None:
        """Consume `time_units` from the job's remaining execution budget."""
        self.remaining_time_till_done -= int(time_units)

    def set_started(self, start_time: int) -> None:
        """Record the first time the job began execution."""
        if self.s is None:
            self.s = int(start_time)

    def is_late(self) -> bool:
        """Return True if the job finished after its deadline."""
        if self.f is None:
            return False
        return self.f > self.d