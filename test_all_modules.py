#!/usr/bin/env python3
"""Test runner for all modules"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Running Module Tests")
print("=" * 60)

# Test config
print("\n[1/8] Testing config.py...")
try:
    from config import DISTRIBUTION_MAPPING, CORES, TASKS, JITTER
    assert 'automotive' in DISTRIBUTION_MAPPING
    assert CORES == '1-core'
    print("✓ config.py tests passed")
except Exception as e:
    print(f"✗ config.py tests failed: {e}")

# Test job
print("\n[2/8] Testing job.py...")
try:
    import pandas as pd
    from job import Job
    task_series = pd.Series({'task_id': 1, 'C_i': 5, 'T_i': 10, 'D_i': 10})
    job = Job(task_series, activation=0)
    assert job.C == 5
    print("✓ job.py tests passed")
except Exception as e:
    print(f"✗ job.py tests failed: {e}")

# Test analysis
print("\n[3/8] Testing analysis.py...")
try:
    import pandas as pd
    from analysis import edf_processor_demand_test
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [1, 1],
        'T_i': [4, 5],
        'D_i': [4, 5]
    })
    result = edf_processor_demand_test(task_set)
    assert isinstance(result, bool)
    print("✓ analysis.py tests passed")
except Exception as e:
    print(f"✗ analysis.py tests failed: {e}")

# Test task_set_parser
print("\n[4/8] Testing task_set_parser.py...")
try:
    from parser import Parser
    parser = Parser()
    print("✓ task_set_parser.py tests passed (initialization)")
except Exception as e:
    print(f"✗ task_set_parser.py tests failed: {e}")

# Test EDF
print("\n[5/8] Testing earliest_deadline_first.py...")
try:
    import pandas as pd
    from earliest_deadline_first import EDF
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [2, 3],
        'T_i': [6, 8],
        'D_i': [6, 8]
    })
    edf = EDF()
    edf.set_tasks(task_set)
    assert edf.is_scheduable() == True
    print("✓ earliest_deadline_first.py tests passed")
except Exception as e:
    print(f"✗ earliest_deadline_first.py tests failed: {e}")

# Test RM
print("\n[6/8] Testing rate_monotonic.py...")
try:
    import pandas as pd
    from rate_monotonic import RateMonotonic
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [1, 2],
        'T_i': [4, 6],
        'D_i': [4, 6]
    })
    rm = RateMonotonic()
    rm.set_tasks(task_set)
    result = rm.is_scheduable()
    assert isinstance(result, bool)
    print("✓ rate_monotonic.py tests passed")
except Exception as e:
    print(f"✗ rate_monotonic.py tests failed: {e}")

# Test simulator
print("\n[7/8] Testing simulator.py...")
try:
    import pandas as pd
    from simulator import Simulator
    from earliest_deadline_first import EDF
    task_set = pd.DataFrame({
        'task_id': [1, 2],
        'C_i': [1, 2],
        'T_i': [4, 5],
        'D_i': [4, 5]
    })
    edf = EDF()
    sim = Simulator()
    results = sim.start(task_set, edf)
    assert 'completed_jobs' in results
    assert 'metrics' in results
    print("✓ simulator.py tests passed")
except Exception as e:
    print(f"✗ simulator.py tests failed: {e}")

print("\n" + "=" * 60)
print("All module tests completed!")
print("=" * 60)
