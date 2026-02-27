from simulator import Simulator, TaskSetMetrics
from parser import Parser
from earliest_deadline_first import EDF
from rate_monotonic import RateMonotonic
import numpy as np
import pandas as pd
from parser import Parser
from typing import Optional, Dict
import plotting
sim = Simulator()
parser = Parser()


def run_simulation_for_each_algorithm(dfs, algorithms) -> Dict[str, list[TaskSetMetrics]]:
    results = {}
    for algorithm in algorithms:
        for df in dfs: 
            wcet = True
            result = sim.start(df, algorithm, wcet)
            results.setdefault(df["csv_id"][0], []).append((result))
    return results

def main():
    not_sched = "easy_examples\\not_schedulable"
    folder = "easy_examples\schedulable"
    
    dfs = parser.taskSetParser(not_sched)
    results = run_simulation_for_each_algorithm(dfs, [EDF(), RateMonotonic()])

    for task_set, results_for_each_algorithm in results.items():

        print(f"------- NEW TASK SET  ---------- \n")
        for result_for_algorithm in results_for_each_algorithm:
            #Task set 
            print(f"--- Metrics per algorithm  ---")
            print(f"Algorithm: {result_for_algorithm.algorithm}")
            print(f"Name: {result_for_algorithm.task_set["csv_id"][0]}")
            print(f"Util: {result_for_algorithm.util}")
            print(f"Lub: {result_for_algorithm.lub}")
            print(f"Late tasks: {result_for_algorithm.num_late_tasks}")
            print(f"Theoretical schedud: {result_for_algorithm.is_schedulable_theoretical}")
            print(f"Simulator scheduability: {result_for_algorithm.is_scheduable_simulator}")
            print("\n")
            
            #Each specific task
            # plotting.plot_average_response_times(result_for_algorithm)
            # plotting.plot_average_lateness(result_for_algorithm)
            # plotting.plot_activation_completion_spread(result_for_algorithm)

        
if __name__ == '__main__':
    main()

    

    

  










