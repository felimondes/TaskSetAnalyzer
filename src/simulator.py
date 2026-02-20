import math
import pandas as pd

class SchedulingSimulator:

    task_set = None
    algorithm = None
    
    
    def run(self, task_set: pd.DataFrame, scheduling_algorithm):
        """Run simulation with given task set and scheduling algorithm.

        Accept either a scheduler class (callable) or an already-instantiated
        scheduler instance.
        """
        self.algorithm = scheduling_algorithm
        self.algorithm.set_tasks(task_set)
        # Normalize arrival times to Python ints to avoid numpy scalar issues
        self.arrival_times = sorted(int(x) for x in self.algorithm.jobs_by_arrival.keys())
        self._run()
        results = self.algorithm.results()
        results['metrics'] = self.calculate_metrics(results['completed_jobs'])
        return results
            
    def _run(self):
        current_time = 0
        end_time = self.algorithm.get_running_time()
        arrival_idx = 0
        while current_time < end_time:
            next_job = self.algorithm.get_next_job(current_time)
            
            if next_job is None:
                current_time = self._advance_to_next_arrival(current_time, arrival_idx, end_time)
                arrival_idx += 1
                continue
            
            self.algorithm.mark_job_started(next_job, current_time)
            
            time_until_next_event = self._calculate_time_until_next_event(
                current_time, end_time, arrival_idx
            )
            
            execution_time = self._determine_execution_time_slice(
                next_job, time_until_next_event
            )
            
            # Ensure execution_time is an int
            execution_time = int(execution_time)
            if execution_time <= 0:
                current_time += 1
                continue
            
            self._execute_job_batch(next_job, execution_time)
            current_time += execution_time
            
            if next_job.is_completed():
                self.algorithm.complete_job(next_job, current_time)
            
            current_time = self._try_advance_to_next_arrival(current_time, arrival_idx)
            if arrival_idx < len(self.arrival_times) and current_time >= self.arrival_times[arrival_idx]:
                arrival_idx += 1

    def _calculate_time_until_next_event(self, current_time, end_time, arrival_idx):
        """Calculate time remaining until next scheduling decision point"""
        if arrival_idx < len(self.arrival_times) and self.arrival_times[arrival_idx] > current_time:
            return self.arrival_times[arrival_idx] - current_time
        else:
            return end_time - current_time

    def _determine_execution_time_slice(self, job, time_until_next_event):
        """Determine how long to execute job before next scheduling decision"""
        # Return a Python int (min of ints) to keep loop counters consistent
        return int(min(int(time_until_next_event), int(job.remaining_time_till_done)))

    def _execute_job_batch(self, job, time_units):
        """Execute a job for multiple time units in batch"""
        for _ in range(int(time_units)):
            self.algorithm.execute_job(job, 1)

    def _advance_to_next_arrival(self, current_time, arrival_idx, end_time):
        """Move simulation time to next job arrival.

        If there are no future arrivals, advance to end_time so the main
        loop can terminate instead of stalling.
        """
        if arrival_idx < len(self.arrival_times):
            return self.arrival_times[arrival_idx]
        return end_time

    def _try_advance_to_next_arrival(self, current_time, arrival_idx):
        """Conditionally advance time to next arrival if we've reached it"""
        if arrival_idx < len(self.arrival_times) and current_time >= self.arrival_times[arrival_idx]:
            return self.arrival_times[arrival_idx]
        return current_time

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
        
        response_times = [job.completion_time - job.arrival_time for job in completed_jobs]
        avg_response_time = sum(response_times) / n
        
        completion_times = [job.completion_time for job in completed_jobs]
        arrival_times = [job.arrival_time for job in completed_jobs]
        total_completion_time = max(completion_times) - min(arrival_times)
        
        weighted_sum = sum(job.completion_time for job in completed_jobs)
        
        lateness_values = [job.completion_time - job.absolute_deadline for job in completed_jobs]
        max_lateness = max(lateness_values)
        
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


if __name__ == '__main__':
    import pandas as pd
    from job import Job
    print("Testing SchedulingSimulator...")
    
    # Test with minimal task set
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [1, 2],
        'T_i': [4, 5],
        'D_i': [4, 5]
    })
    
    from earliest_deadline_first import EDF
    from rate_monotonic import RateMonotonic
    
    # Test EDF simulation
    edf = EDF()
    sim = SchedulingSimulator()
    results_edf = sim.run(task_set, edf)
    assert 'completed_jobs' in results_edf
    assert 'schedulable' in results_edf
    assert 'metrics' in results_edf
    assert len(results_edf['completed_jobs']) > 0
    print(f"✓ EDF simulation: {len(results_edf['completed_jobs'])} jobs completed")
    
    # Test RM simulation
    rm = RateMonotonic()
    sim2 = SchedulingSimulator()
    results_rm = sim2.run(task_set, rm)
    assert len(results_rm['completed_jobs']) > 0
    print(f"✓ RM simulation: {len(results_rm['completed_jobs'])} jobs completed")
    
    # Test metrics calculation
    metrics = results_edf['metrics']
    assert metrics['average_response_time'] > 0
    assert metrics['total_completion_time'] > 0
    assert 'num_late_tasks' in metrics
    print(f"✓ Metrics calculated: avg_response_time={metrics['average_response_time']:.2f}")
    
    print("All Simulator tests passed!\n")



