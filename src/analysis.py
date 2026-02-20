import math
from typing import Dict, Any, List


def lcm_of_periods(periods: List[int]) -> int:
    from math import gcd
    l = 1
    for p in periods:
        l = l * p // gcd(l, p)
    return l


# Note: Deadline-Monotonic response-time analysis removed per user request.


def edf_processor_demand_test(tasks_df) -> bool:
    """
    Exact EDF schedulability test using the Processor Demand criterion.

    Returns True if the task set is schedulable under EDF (deadlines <= periods).
    """
    tasks = []
    periods = []
    for idx, row in tasks_df.iterrows():
        C = int(row['C_i'])
        T = int(row['T_i'])
        D = int(row['D_i'])
        tasks.append({'C': C, 'T': T, 'D': D})
        periods.append(T)

    if not tasks:
        return True

    hyper = lcm_of_periods(periods)

    # Generate candidate test points: all k*T + D within [1, hyper]
    candidate_times = set()
    for task in tasks:
        if task['T'] <= 0:
            continue
        max_k = (hyper - task['D']) // task['T'] if hyper >= task['D'] else 0
        for k in range(0, max_k + 1):
            t = task['D'] + k * task['T']
            if 1 <= t <= hyper:
                candidate_times.add(t)

    if not candidate_times:
        return True

    for t in sorted(candidate_times):
        demand = 0
        for task in tasks:
            if t >= task['D']:
                num_jobs = (t - task['D']) // task['T'] + 1
                demand += num_jobs * task['C']

        if demand > t:
            return False

    return True


def compute_wcrts_from_completed_jobs(completed_jobs) -> Dict[int, int]:
    """
    From a list of completed Job objects, compute observed worst-case response
    time per task_id.
    """
    per_task = {}
    for job in completed_jobs:
        tid = int(job.task_id)
        rt = int(job.completion_time - job.arrival_time)
        if tid not in per_task or rt > per_task[tid]:
            per_task[tid] = rt
    return per_task


if __name__ == '__main__':
    import pandas as pd
    from job import Job
    print("Testing analysis functions...")
    
    # Test lcm_of_periods
    periods = [4, 6]
    lcm = lcm_of_periods(periods)
    assert lcm == 12
    print("✓ lcm_of_periods works (lcm(4,6)=12)")
    
    # Test edf_processor_demand_test
    task_set_schedulable = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [1, 1],
        'T_i': [4, 5],
        'D_i': [4, 5]
    })
    assert edf_processor_demand_test(task_set_schedulable) == True
    print("✓ EDF processor demand test: schedulable task set identified")
    
    # Test with unschedulable task set
    task_set_unschedulable = pd.DataFrame({
        'task_id': [1, 2, 3],
        'C_i': [3, 3, 3],
        'T_i': [5, 5, 5],
        'D_i': [5, 5, 5]
    })
    assert edf_processor_demand_test(task_set_unschedulable) == False
    print("✓ EDF processor demand test: unschedulable task set identified")
    
    # Test compute_wcrts_from_completed_jobs
    jobs = []
    for i in range(1, 4):
        task = pd.Series({'task_id': i, 'C_i': 1, 'T_i': 10, 'D_i': 10})
        job = Job(task, arrival_time=0)
        job.completion_time = 5 + i * 2  # vary completion times
        jobs.append(job)
    
    wcrts = compute_wcrts_from_completed_jobs(jobs)
    assert len(wcrts) == 3
    assert wcrts[1] == 5
    assert wcrts[2] == 7
    assert wcrts[3] == 9
    print(f"✓ compute_wcrts_from_completed_jobs: {wcrts}")
    
    print("All analysis tests passed!\n")
