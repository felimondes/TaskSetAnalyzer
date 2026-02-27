import math
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import pandas as pd

from job import Job


class Simulator:
 
    def start(self, task_set: pd.DataFrame, scheduler: Any, wcet: bool) -> TaskSetMetrics:
        self._initialize(task_set, scheduler, wcet)
        self._run()
        return self._calculate_metrics(task_set)
    
    def _initialize(self, task_set: pd.DataFrame, scheduler: Any, wcet: bool) -> None:
        self.wcet = wcet
        self.scheduler = scheduler
        self.hyperperiod: int = self._get_hyperperiod(task_set)

        self.jobs_by_arrival_time: Dict[int, List[Job]] = self._calculate_jobs_arrival_times(task_set, self.hyperperiod)
        self.sorted_arrival_times: List[int] = sorted(self.jobs_by_arrival_time.keys())

        self.completed_jobs: List[Job] = []
        self.active_jobs: List[Job] = []

        self.current_time: int = 0
        self.arrival_idx: int = 0
        self.job_in_execution: Optional[Job] = None
    def _run(self) -> None:
        while self._has_pending_events():
            self._activate_newly_arrived_jobs()

            job = self.scheduler.select_next_job_from_active(self.active_jobs)

            if job is None:
                self._advance_to_next_arrival()
                continue
            
            if job.s is None:
                job.set_started(self.current_time)

            execution_time = self._determine_execution_time(job)
            self._execute_job(job, execution_time)

            self.current_time += execution_time
            if job.is_complete():
                self._remove_executing_job()
                job.f = self.current_time
                job.response_time = job.f - job.a
                job.lateness = job.f - job.d
                self.completed_jobs.append(job)
                self.active_jobs.remove(job)

            self._update_arrival_index()

    def _calculate_metrics(self, task_set: pd.DataFrame) -> TaskSetMetrics:
        """Aggregate per-job and per-task statistics for the run."""
        job_response_times_by_task: Dict[str, List] = {}
        lateness_by_task: Dict[str, List] = {}
        activation_times_by_task: Dict[str, List] = {}
        completion_times_by_task: Dict[str, List] = {}

        sum_response_times = 0

        for job in self.completed_jobs:
            self._add_to_response_times(job, job_response_times_by_task)
            self._add_to_lateness_by_task(job, lateness_by_task)
            self._add_to_activation_times_by_task(job, activation_times_by_task)
            self._add_to_completion_times_by_task(job, completion_times_by_task)

            sum_response_times += job.response_time if job.response_time is not None else 0

        total_late_tasks = sum(1 for job in self.completed_jobs if job.is_late())
        lateness_values = [job.lateness for job in self.completed_jobs if job.lateness is not None]
        max_lateness = max(lateness_values) if lateness_values else 0

        average_response_time = (sum_response_times / len(self.completed_jobs)) if self.completed_jobs else 0

      
        is_scheduable = self.scheduler.is_scheduable(task_set)
        lub = self.scheduler.get_least_upper_bound(task_set)
        util = self.scheduler.get_utilization(task_set)

        return TaskSetMetrics(
            algorithm=str(self.scheduler),
            task_set=task_set,
            average_response_time=round(average_response_time, 2),
            is_schedulable_theoretical=is_scheduable,
            is_scheduable_simulator = total_late_tasks == 0,
            num_late_tasks=total_late_tasks,
            lub=lub,
            util=util,
            job_lateness_by_task=lateness_by_task,
            job_response_times_by_task=job_response_times_by_task,
            job_activation_times_by_task=activation_times_by_task,
            job_completion_times_by_task=completion_times_by_task,
        )


