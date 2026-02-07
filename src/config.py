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
    'WCET': 'C_i_j',      # Maximum execution time (Worst Case)
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
