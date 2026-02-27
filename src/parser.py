import pandas as pd
from pathlib import Path
from typing import Optional



class Parser:

        
    def taskSetParser(self, path: str) -> pd.DataFrame:
            csvs = self._find_all_csvs_from_folder_relative_path(path)
            dfs = []
            for csv in csvs:
                df = pd.read_csv(csv)
                self._rename_headers(df)
                p = Path(csv)
                last_two = Path(*p.parts[-1:])
                df["csv_id"] = str(last_two)
                dfs.append(df)
            return dfs
    
    def _find_all_csvs_from_folder_relative_path(self, relative_path: str) -> list[str]:
        import os
        csvs = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        for root, dirs, files in os.walk(script_dir + "\\" + relative_path):
            for file_name in files:
                csv_path = root + "\\" + file_name
                csvs.append(csv_path)
        return csvs

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
    dfs = tasksetparser.taskSetParser("src/test_examples")
    for df in dfs:
        print(df.columns)
    

    