#Helpers 
    def _execute_job(self, job: Job, time_units: int) -> None:
        #If no jobs executing
        if not self.job_in_execution:
            job.execute(time_units)
            job.isExecuting = True
            self.job_in_execution = job
        
        #If the same job is executing, continue executing it
        elif self.job_in_execution == job:
            job.execute(time_units)
        
        #If a different job is executing, preempt it and start executing the new job
        else:
            self._remove_executing_job()
            job.execute(time_units)
            job.isExecuting = True
            self.job_in_execution = job
    def _remove_executing_job(self) -> None:
        if self.job_in_execution:
            self.job_in_execution.isExecuting = False
            self.job_in_execution = None

    def _has_pending_events(self) -> bool:
        return self.arrival_idx < len(self.sorted_arrival_times) or bool(self.active_jobs)
    def _calculate_time_until_next_event(self) -> int:
        """Time until the next arrival or the end of the hyperperiod."""
        if self._is_more_arrivals():
            return self.sorted_arrival_times[self.arrival_idx] - self.current_time
        return math.inf #there is no event afterwards
    def _determine_execution_time(self, job: Job) -> int:
        """Execution slice length before the next scheduling decision."""
        time_until_next_event = self._calculate_time_until_next_event()
        if time_until_next_event == 0:
            return 1
        return min(job.remaining_time_till_done, time_until_next_event)
    def _advance_to_next_arrival(self) -> None:
        """Advance simulation time to the next arrival time or hyperperiod end."""
        if self._is_more_arrivals():
            self.current_time = self.sorted_arrival_times[self.arrival_idx]
            self.arrival_idx += 1
            return
        self.current_time = self.hyperperiod
    def _update_arrival_index(self) -> None:
        """Advance the arrival index if we've reached or passed the next arrival."""
        if self._is_more_arrivals() and self.current_time >= self.sorted_arrival_times[self.arrival_idx]:
            self.arrival_idx += 1
    def _activate_newly_arrived_jobs(self) -> None:
        """Move jobs that arrive at `current_time` to the active list."""
        if self.current_time in self.jobs_by_arrival_time:
            self.active_jobs.extend(self.jobs_by_arrival_time[self.current_time])
    def _calculate_jobs_arrival_times(self, task_set: pd.DataFrame, hyperperiod: int) -> Dict[int, List[Job]]:
        """Instantiate Job objects for each release within the hyperperiod."""
        jobs_arrival_times: Dict[int, List[Job]] = {}
        for _, task_type in task_set.iterrows():
            num_jobs = self._get_num_jobs_for_task(task_type, hyperperiod)
            for i in range(num_jobs):
                arrival_time = int(i * task_type['T_i'])
                job = Job(task_type, arrival_time, self.wcet)
                jobs_arrival_times.setdefault(arrival_time, []).append(job)

        return jobs_arrival_times
    
    def _add_to_activation_times_by_task(self, job: Job, activation_times_by_task: Dict[str, List]) -> None:
        activation_times_by_task.setdefault(job.task_id, []).append((job.job_id, job.a))
    def _add_to_completion_times_by_task(self, job: Job, completion_times_by_task: Dict[str, List]) -> None:
        completion_times_by_task.setdefault(job.task_id, []).append((job.job_id, job.f))
    def _add_to_response_times(self, job: Job, job_response_times_by_task: Dict[str, List]) -> None:
        job_response_times_by_task.setdefault(job.task_id, []).append((job.job_id, job.response_time))
    def _add_to_lateness_by_task(self, job: Job, job_lateness_by_task: Dict[str, List]) -> None:
        job_lateness_by_task.setdefault(job.task_id, []).append((job.job_id, job.lateness))

    def _get_hyperperiod(self, task_set: pd.DataFrame) -> int:
        """Compute the hyperperiod (LCM of task periods)."""
        periods = [int(p) for p in task_set['T_i'].tolist()]
        hyperperiod = math.lcm(*periods)
        return int(hyperperiod)
    def _get_num_jobs_for_task(self, task_type: pd.Series, hyperperiod: int) -> int:
        return hyperperiod // task_type['T_i']
    def _is_more_arrivals(self) -> bool:
        return self.arrival_idx < len(self.sorted_arrival_times)


@dataclass(frozen=True)
class TaskSetMetrics:
    
    # ----- task set level -----
    algorithm:str 
    is_scheduable_simulator: bool
    task_set: pd.DataFrame
    average_response_time: float
    is_schedulable_theoretical: bool
    lub: float
    util: float
    num_late_tasks: int

    # ----- per task -----
    job_lateness_by_task: Dict[str, List[Tuple[str, float]]]
    job_response_times_by_task: Dict[str, List[Tuple[str, float]]]
    job_activation_times_by_task: Dict[str, List[Tuple[str, float]]]
    job_completion_times_by_task: Dict[str, List[Tuple[str, float]]]