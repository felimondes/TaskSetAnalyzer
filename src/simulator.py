import math
import pandas as pd

class Simulator:

    def run(self, task_set:pd.DataFrame, scheduler):
        scheduler.set_tasks(task_set)
        clock = 0
        hyperperiod = scheduler.get_hyperperiod()

        while clock < hyperperiod:
            next_task = scheduler.get_next_task(clock)
            scheduler.execute_task(next_task, clock)
            clock += 1
            

        

    def calculate_hyperperiod_periodic_tasks(self, task_set):
        periods = task_set['T_i'].tolist()
        hyperperiod = math.lcm(*periods)
        return hyperperiod

