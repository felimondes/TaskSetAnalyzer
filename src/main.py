from job import Job
from simulator import Simulator
from task_set_parser import TaskSetParser
from earliest_deadline_first import EDF
from rate_monotonic import RateMonotonic
import csv
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    sim = Simulator()
    edf = EDF()

    task_set = pd.DataFrame({
        'task_id': ['A', 'B'],
        'T_i': [4, 5],
        'D_i': [4, 5],
        'C_i': [1, 5],
        'C_i_min': [1,3]
    })

    wcet = False
    results = sim.start(task_set, edf, wcet)
    
    print(task_set)
    print("Job response times by task:", results.get("job_response_times_by_task"))
    print("Activation times by task:", results.get("activation_times_by_task"))
    print("Completion times by task:", results.get("completion_times_by_task"))
    print("Schedulable (analysis):", results.get("schedulable_analysis"))
    print("Schedulable (simulator):", results.get("schedulable_simulator"))
    print("Hyperperiod:", results.get("hyperperiod"))
    print("...")
    print("and more")

    

  










