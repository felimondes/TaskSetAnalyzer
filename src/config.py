# ============================================================================
# CSV COLUMN NAMES - Original columns from task-set files
# ============================================================================
ORIGINAL_COLUMNS = {
    'JITTER': 'Jitter',
    'BCET': 'BCET',  # Best Case Execution Time
    'WCET': 'WCET',  # Worst Case Execution Time
    'PERIOD': 'Period',
    'DEADLINE': 'Deadline',
    'PE': 'PE',  # Processing Element
    'TASK_ID': 'TaskID',
}

# ============================================================================
# CSV COLUMN NAMES - Standardized names (Real-time scheduling notation)
# ============================================================================
# These are the names used internally after loading from CSV
STANDARDIZED_COLUMNS = {
    'JITTER': 'Jitter',
    'BCET': 'C_i_j_min',  # Minimum execution time (Best Case)
    'WCET': 'C_i_j',      # Maximum execution time (Worst Case) - C_i_j is the standard notation for execution time of task i on PE j
    'PERIOD': 'T_i',      # Task period
    'DEADLINE': 'D_i',    # Relative deadline
    'PE': 'PE',           # Processing Element
    'TASK_ID': 'TaskID',
}

# ============================================================================
# DIRECTORY STRUCTURE CONSTANTS
# ============================================================================
CORES = '1-core'
TASKS = '25-task'
JITTER = '0-jitter'

# ============================================================================
# DISTRIBUTION MAPPING
# ============================================================================
DISTRIBUTION_MAPPING = {
    'automotive': {
        'util_dist': 'automotive-utilDist',
        'per_dist': 'automotive-perDist',
        'prefix': 'automotive'
    },
    'uunifast': {
        'util_dist': 'uunifast-utilDist',
        'per_dist': 'uniform-discrete-perDist',
        'prefix': 'uniform-discrete'
    }
}


if __name__ == '__main__':
    print("Testing config constants...")
    
    # Test DISTRIBUTION_MAPPING
    assert 'automotive' in DISTRIBUTION_MAPPING
    assert 'uunifast' in DISTRIBUTION_MAPPING
    assert DISTRIBUTION_MAPPING['automotive']['util_dist'] == 'automotive-utilDist'
    print("✓ DISTRIBUTION_MAPPING configured correctly")
    
    # Test directory constants
    assert CORES == '1-core'
    assert TASKS == '25-task'
    assert JITTER == '0-jitter'
    print("✓ Directory structure constants defined")
    
    # Test column mappings
    assert 'WCET' in ORIGINAL_COLUMNS
    assert STANDARDIZED_COLUMNS['WCET'] == 'C_i_j'
    assert STANDARDIZED_COLUMNS['PERIOD'] == 'T_i'
    assert STANDARDIZED_COLUMNS['DEADLINE'] == 'D_i'
    print("✓ Column name mappings configured")
    
    print("All config tests passed!\n")
