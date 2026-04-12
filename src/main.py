from simulator import Simulator, TaskSetMetrics
from response_time_analysis_RM import response_time_analysis_rta
from response_time_analysis_RM import analyze_taskset, print_analysis_summary
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
folder_path = "test_examples"


path_to_taskset = "test_examples/not_schedulable/Unschedulable_Full_Utilization_NonUnique_Periods_taskset.csv"

def display_rta_results(dfs: list[pd.DataFrame]) -> None:
    """
    Nicely displays WCRT + schedulability results for multiple task sets.
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
            print("running")
            print(df["csv_id"])
            wcet = False
            result = sim.start(df, algorithm, wcet)
            results.setdefault(df["csv_id"][0], []).append((result))
    return results


def analysis():
    analysis_mode = "2"
    if analysis_mode == "1":
        
        df = parser.load_taskset_csv(path_to_taskset)
        is_sched, rta_results = response_time_analysis_rta(df)
        
        print(f"\nTaskset: {df['csv_id'].iloc[0]}")
        print(f"RTA schedulable: {is_sched}")
        
        cols = [c for c in ["task_id", "C_i", "T_i", "D_i", "R_i", "meets_deadline"] if c in rta_results.columns]
        print(rta_results[cols].to_string(index=False)) 

    elif analysis_mode == "2":
        dfs = parser.load_all_csvs_recursive(folder_path)
        display_rta_results(dfs)
        
        

        
    
    else:
        print("Invalid choice. Enter 1 or 2.")     



def simulation():
        folder = "test_examples"
        # folder = "dab"
        dfs = parser.load_all_csvs_recursive(folder)
        print("running simulation for each algorithm")
        results = run_simulation_for_each_algorithm(dfs, [RateMonotonic()])
        print("Done running simulations for each algorithm")

        for task_set, results_for_each_algorithm in results.items():
            print(f"------- NEW TASK SET  ---------- \n")
            for result_for_algorithm in results_for_each_algorithm:
                #Task set 
                # print(f"--- Metrics per algorithm  ---")
                print(f"Algorithm: {result_for_algorithm.algorithm}")
                print(f"Name: {result_for_algorithm.task_set["csv_id"][0]}")
                # print(f"Util: {result_for_algorithm.util}")
                # print(f"Lub: {result_for_algorithm.lub}")
                # print(f"Late tasks: {result_for_algorithm.num_late_tasks}")
                print(f"Theoretical schedud: {result_for_algorithm.is_schedulable_theoretical}")
                print(f"Simulator scheduability: {result_for_algorithm.is_scheduable_simulator}")
                print("\n")
                
                # #Each specific task
                # plotting.plot_all_task_metrics(result_for_algorithm)
     
def main():
        # analysis()
        simulation()

            
if __name__ == '__main__':
    main()
















