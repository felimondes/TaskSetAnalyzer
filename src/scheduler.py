from abc import ABC, abstractmethod
import math
from job import Job


class PeriodicTaskSetScheduler(ABC):
    """
    Base class for periodic task set scheduling algorithms.
    Handles common job creation, activation, and execution logic.
    Subclasses define priority rules via select_next_job_from_active().
    """
    
    def __init__(self):
        self.tasks = None
        self.jobs_by_arrival = {}
        self.completed_jobs = []
        self.active_jobs = []
    
    def set_tasks(self, tasks):
        """Initialize task set and create jobs"""
        self.tasks = tasks
        self.create_all_jobs()
    
    def get_running_time(self):
        """Calculate hyperperiod of the task set"""
        periods = [int(p) for p in self.tasks['T_i'].tolist()]
        hyperperiod = math.lcm(*periods)
        return int(hyperperiod)
    
    def create_all_jobs(self):
        """Create all job instances for each task within the hyperperiod"""
        self.jobs_by_arrival = {}
        hyperperiod = self.get_running_time()
        
        for index, task_type in self.tasks.iterrows():
            num_jobs = hyperperiod // task_type['T_i']
            self._create_jobs_for_task(task_type, num_jobs)
    
    def _create_jobs_for_task(self, task_type, num_jobs):
        """Create individual job instances for a task type"""
        for k in range(num_jobs):
            arrival_time = int(k * int(task_type['T_i']))
            job = Job(task_type, arrival_time, deadline_offset=arrival_time)
            
            if arrival_time not in self.jobs_by_arrival:
                self.jobs_by_arrival[arrival_time] = []
            self.jobs_by_arrival[arrival_time].append(job)
    
    def activate_newly_arrived_jobs(self, current_time):
        """Activate jobs that arrived at the current time"""
        if current_time in self.jobs_by_arrival:
            self.active_jobs.extend(self.jobs_by_arrival[current_time])
    
    def remove_completed_from_active(self):
        """Remove finished jobs from the active job queue"""
        self.active_jobs = [job for job in self.active_jobs if not job.is_completed()]
    
    @abstractmethod
    def select_next_job_from_active(self):
        """
        Choose which job to execute next based on scheduling priority.
        Must return a Job or None if no jobs are active.
        """
        pass
    
    def get_next_job(self, current_time):
        """Get the next job to execute based on scheduling policy"""
        self.activate_newly_arrived_jobs(current_time)
        self.remove_completed_from_active()
        
        if not self.active_jobs:
            return None
        
        return self.select_next_job_from_active()
    
    def mark_job_started(self, job, current_time):
        """Mark when a job first starts execution"""
        if job.start_time is None:
            job.start_time = current_time
    
    def execute_job(self, job, time_units):
        """Execute a job for the given number of time units"""
        job.execute(time_units)
    
    def complete_job(self, job, current_time):
        """Mark a job as completed and record completion time"""
        job.completion_time = current_time
        self.completed_jobs.append(job)
    
    @abstractmethod
    def is_schedulable(self):
        """Check if the task set is schedulable under this algorithm"""
        pass
    
    def results(self):
        """Return scheduling results"""
        return {
            'completed_jobs': self.completed_jobs,
            'schedulable': self.is_schedulable()
        }
        

