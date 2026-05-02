import pandas as pd
from pathlib import Path
from typing import Optional
import os


class Parser:

    def load_taskset_csv(self, relative_csv_path: str) -> pd.DataFrame:
        """
        Load ONE taskset CSV given a relative path (relative to main.py / project root),
        rename columns to internal names, and add csv_id.
        """
        rel_path = relative_csv_path.replace("/", "\\")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.normpath(os.path.join(script_dir, ".."))
        abs_path = os.path.normpath(os.path.join(project_root, rel_path))

        df = pd.read_csv(abs_path)

        # normalize headers (BCET/WCET/Period/Deadline -> C_i_min/C_i/T_i/D_i)
        self._rename_headers(df)

        if "csv_id" not in df.columns:
            df["csv_id"] = Path(rel_path).name

        return df
        
    def load_all_csvs_recursive(self, path: str) -> list[pd.DataFrame]:
            import os
            csvs = []
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.normpath(os.path.join(script_dir, ".."))
            search_dir = os.path.normpath(os.path.join(project_root, path))
            for root, dirs, files in os.walk(search_dir):
                for file_name in files:
                    csv_path = os.path.join(root, file_name)
                    csvs.append(csv_path)

            dfs = []
            for csv in csvs:
                df = pd.read_csv(csv)
                self._rename_headers(df)
                p = Path(csv)
                last = Path(*p.parts[-1:])
                df["csv_id"] = str(last)
                dfs.append(df)
            return dfs

    def _rename_headers(self, df:pd.DataFrame):
        df.rename(columns={
            'BCET': 'C_i_min',
            'WCET': 'C_i',
            'Period': 'T_i',
            'Deadline': 'D_i',
        }, inplace=True)

        df.insert(0, 'task_id', range(1, len(df) + 1))
        

        return df

if __name__ == '__main__':
    tasksetparser = Parser()
    dfs = tasksetparser.load_all_csvs_recursive("src/test_examples")
    for df in dfs:
        print(df.columns)
    

    
