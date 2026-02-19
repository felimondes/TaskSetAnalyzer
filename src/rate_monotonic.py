from abc import abstractmethod
from scheduler import Scheduler
from job import Job


class RateMonotonic(Scheduler):
    def __init__(self):
        self.tasks = None
        self.jobs_by_arrival = {}  # arrival_time -> list of jobs
        self.completed_jobs = []
        self.active_jobs = []  # Jobs currently in the system
    
    def get_running_time(self):
        import math
        periods = self.tasks['T_i'].tolist()
        hyperperiod = math.lcm(*periods)
        return hyperperiod
    
    def set_tasks(self, tasks):
        self.tasks = tasks
        self.set_jobs()

    def set_jobs(self):
        self.jobs_by_arrival = {}
        for index, row in self.tasks.iterrows():
            for k in range(0, self.get_running_time() // row['T_i']):
                job = Job(row, arrival_time=k * row['T_i'], deadline_offset=k * row['T_i'])
                arrival = job.arrival_time
                if arrival not in self.jobs_by_arrival:
                    self.jobs_by_arrival[arrival] = []
                self.jobs_by_arrival[arrival].append(job)
    
    def get_next_task(self, current_time):
        # Add newly arrived jobs
        if current_time in self.jobs_by_arrival:
            self.active_jobs.extend(self.jobs_by_arrival[current_time])
        
        # Remove completed jobs
        self.active_jobs = [job for job in self.active_jobs if not job.is_completed()]
        
        if not self.active_jobs:
            return None
        
        # Sort by period (ascending) - shorter period = higher priority
        next_job = min(self.active_jobs, key=lambda x: x.T)
        return next_job

    def execute_task(self, job, current_time):
        if job.start_time is None:
            job.start_time = current_time
        
        job.execute(1)
        
        if job.is_completed():
            job.completion_time = current_time + 1
            self.completed_jobs.append(job)

    def is_schedulable(self):
        # Liu and Layland bound for Rate Monotonic
        utilization = sum(self.tasks['C_i'] / self.tasks['T_i'])
        n = len(self.tasks)
        rm_bound = n * (2 ** (1/n) - 1)
        return utilization <= rm_bound

    def results(self):
        return {
            'completed_jobs': self.completed_jobs,
            'schedulable': self.is_schedulable()
        }

