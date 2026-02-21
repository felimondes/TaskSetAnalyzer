from abc import ABC, abstractmethod
import math
from job import Job


class PeriodicTaskSetScheduler(ABC):
    """
    Base class for periodic task set scheduling algorithms.
    Handles common job creation, activation, and execution logic.
    Subclasses define priority rules via select_next_job_from_active().
    """
    @abstractmethod
    def select_next_job_from_active(self):
        """
        Choose which job to execute next based on scheduling priority.
        Must return a Job or None if no jobs are active.
        """
        pass

    @abstractmethod
    def is_scheduable(self):
        """Check if the task set is schedulable under this algorithm"""
        pass
    
    @abstractmethod
    def get_least_upper_bound(self, n):
        """Return the least upper bound on utilization for n tasks under this algorithm"""
        pass

    def get_utilization(self, tasks):
        """Calculate total utilization of the task set"""
        return sum(tasks['C_i'] / tasks['T_i'])


    def results(self):
        """Return scheduling results"""
        return {
            'completed_jobs': self.completed_jobs,
            'schedulable': self.is_scheduable()
        }
        

