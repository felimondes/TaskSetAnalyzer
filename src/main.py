from simulator import Simulator, TaskSetMetrics
from analyser import response_time_analysis_rta
from analyser import analyze_taskset, analyze_tasksets_in_folder, print_analysis_summary
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

    # Use AnalysisTool or SimulationTool:
    tool_used = input("Choose tool: \n1. Analysis Tool \n2. Simulation Tool \nEnter 1 or 2: ").strip()



    if tool_used == "1":
        print("Analysis tool, lets get started with analysing")
        
        # Choose analysis mode
        analysis_mode = input("Analyze (1) single taskset or (2) folder? Enter 1 or 2: ").strip()
        
        if analysis_mode == "1":
            # Single taskset analysis
            path_to_taskset = "easy_examples/not_schedulable/Unschedulable_Full_Utilization_NonUnique_Periods_taskset.csv"
            
            parser_obj = parser
            df = parser_obj.load_taskset_csv(path_to_taskset)
            
            is_sched, rta_results = response_time_analysis_rta(df)
            
            print(f"\nTaskset: {df['csv_id'].iloc[0]}")
            print(f"RTA schedulable: {is_sched}")
            
            cols = [c for c in ["task_id", "C_i", "T_i", "D_i", "R_i", "meets_deadline"] if c in rta_results.columns]
            print(rta_results[cols].to_string(index=False))
        
        elif analysis_mode == "2":
            # Folder analysis
            folder_path = "easy_examples/schedulable"
            folder_results = analyze_tasksets_in_folder(folder_path)
            print_analysis_summary(folder_results)
            
            # Print detailed results for each taskset
            for csv_id, schedulable, result_df in folder_results:
                print(f"\n{csv_id}: {'SCHEDULABLE' if schedulable else 'NOT SCHEDULABLE'}")
                cols = [c for c in ["task_id", "C_i", "T_i", "D_i", "R_i", "meets_deadline"] if c in result_df.columns]
                print(result_df[cols].to_string(index=False))
        
        else:
            print("Invalid choice. Enter 1 or 2.")

    elif tool_used == "2":

        not_sched = "easy_examples\\not_schedulable"
        folder = "easy_examples\\schedulable"
        

        dfs = parser.taskSetParser(not_sched)
        print("running simulation for each algorithm")
        results = run_simulation_for_each_algorithm(dfs, [EDF(), RateMonotonic()])
        print("Done running simulations for each algorithm")

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
    else:
            print("Invalid choice. Enter 1 or 2.")
        
if __name__ == '__main__':
    main()
















