from scheduler import PeriodicTaskSetScheduler
import pandas as pd
from simulator import Simulator


class EDF(PeriodicTaskSetScheduler):

    def select_next_job_from_active(self, active_jobs: list):
        if not active_jobs:
            return None

        # Find jobs with earliest deadline
        earliest_deadline = min(job.d for job in active_jobs)
        jobs_with_earliest_deadline = [job for job in active_jobs if job.d == earliest_deadline]

        # If there is only one job with the earliest deadline, return it
        if len(jobs_with_earliest_deadline) == 1:
            return jobs_with_earliest_deadline[0]

        # If there are multiple jobs with the same earliest deadline, check if any is executing
        executing_job = next((job for job in jobs_with_earliest_deadline if job.isExecuting), None)
        if executing_job:
            return executing_job

        # If no job is executing, return the one with shortest period (like in RM)
        return min(jobs_with_earliest_deadline, key=lambda job: job.T)
    
    def is_scheduable(self, tasks):
        utilization = sum(tasks['C_i'] / tasks['T_i'])
        return utilization <= 1.0
    
    def get_least_upper_bound(self, n: int) -> float:
        return 1.0
    

if __name__ == '__main__':
    sim = Simulator()
    edf = EDF()

    # # Example 1: schedulable
    # task_set = pd.DataFrame({
    #     'task_id': ['A', 'B'],
    #     'T_i': [4, 5],
    #     'D_i': [4, 5],
    #     'C_i': [1, 3],
    # })

    # print(task_set)
    # results = sim.start(task_set, edf, True)
    # print("Job response times by task:", results.get("job_response_times_by_task"))
    # print("Activation times by task:", results.get("activation_times_by_task"))
    # print("Completion times by task:", results.get("completion_times_by_task"))
    # print("Schedulable (analysis):", results.get("schedulable_analysis"))
    # print("Schedulable (simulator):", results.get("schedulable_simulator"))


    # print("\n\n\n")

    task_set = pd.DataFrame({
        'task_id': ['A', 'B'],
        'T_i': [4, 5],
        'D_i': [4, 5],
        'C_i': [1, 5],
        'C_i_min': [1,3]
    })

    print(task_set)
    results = sim.start(task_set, edf, False)
    print("Job response times by task:", results.get("job_response_times_by_task"))
    print("Activation times by task:", results.get("activation_times_by_task"))
    print("Completion times by task:", results.get("completion_times_by_task"))
    print("Schedulable (analysis):", results.get("schedulable_analysis"))
    print("Schedulable (simulator):", results.get("schedulable_simulator"))
    print("Hyperperiod:", results.get("hyperperiod"))


