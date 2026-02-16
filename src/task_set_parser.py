import pandas as pd
from pathlib import Path
from typing import Optional

from config import (
    DISTRIBUTION_MAPPING,
    CORES,
    TASKS,
    JITTER,
)


class TaskSetParser:

    DISTRIBUTION_MAPPING = DISTRIBUTION_MAPPING
    CORES = CORES
    TASKS = TASKS
    JITTER = JITTER

    def __init__(self, task_sets_root: Optional[str] = None):
        if task_sets_root is None:
            # Assume standard project structure: src/../task-sets
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            self.task_sets_root = project_root / "task-sets"
        else:
            self.task_sets_root = Path(task_sets_root)

        if not self.task_sets_root.exists():
            raise FileNotFoundError(
                f"Task sets directory not found at {self.task_sets_root}"
            )

    def parse(
        self,
        distribution: str,
        util_level: float,
        csv_identifier: int
    ) -> pd.DataFrame:
        #inputs are steps in the path to the csv file.

        # Validate distribution type
        if distribution.lower() not in self.DISTRIBUTION_MAPPING:
            raise ValueError(
                f"Invalid distribution type: '{distribution}'. "
                f"Must be one of {list(self.DISTRIBUTION_MAPPING.keys())}"
            )

        distribution = distribution.lower()
        dist_info = self.DISTRIBUTION_MAPPING[distribution]

        # Format utilization level (e.g., 0.10 -> '0.10-util')
        util_folder = f"{util_level:.2f}-util"

        # Format CSV filename (e.g., 'automotive_10.csv')
        csv_filename = f"{dist_info['prefix']}_{csv_identifier}.csv"

        # Construct the full path
        csv_path = (
            self.task_sets_root /
            'output' /
            dist_info['util_dist'] /
            dist_info['per_dist'] /
            self.CORES /
            self.TASKS /
            self.JITTER /
            util_folder /
            'tasksets' /
            csv_filename
        )

        # Check if file exists
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Task set file not found: {csv_path}\n"
                f"Parameters: distribution='{distribution}', "
                f"util_level={util_level}, csv_identifier={csv_identifier}"
            )

        # Load and return the DataFrame
        df = pd.read_csv(csv_path)

        # Add metadata as attributes
        df.attrs['distribution'] = distribution
        df.attrs['util_level'] = util_level
        df.attrs['csv_identifier'] = csv_identifier
        df.attrs['file_path'] = str(csv_path)

        #rename columns to standard names
        df.rename(columns={
            'BCET': 'C_i_j_min',
            'WCET': 'C_i_j',
            'Period': 'T_i',
            'Deadline': 'D_i',
        }, inplace=True)

        return df
