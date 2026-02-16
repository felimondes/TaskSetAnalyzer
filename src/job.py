import pandas as pd
class Job:
    
    def __init__(self, tasktype:pd.Series):

        t = type(tasktype)
        self.task_id = tasktype['task_id']
        self.D = tasktype['D_i'] #relative deadline
        self.C = tasktype['C_i'] #execution time
        self.T = tasktype['T_i'] #period (same as relative deadline)
        self.remaining_time_till_done = self.C

    def execute(self, time_units):
        self.remaining_time_till_done -= time_units

    