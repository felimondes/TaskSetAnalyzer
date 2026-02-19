import math
import pandas as pd

class SchedulingSimulator:

    task_set = None
    algorithm = None
    
    def run(self, task_set:pd.DataFrame, scheduling_algorithm):
        self.task_set = task_set
        self.algorithm = scheduling_algorithm
        scheduling_algorithm.set_tasks(task_set)
        self._run()
        results = scheduling_algorithm.results()
        results['metrics'] = self.calculate_metrics(results['completed_jobs'])
        return results
            
    def _run(self):
        """
        Optimized simulation using smart time-stepping.
        Instead of checking every time unit, we batch execution and only
        re-evaluate scheduling at arrival times.
        """
        current_time = 0
        end_time = self.algorithm.get_running_time()
        
        # Get unique arrival times for smart stepping
        arrival_times = []
        if hasattr(self.algorithm, 'jobs_by_arrival'):
            arrival_times = sorted(self.algorithm.jobs_by_arrival.keys())
        
        arrival_idx = 0
        
        while current_time < end_time:
            next_job = self.algorithm.get_next_task(current_time)
            
            if next_job is None:
                # No job runnable, skip to next arrival
                if arrival_idx < len(arrival_times):
                    current_time = arrival_times[arrival_idx]
                    arrival_idx += 1
                else:
                    break
                continue
            
            # Set start time if not already set
            if next_job.start_time is None:
                next_job.start_time = current_time
            
            # How long until next scheduling decision point?
            if arrival_idx < len(arrival_times) and arrival_times[arrival_idx] > current_time:
                time_until_next_arrival = arrival_times[arrival_idx] - current_time
            else:
                time_until_next_arrival = end_time - current_time
            
            # How much time does job need?
            time_job_needs = next_job.remaining_time_till_done
            
            # Execute for minimum of the two
            execute_time = min(time_until_next_arrival, time_job_needs)
            
            if execute_time <= 0:
                current_time += 1
                continue
            
            # Execute the job in batch
            for _ in range(execute_time):
                next_job.execute(1)
            
            current_time += execute_time
            
            # Check if job completed
            if next_job.is_completed():
                next_job.completion_time = current_time
                self.algorithm.completed_jobs.append(next_job)
            
            # Move to next arrival time if we haven't yet
            if arrival_idx < len(arrival_times) and current_time >= arrival_times[arrival_idx]:
                current_time = arrival_times[arrival_idx]
                arrival_idx += 1

    def calculate_metrics(self, completed_jobs):
        """
        Calculate scheduling performance metrics:
        - Average response time (tr)
        - Total completion time (tc)
        - Weighted sum of completion times (tw)
        - Maximum lateness (Lmax)
        - Maximum number of late tasks (Nlate)
        """
        if not completed_jobs:
            return {}
        
        n = len(completed_jobs)
        
        # Average response time: tr = (1/n) * sum(fi - ai)
        response_times = [job.completion_time - job.arrival_time for job in completed_jobs]
        avg_response_time = sum(response_times) / n
        
        # Total completion time: tc = max(fi) - min(ai)
        completion_times = [job.completion_time for job in completed_jobs]
        arrival_times = [job.arrival_time for job in completed_jobs]
        total_completion_time = max(completion_times) - min(arrival_times)
        
        # Weighted sum of completion times: tw = sum(wi * fi)
        # Using wi = 1 for all jobs (can be modified if weights are available)
        weighted_sum = sum(job.completion_time for job in completed_jobs)
        
        # Maximum lateness: Lmax = max(fi - di)
        lateness_values = [job.completion_time - job.absolute_deadline for job in completed_jobs]
        max_lateness = max(lateness_values)
        
        # Maximum number of late tasks: Nlate = sum(miss(fi))
        # where miss(fi) = 1 if fi > di, 0 otherwise
        num_late_tasks = sum(1 for job in completed_jobs if job.is_late())
        
        return {
            'average_response_time': avg_response_time,
            'total_completion_time': total_completion_time,
            'weighted_sum_completion_times': weighted_sum,
            'max_lateness': max_lateness,
            'num_late_tasks': num_late_tasks,
            'response_times': response_times,
            'lateness_values': lateness_values
        }



