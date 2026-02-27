from simulator import Simulator
from parser import Parser
from earliest_deadline_first import EDF
from rate_monotonic import RateMonotonic
import numpy as np
import pandas as pd
from parser import Parser

sim = Simulator()
edf = EDF()
rm = RateMonotonic()
parser = Parser()

def run_simulations(dfs):
    for df in dfs: 
        wcet = True
        results = sim.start(df, edf, wcet)
        result = results.get("schedulable_analysis")
        print(f"scheudable? {result[0]}")

def main():

    not_sched = "easy_examples\\not_schedulable"
    sched = "easy_examples\schedulable"
    folders = [not_sched]
    
    for folder in folders:
        dfs = parser.taskSetParser(folder)
        run_simulations(dfs)
        
if __name__ == '__main__':
    main()

    

    

  










