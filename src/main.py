from src.simulatorTool.simulator import Simulator, TaskSetMetrics
from src.analysisTool.response_time_analysis_RM import response_time_analysis_rta
from src.analysisTool.response_time_analysis_RM import analyze_taskset, print_analysis_summary
from src.misc.parser import Parser
from src.simulatorTool.earliest_deadline_first import EDF
from src.simulatorTool.rate_monotonic import RateMonotonic
import numpy as np
import pandas as pd
from typing import Optional, Dict
import src.misc.plotting as plotting
sim = Simulator()
parser = Parser()



#touch: simulation panel
wcet = False
isOnlyUnschedulableTestCases = False

if isOnlyUnschedulableTestCases:
    amountOfHyperPeriods = 100
else:
     amountOfHyperPeriods = 1


#dont touch
algorithms = [RateMonotonic(), EDF()]
path_to_all_tests = "test_examples"
path_to_unschedulable = "test_examples/not_schedulable"

def display_rta_results(dfs: list[pd.DataFrame]) -> None:
    """
    Made with AI
    """

    for idx, df in enumerate(dfs, start=1):
        print("\n" + "=" * 60)
        print(f" TASK SET {idx}")
        print("=" * 60)

        is_sched, results = response_time_analysis_rta(df)

        # Pretty status line
        status = "✅ SCHEDULABLE" if is_sched else "❌ NOT SCHEDULABLE"
        print(f"\nOverall Result: {status}\n")

        # Select and format columns for readability
        view = results[["C_i", "T_i", "D_i", "R_i", "meets_deadline"]].copy()

        # Optional: nicer formatting
        view["R_i"] = view["R_i"].round(3)

        print(view.to_string(index=False))

        print("\nSummary:")
        print(f"- Tasks: {len(results)}")
        print(f"- Deadline misses: {(~results['meets_deadline']).sum()}")
def run_simulation_for_each_algorithm(dfs, algorithms) -> Dict[str, list[TaskSetMetrics]]:
    results = {}
    for algorithm in algorithms:
        for df in dfs:
            result = sim.start(df, algorithm, wcet, amountOfHyperPeriods)
            results.setdefault(df["csv_id"][0], []).append((result))
    return results
def analysis():
    dfs = parser.load_all_csvs_recursive(path_to_all_tests)
    display_rta_results(dfs)

def simulation():
    
        if isOnlyUnschedulableTestCases:
             dfs = parser.load_all_csvs_recursive(path_to_unschedulable)
        else:
            dfs = parser.load_all_csvs_recursive(path_to_all_tests)

        print("Running simulations - this take 1 min ish")
        results = run_simulation_for_each_algorithm(dfs, algorithms)

        for task_set, results_for_each_algorithm in results.items():
            for result_for_algorithm in results_for_each_algorithm:
                #Task set 
                print(f"--- Metrics per algorithm  ---")
                print(f"Algorithm: {result_for_algorithm.algorithm}")
                print(f"Name: {result_for_algorithm.task_set['csv_id'][0]}")
                print(f"Util: {result_for_algorithm.util}")
                print(f"Late tasks: {result_for_algorithm.num_late_tasks}")
                print(f"Theoretical schedud: {result_for_algorithm.is_schedulable_theoretical}")
                print(f"Simulator scheduability: {result_for_algorithm.is_scheduable_simulator}")
                print("\n")
                
        
                plotting.plot_wcrt_table(result_for_algorithm, isOnlyUnschedulableTestCases)
     
def main():
        while True:
            print("Press 1 to run analysis tool")
            print("Press 2 to run simulation tool")
            print("Press anything else to quit")
            answer = input()
            if answer == "1":
                analysis()
            elif answer == "2": 
                simulation()
            else:
                break
            print("\n \n")

















