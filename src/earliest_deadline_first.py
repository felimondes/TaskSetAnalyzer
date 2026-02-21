from scheduler import PeriodicTaskSetScheduler


class EDF(PeriodicTaskSetScheduler):

    def select_next_job_from_active(self):
        return min(self.active_jobs, key=lambda job: job.absolute_deadline)
    
    def is_scheduable(self):
        utilization = sum(self.tasks['C_i'] / self.tasks['T_i'])
        return utilization <= 1.0


if __name__ == '__main__':
    import pandas as pd
    from simulator import Simulator
    print("Testing EDF scheduler...")
    
    # Create a sample task set
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [2, 3],
        'T_i': [6, 8],
        'D_i': [6, 8]
    })
    
    # Test schedulability
    edf = EDF()
    edf.set_tasks(task_set)
    assert edf.is_scheduable() == True
    print("✓ EDF schedulability test (utilization <= 1.0)")
    
    # Test job selection (EDF: earliest deadline first)
    sim = Simulator()
    results = sim.start(task_set, edf)
    assert results['schedulable'] == True
    assert len(results['completed_jobs']) > 0
    print(f"✓ EDF simulation completed {len(results['completed_jobs'])} jobs")
    
    # Test with overloaded task set
    task_set_overloaded = pd.DataFrame({
        'task_id': [1, 2, 3],
        'C_i': [3, 3, 3],
        'T_i': [5, 5, 5],
        'D_i': [5, 5, 5]
    })
    edf_ol = EDF()
    edf_ol.set_tasks(task_set_overloaded)
    assert edf_ol.is_scheduable() == False
    print("✓ EDF correctly identifies unschedulable task set (utilization > 1.0)")
    
    print("All EDF tests passed!\n")


