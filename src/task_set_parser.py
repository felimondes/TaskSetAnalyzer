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

    def __init__(self):
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        self.task_sets_root = project_root / "task-sets"
    def parse(self, distribution: str, util_level: float, csv_identifier: int) -> pd.DataFrame:
        distribution = distribution.lower()
        if distribution not in self.DISTRIBUTION_MAPPING:
            raise ValueError(
                f"Invalid distribution type: '{distribution}'. "
                f"Must be one of {list(self.DISTRIBUTION_MAPPING.keys())}"
            )

        dist_info = self.DISTRIBUTION_MAPPING[distribution]
        util_folder = f"{util_level:.2f}-util"
        csv_filename = f"{dist_info['prefix']}_{csv_identifier}.csv"

        # Construct the full path
        base_dir = (
            self.task_sets_root /
            'output' /
            dist_info['util_dist'] /
            dist_info['per_dist'] /
            self.CORES /
            self.TASKS /
            self.JITTER
        )

        tasksets_dir = base_dir / util_folder / 'tasksets'

        # Prefer exact filename if present, otherwise try to find any csv in the folder
        csv_path = tasksets_dir / csv_filename

        df = pd.read_csv(csv_path)

        df.attrs['distribution'] = distribution
        df.attrs['util_level'] = util_level
        df.attrs['csv_identifier'] = csv_identifier
        df.attrs['file_path'] = str(csv_path)

        df.rename(columns={
            'BCET': 'C_i_j_min',
            'WCET': 'C_i_j',
            'Period': 'T_i',
            'Deadline': 'D_i',
        }, inplace=True)

        # Add task_id if it doesn't exist
        if 'task_id' not in df.columns:
            df.insert(0, 'task_id', range(1, len(df) + 1))

        return df
    

if __name__ == '__main__':
    parser = TaskSetParser()

    util = 0.20
    distribution = 'automotive'
    distribution = 'uunifast'

    df = parser.parse(distribution, util, 1)
    print(df.head())

    # Add T_i and D_i of first row
    print(f"T_i: {df.loc[0, 'T_i']}, D_i: {df.loc[0, 'D_i']}: {df.loc[0, 'T_i'] + df.loc[0, 'D_i']}")

    
