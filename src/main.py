from job import Job
from simulator import SchedulingSimulator
from task_set_parser import TaskSetParser
from earliest_deadline_first import EDF
from rate_monotonic import RateMonotonic
import csv
import os
from pathlib import Path

def run_single_task_set(task_set, scheduler_name):
    """Run simulation on a single task set with specified scheduler"""
    simulator = SchedulingSimulator()
    
    if scheduler_name.lower() == 'edf':
        scheduler = EDF()
    elif scheduler_name.lower() == 'rm':
        scheduler = RateMonotonic()
    else:
        raise ValueError(f"Unknown scheduler: {scheduler_name}")
    
    results = simulator.run(task_set, scheduler)
    return results

def run_multiple_task_sets(distribution, util_min, util_max, csv_id=0, step=0.10):
    """
    Run simulations on multiple task sets within utilization range.
    
    Args:
        distribution: Distribution type (e.g., 'automotive', 'uunifast')
        util_min: Minimum utilization level (e.g., 0.10)
        util_max: Maximum utilization level (e.g., 0.60)
        csv_id: CSV identifier (default 0)
        step: Utilization step size (default 0.10)
    
    Returns:
        Dictionary with results for each utilization level and scheduler
    """
    parser = TaskSetParser()
    results = {}
    
    # Generate utilization levels
    util_level = util_min
    while util_level <= util_max + 1e-9:  # +epsilon to handle floating point
        util_rounded = round(util_level, 2)
        print(f"Processing {distribution} at utilization {util_rounded}...", end=" ", flush=True)
        
        try:
            # Parse task set
            task_set = parser.parse(distribution, util_rounded, csv_id)
            
            results[util_rounded] = {}
            
            # Run EDF
            edf_results = run_single_task_set(task_set, 'edf')
            results[util_rounded]['edf'] = edf_results
            
            # Run Rate Monotonic
            rm_results = run_single_task_set(task_set, 'rm')
            results[util_rounded]['rm'] = rm_results
            
        except FileNotFoundError as e:
            print("⚠ Skipped")
            results[util_rounded] = None
        
        util_level += step
    
    return results

def save_results_to_csv(results, output_file):
    """
    Save simulation results to CSV file.
    
    Args:
        results: Dictionary of results from run_multiple_task_sets
        output_file: Path to output CSV file
    """
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow([
            'Utilization',
            'EDF_Jobs_Completed',
            'EDF_Schedulable',
            'EDF_Avg_Response_Time',
            'EDF_Total_Completion_Time',
            'EDF_Weighted_Sum_Completion',
            'EDF_Max_Lateness',
            'EDF_Late_Tasks',
            'RM_Jobs_Completed',
            'RM_Schedulable',
            'RM_Avg_Response_Time',
            'RM_Total_Completion_Time',
            'RM_Weighted_Sum_Completion',
            'RM_Max_Lateness',
            'RM_Late_Tasks'
        ])
        
        # Write data rows
        for util in sorted(results.keys()):
            if results[util] is None:
                writer.writerow([util] + ['N/A'] * 14)
                continue
            
            edf = results[util].get('edf')
            rm = results[util].get('rm')
            
            row = [util]
            
            # EDF metrics
            if edf:
                row.extend([
                    len(edf['completed_jobs']),
                    edf['schedulable'],
                    edf['metrics'].get('average_response_time', 'N/A'),
                    edf['metrics'].get('total_completion_time', 'N/A'),
                    edf['metrics'].get('weighted_sum_completion_times', 'N/A'),
                    edf['metrics'].get('max_lateness', 'N/A'),
                    edf['metrics'].get('num_late_tasks', 'N/A')
                ])
            else:
                row.extend(['N/A'] * 7)
            
            # RM metrics
            if rm:
                row.extend([
                    len(rm['completed_jobs']),
                    rm['schedulable'],
                    rm['metrics'].get('average_response_time', 'N/A'),
                    rm['metrics'].get('total_completion_time', 'N/A'),
                    rm['metrics'].get('weighted_sum_completion_times', 'N/A'),
                    rm['metrics'].get('max_lateness', 'N/A'),
                    rm['metrics'].get('num_late_tasks', 'N/A')
                ])
            else:
                row.extend(['N/A'] * 7)
            
            writer.writerow(row)
    
    print(f"Results saved to {output_file}")

