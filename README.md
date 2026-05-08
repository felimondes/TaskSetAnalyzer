To run this code:

- download the python libraries in requirements.txt
- run run.py to select between simulation or analysis tool.
  For the analysis tools all results are printed in the terminal.
  For the simulation tool task wise results are given in the terminal,
  while WCRTs for each job within task sets can be found in the src/images folder.

You can configure the simulation in the #SIMULATION PANEL in the top of main.py.

* Use flag "wcet" to toggle between WCET to varying execution time
* Use flag "isOnlyUnSchedulableTestCases" to only run unschedulable test cases. This will run 100 hyperperiods for each task set. This is important testing the simulation.

To change seed for the simulation tool change line 4 in job.py in the simulatorTool folder:
random.seed(42)
