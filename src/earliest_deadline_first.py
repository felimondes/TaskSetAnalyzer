

from abc import abstractmethod
from scheduler import Scheduler


class EDF(Scheduler):


    def get_hyperperiod(self, task_set):
        import math
        periods = task_set['T_i'].tolist()
        hyperperiod = math.lcm(*periods)
        return hyperperiod
    
    def set_tasks(self, tasks):
        self.tasks = tasks


    def set_jobs(self):
        self.jobs = []
        for index, row in self.tasks.iterrows():
            for k in range(0, self.get_hyperperiod(self.tasks) // row['T_i']):
                job = {
                    'task_id': row['task_id'],
                    'C_i': row['C_i'],
                    'D_i': row['D_i'] + k * row['T_i'],
                    'R_i': 0,
                    'remaining_time': row['C_i']
                }
                self.jobs.append(job)
    
    def get_next_task(self, current_time):
        pass

    def execute_task(self, task, current_time):
        pass

    def is_schedulable(self):
        pass