def create_plots(results, output_dir='results/plots'):
    """
    Create comparison plots for the results.
    
    Args:
        results: Dictionary of results from run_multiple_task_sets
        output_dir: Directory to save plots
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib not installed. Skipping plots.")
        print("Install with: pip install matplotlib")
        return
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    utils = sorted([u for u in results.keys() if results[u] is not None])
    
    if not utils:
        print("No valid results to plot")
        return
    
    # Extract data
    edf_late_tasks = []
    rm_late_tasks = []
    edf_max_lateness = []
    rm_max_lateness = []
    edf_avg_response = []
    rm_avg_response = []
    
    for util in utils:
        if results[util]:
            edf = results[util].get('edf')
            rm = results[util].get('rm')
            
            edf_late_tasks.append(edf['metrics'].get('num_late_tasks', 0) if edf else 0)
            rm_late_tasks.append(rm['metrics'].get('num_late_tasks', 0) if rm else 0)
            edf_max_lateness.append(edf['metrics'].get('max_lateness', 0) if edf else 0)
            rm_max_lateness.append(rm['metrics'].get('max_lateness', 0) if rm else 0)
            edf_avg_response.append(edf['metrics'].get('average_response_time', 0) if edf else 0)
            rm_avg_response.append(rm['metrics'].get('average_response_time', 0) if rm else 0)
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Scheduling Algorithm Comparison across Task Sets', fontsize=16, fontweight='bold')
    
    # Plot 1: Late Tasks
    ax = axes[0, 0]
    x = np.arange(len(utils))
    width = 0.35
    ax.bar(x - width/2, edf_late_tasks, width, label='EDF', alpha=0.8)
    ax.bar(x + width/2, rm_late_tasks, width, label='RM', alpha=0.8)
    ax.set_xlabel('Utilization')
    ax.set_ylabel('Number of Late Tasks')
    ax.set_title('Late Tasks vs Utilization')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{u:.2f}' for u in utils])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Plot 2: Maximum Lateness
    ax = axes[0, 1]
    ax.plot(utils, edf_max_lateness, 'o-', label='EDF', linewidth=2, markersize=8)
    ax.plot(utils, rm_max_lateness, 's-', label='RM', linewidth=2, markersize=8)
    ax.set_xlabel('Utilization')
    ax.set_ylabel('Maximum Lateness (time units)')
    ax.set_title('Maximum Lateness vs Utilization')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Average Response Time
    ax = axes[1, 0]
    ax.plot(utils, edf_avg_response, 'o-', label='EDF', linewidth=2, markersize=8)
    ax.plot(utils, rm_avg_response, 's-', label='RM', linewidth=2, markersize=8)
    ax.set_xlabel('Utilization')
    ax.set_ylabel('Average Response Time (time units)')
    ax.set_title('Average Response Time vs Utilization')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Performance Comparison (Late Tasks)
    ax = axes[1, 1]
    diff = np.array(rm_late_tasks) - np.array(edf_late_tasks)
    colors = ['green' if d <= 0 else 'red' for d in diff]
    ax.bar(utils, diff, color=colors, alpha=0.7)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Utilization')
    ax.set_ylabel('RM Late Tasks - EDF Late Tasks')
    ax.set_title('Algorithm Comparison (Negative = EDF Better)')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'scheduling_comparison.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {plot_file}")
    plt.close()

if __name__ == '__main__':
    # Run simulations
    print("Running simulations...")
    results = run_multiple_task_sets(
        distribution='automotive',
        util_min=0.10,
        util_max=0.20,
        csv_id=0,
        step=0.10
    )
    
    # Save results to CSV
    csv_file = 'results/scheduling_results.csv'
    save_results_to_csv(results, csv_file)
    
    # Create plots
    create_plots(results, 'results/plots')
    
    print("\nDone! Check the 'results' directory for output files.")











