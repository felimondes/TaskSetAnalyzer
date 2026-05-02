import numpy as np
import pandas as pd
from src.misc.parser import Parser

def response_time_analysis_rta(df: pd.DataFrame) -> tuple[bool, pd.DataFrame]:
    """
    Worst-case response time analysis (Buttazzo Eq. 4.19, Fig. 4.17).
    Returns: (schedulable, results_df)
    """
    required = {"C_i", "T_i", "D_i"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Taskset missing required columns: {sorted(missing)}")

    work = df.sort_values(by=["D_i", "T_i"]).reset_index(drop=True)

    C = work["C_i"].to_numpy(dtype=float)
    T = work["T_i"].to_numpy(dtype=float)
    D = work["D_i"].to_numpy(dtype=float)

    R = np.zeros(len(work), dtype=float)
    schedulable = True

    for i in range(len(work)):
        Ri = C[i]  # initial guess
        while True:
            Rold = Ri

            if i == 0:
                interference = 0.0
            else:
                interference = np.sum(np.ceil(Rold / T[:i]) * C[:i])

            Ri = C[i] + interference

            # Deadline miss => not schedulable
            if Ri > D[i]:
                schedulable = False
                break

            # Converged (fixed point reached)
            if Ri <= Rold:
                break

        R[i] = Ri

        if not schedulable:
            break

    results = work.copy()
    results["R_i"] = R
    results["meets_deadline"] = results["R_i"] <= results["D_i"]

    return schedulable, results


def analyze_taskset(csv_path: str) -> tuple[bool, pd.DataFrame]:
    """
    Analyze a single taskset from a CSV file.
    
    Args:
        csv_path: Relative path to the CSV file
        
    Returns:
        (schedulable, results_df)
    """
    parser = Parser()
    df = parser.load_taskset_csv(csv_path)
    return response_time_analysis_rta(df)




def print_analysis_summary(results: list[tuple[str, bool, pd.DataFrame]]):
    """
    Print a summary of analysis results for multiple tasksets.
    
    Args:
        results: Output from analyze_tasksets_in_folder
    """
    print(f"\n{'='*60}")
    print(f"Analysis Summary for {len(results)} tasksets")
    print(f"{'='*60}\n")
    
    schedulable_count = sum(1 for _, sched, _ in results if sched)
    
    for csv_id, schedulable, result_df in results:
        status = "✓ SCHEDULABLE" if schedulable else "✗ NOT SCHEDULABLE"
        print(f"{csv_id}: {status}")
    
    print(f"\n{'='*60}")
    print(f"Schedulable: {schedulable_count}/{len(results)}")
    print(f"{'='*60}\n")