import pandas as pd

class Job:
    def __init__(self, tasktype: pd.Series, arrival_time, deadline_offset=None):
        """
        Initialize a job instance.
        
        Args:
            tasktype: Task type parameters from DataFrame row
            arrival_time: When this job arrives in the system
            deadline_offset: Base time for deadline calculation (defaults to arrival_time)
        """
        if deadline_offset is None:
            deadline_offset = arrival_time

        # Handle task_id - it might be in the Series or be the index
        if 'task_id' in tasktype:
            self.task_id = tasktype['task_id']
        elif hasattr(tasktype, 'name'):
            self.task_id = tasktype.name
        else:
            self.task_id = 0
        # Normalize numeric fields to Python ints
        self.D = int(tasktype['D_i'])  # relative deadline
        self.C = int(tasktype['C_i'])  # execution time (worst case)
        self.T = int(tasktype['T_i'])  # period
        self.remaining_time_till_done = int(self.C)
        self.arrival_time = int(arrival_time)
        self.absolute_deadline = int(self.D + int(deadline_offset))
        self.completion_time = None
        self.start_time = None

    def execute(self, time_units):
        """Execute job for given number of time units"""
        self.remaining_time_till_done -= time_units

    def is_completed(self):
        """Check if job has finished execution"""
        return self.remaining_time_till_done <= 0

    def is_late(self):
        """Check if job missed its deadline"""
        if self.completion_time is None:
            return False
        return self.completion_time > self.absolute_deadline


if __name__ == '__main__':
    print("Testing Job class...")
    
    # Create a sample task
    task_series = pd.Series({
        'task_id': 1,
        'C_i': 5,
        'T_i': 10,
        'D_i': 10
    })
    
    # Test Job instantiation
    job = Job(task_series, arrival_time=0)
    assert job.task_id == 1
    assert job.C == 5
    assert job.T == 10
    assert job.D == 10
    assert job.arrival_time == 0
    assert job.absolute_deadline == 10
    print("✓ Job instantiation")
    
    # Test execution
    assert not job.is_completed()
    assert job.remaining_time_till_done == 5
    job.execute(2)
    assert job.remaining_time_till_done == 3
    print("✓ Job execution")
    
    # Test completion
    job.execute(3)
    assert job.is_completed()
    print("✓ Job completion")
    
    # Test lateness
    job.completion_time = 15
    assert job.is_late()
    job.completion_time = 10
    assert not job.is_late()
    print("✓ Job lateness detection")
    
    print("All Job tests passed!\n")
