import pandas as pd

class Job:
    def __init__(self, tasktype: pd.Series, activation):

        self.job_id = f"{tasktype['task_id']}_{activation}"
        self.task_id = tasktype['task_id']
        self.T = tasktype['T_i']                    # period
        D = tasktype['D_i']                         # relative deadline
        C = tasktype['C_i']                         # execution time (worst case) #TODO Allow for flex execution times in the future
        self.remaining_time_till_done = int(C)      # time left to execute before job is completed
        self.d = int(activation + D)                # absolute deadline
        self.a = activation                         # activation
        self.s = None                               # start time
        self.f = None                               # finish time
        self.completion_time = None                 # time when job completed execution

        self.lateness = None                        # lateness
        self.response_time = None                   # response time



    def is_complete(self):
        if self.remaining_time_till_done < 0:
            raise ValueError(f"Job {self.task_id} over-executed by {-self.remaining_time_till_done} time units") #TODO fix why this happens, if it happens at all X)
        return self.remaining_time_till_done == 0

   

    def execute(self, time_units):
        self.remaining_time_till_done -= time_units
 
 
    def set_started(self, start_time):
            """Mark when a job first starts execution"""
            if self.s is None:
                self.s = start_time
    
    def is_late(self):
        """Check if job missed its deadline"""
        if self.f is None:
            return False
        return self.f > self.d