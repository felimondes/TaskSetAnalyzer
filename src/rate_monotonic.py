from scheduler import PeriodicTaskSetScheduler
import pandas as pd
import simulator
class RateMonotonic(PeriodicTaskSetScheduler):
    

    def select_next_job_from_active(self, active_jobs):
        if not active_jobs:
            return None
        return min(active_jobs, key=lambda job: job.T) #sort by period, shortest period has highest priority
    
    def is_scheduable(self, tasks):
        utilization = sum(tasks['C_i'] / tasks['T_i'])
        n = len(tasks)
        rm_bound = n * (2 ** (1/n) - 1)
        return utilization <= rm_bound
    
    def get_least_upper_bound(self, n):
        return n * (2 ** (1/n) - 1)

if __name__ == "__main__":

    simulator = simulator.Simulator()
    rate_monotonic_scheduler = RateMonotonic()

    #Sc
    task_set = pd.DataFrame({
        'task_id': ['A', 'B'],
        'T_i': [4, 5],
        'D_i': [4, 5],
        'C_i': [1, 3]
    })


    print(task_set)
    results = simulator.start(task_set, rate_monotonic_scheduler)
    print("Job response times by task: " + str(results["job_response_times_by_task"]))
    print("Activation times by task: " + str(results["activation_times_by_task"]))
    print("Completion times by task: " + str(results["completion_times_by_task"]))
    print("Schedulable: " + str(results["schedulable_analysis"]))
    print("Schedulable according to simulator: " + str(results["schedulable_simulator"]))


    print("\n\n\n")

    #Sc
    task_set = pd.DataFrame({
        'task_id': ['A', 'B'],
        'T_i': [4, 5],
        'D_i': [4, 5],
        'C_i': [1, 4]
    })


    print(task_set)
    results = simulator.start(task_set, rate_monotonic_scheduler)
    print("Job response times by task: " + str(results["job_response_times_by_task"]))
    print("Activation times by task: " + str(results["activation_times_by_task"]))
    print("Completion times by task: " + str(results["completion_times_by_task"]))
    print("Schedulable: " + str(results["schedulable_analysis"]))
    print("Schedulable according to simulator: " + str(results["schedulable_simulator"]))
    print("Hyperperiod: " + str(results["hyperperiod"]))