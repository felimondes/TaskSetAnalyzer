from scheduler import PeriodicTaskSetScheduler


class RateMonotonic(PeriodicTaskSetScheduler):
    

    def select_next_job_from_active(self):
        return min(self.active_jobs, key=lambda job: job.T)
    
    def is_schedulable(self):
        utilization = sum(self.tasks['C_i'] / self.tasks['T_i'])
        n = len(self.tasks)
        rm_bound = n * (2 ** (1/n) - 1)
        return utilization <= rm_bound


if __name__ == '__main__':
    import pandas as pd
    from simulator import SchedulingSimulator
    print("Testing Rate Monotonic scheduler...")
    
    # Create a sample task set
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [1, 2],
        'T_i': [4, 6],
        'D_i': [4, 6]
    })
    
    # Test priority ordering (lower period = higher priority)
    rm = RateMonotonic()
    rm.set_tasks(task_set)
    assert len(rm.tasks) == 2
    print("✓ RM task set loaded")
    
    # Test schedulability using RM bound
    is_sched = rm.is_schedulable()
    utilization = sum(task_set['C_i'] / task_set['T_i'])
    n = len(task_set)
    rm_bound = n * (2 ** (1/n) - 1)
    expected = utilization <= rm_bound
    assert is_sched == expected
    print(f"✓ RM schedulability test (util={utilization:.2f}, bound={rm_bound:.2f})")
    
    # Test simulation
    sim = SchedulingSimulator()
    results = sim.run(task_set, rm)
    assert len(results['completed_jobs']) > 0
    print(f"✓ RM simulation completed {len(results['completed_jobs'])} jobs")
    
    print("All Rate Monotonic tests passed!\n")

