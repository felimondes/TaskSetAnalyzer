import pandas as pd
class Job:
    
    def __init__(self, tasktype:pd.Series, arrival_time=0, deadline_offset=0):

        t = type(tasktype)
        # Handle task_id - it might be in the Series or be the index
        if 'task_id' in tasktype:
            self.task_id = tasktype['task_id']
        elif hasattr(tasktype, 'name'):
            self.task_id = tasktype.name
        else:
            self.task_id = 0
        
        self.D = tasktype['D_i'] #relative deadline
        self.C = tasktype['C_i'] #execution time
        self.T = tasktype['T_i'] #period (same as relative deadline)
        self.remaining_time_till_done = self.C
        self.arrival_time = arrival_time
        self.absolute_deadline = self.D + deadline_offset
        self.completion_time = None
        self.start_time = None

    def execute(self, time_units):
        self.remaining_time_till_done -= time_units

    def is_completed(self):
        return self.remaining_time_till_done <= 0

    def is_late(self):
        if self.completion_time is None:
            return False
        return self.completion_time > self.absolute_deadline
