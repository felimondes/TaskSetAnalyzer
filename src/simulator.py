import math
import pandas as pd
from job import Job
from rate_monotonic import RateMonotonic

class Simulator:
    def start(self, task_set: pd.DataFrame, algorithm):
        """Run simulation with given task set and scheduling algorithm.
        Accept either a scheduler class (callable) or an already-instantiated
        scheduler instance.
        """
        self._initialization(task_set, algorithm)
        self._run()
        return self._calculate_metrics(task_set)
    
    def _initialization(self, task_set: pd.DataFrame, algorithm):
        """Reset simulator state before running a new simulation."""
        self.algorithm = algorithm
        self.hyperperiod = self._get_hyperperiod(task_set)
       
        self.jobs_by_arrival_time = self._calculate_jobs_arrival_times(task_set, self.hyperperiod)
        self.sorted_arrival_times = sorted(x for x in self.jobs_by_arrival_time.keys())

        self.completed_jobs = []
        self.active_jobs = []

        self.current_time = 0
        self.arrival_idx = 0
    def _run(self):

        while self._is_active_jobs():
            self._activate_newly_arrived_jobs()
            job = self.algorithm.select_next_job_from_active(self.active_jobs)

            if job is None:
                self._advance_to_next_arrival()
                continue
            
            if job.s is None:
                job.set_started(self.current_time)
            
            execution_time = self._determine_execution_time(job)
            job.execute(execution_time)

            self.current_time += execution_time
            if job.is_complete():
                job.f = self.current_time
                job.response_time = job.f - job.a
                job.lateness = job.f - job.d
                self.completed_jobs.append(job)
                self.active_jobs.remove(job)
            self._update_arrival_index()

    def _calculate_metrics(self, task_set):
        job_response_times_by_task = {}
        job_lateness_by_task = {}
        weighted_sum = 0
        num_late_tasks = 0
        sum_response_times = 0
        completion_times = []
        arrival_times = []
        activation_times_by_task = {}
        completion_times_by_task = {}

        for job in self.completed_jobs:
            self._add_to_response_times(job, job_response_times_by_task)
            self._add_to_lateness_by_task(job, job_lateness_by_task)
            self._add_to_activation_times_by_task(job, activation_times_by_task)
            self._add_to_completion_times_by_task(job, completion_times_by_task)
            weighted_sum += job.f
            sum_response_times += job.response_time
            completion_times.append(job.f)
            arrival_times.append(job.a)
        

        
        num_late_tasks = sum(1 for job in self.completed_jobs if job.is_late())
        max_lateness = max(job_lateness_by_task.values())
        average_response_time = sum_response_times / len(self.completed_jobs) if self.completed_jobs else 0
        
        return {
            'average_response_time': average_response_time,
            'weighted_sum_completion_times': weighted_sum,
            'max_lateness': max_lateness,
            'num_late_tasks': num_late_tasks,
            'job_response_times_by_task': job_response_times_by_task,
            'lateness_by_job': job_lateness_by_task,
            'hyperperiod': self.hyperperiod,
            'jobs_of_each_type': {task_id: len(jobs) for task_id, jobs in self.jobs_by_arrival_time.items()},
            'activation_times_by_task': activation_times_by_task,
            'completion_times_by_task': completion_times_by_task,
            'schedulable_analysis': (self.algorithm.is_scheduable(task_set), self.algorithm.get_least_upper_bound(len(task_set)), self.algorithm.get_utilization(task_set)),
            'schedulable_simulator': (num_late_tasks == 0, num_late_tasks, max_lateness)
        }

    def _add_to_activation_times_by_task(self, job, activation_times_by_task):
        if job.task_id not in activation_times_by_task:
            activation_times_by_task[job.task_id] = []
        activation_times_by_task[job.task_id].append((job.job_id, job.a))
    def _add_to_completion_times_by_task(self, job, completion_times_by_task):
        if job.task_id not in completion_times_by_task:
            completion_times_by_task[job.task_id] = []
        completion_times_by_task[job.task_id].append((job.job_id, job.f))
    def _add_to_response_times(self, job, job_response_times_by_task):
        if job.task_id not in job_response_times_by_task:
            job_response_times_by_task[job.task_id] = []
        job_response_times_by_task[job.task_id].append((job.job_id, job.response_time))
    def _add_to_lateness_by_task(self, job, job_lateness_by_task):
        if job.task_id not in job_lateness_by_task:
            job_lateness_by_task[job.task_id] = []
        job_lateness_by_task[job.task_id].append((job.job_id, job.lateness))

    def _is_active_jobs(self):
        return self.arrival_idx < len(self.sorted_arrival_times) or self.active_jobs
    def _calculate_time_until_next_event(self):
        """Calculate time remaining until next scheduling decision point"""
        if self._is_more_arrivals():
            return  self.sorted_arrival_times[self.arrival_idx] - self.current_time
        else:
            return self.hyperperiod - self.current_time
    def _determine_execution_time(self, job):
        """Determine how long to execute job before next scheduling decision"""
        time_until_next_event = self._calculate_time_until_next_event()
        if time_until_next_event == 0:
            return 1  # Ensure we make progress even if next event is now
        return min(job.remaining_time_till_done, time_until_next_event)
    def _advance_to_next_arrival(self):
        """Move simulation time to next job arrival.

        If there are no future arrivals, advance to end_time so the main
        loop can terminate instead of stalling.
        """
        
        if self._is_more_arrivals():
            self.current_time = self.sorted_arrival_times[self.arrival_idx]
            self.arrival_idx += 1
            return
        
        self.current_time = self.hyperperiod
    def _update_arrival_index(self):
        """Conditionally advance time to next arrival if we've reached it"""
        if self._is_more_arrivals() and self.current_time >= self.sorted_arrival_times[self.arrival_idx]:
            self.arrival_idx += 1
    def _activate_newly_arrived_jobs(self):
        """Activate jobs that arrived at the current time"""
        if self.current_time in self.jobs_by_arrival_time:
            self.active_jobs.extend(self.jobs_by_arrival_time[self.current_time])
    def _calculate_jobs_arrival_times(self, task_set, hyperperiod):
        """Create all job instances for each task within the hyperperiod"""
        jobs_arrival_times = {}
        for index, task_type in task_set.iterrows():
            num_jobs = self._get_num_jobs_for_task(task_type, hyperperiod)
            for i in range(num_jobs):
                arrival_time = int(i * task_type['T_i'])
                job = Job(task_type, arrival_time)
                if arrival_time not in jobs_arrival_times:
                    jobs_arrival_times[arrival_time] = []
                jobs_arrival_times[arrival_time].append(job)

        return jobs_arrival_times
    
    def _get_hyperperiod(self, task_set):
        """Calculate hyperperiod of the task set"""
        periods = [int(p) for p in task_set['T_i'].tolist()]
        hyperperiod = math.lcm(*periods)
        return int(hyperperiod)
    def _get_num_jobs_for_task(self, task_type, hyperperiod):
            num_jobs = hyperperiod // task_type['T_i']
            return num_jobs
    def _is_more_arrivals(self):
        return self.arrival_idx < len(self.sorted_arrival_times)

