To run this code: (this runs all test cases in the test_examples folder).

- download the python libraries in requirements.txt
- run run.py to select between simulation or analysis tool.
  For the analysis tools all results are printed in the terminal.
  For the simulation tool task wise results are given in the terminal,
  while WCRTs for each job within task sets can be found in the src/images folder.

To find WCRT for EDF and RM using the simulation tool:

Change the wcet flag in main.py line 16 to true:
wcet = False

This makes the simulation tool run with only wcet instead of varying times.

To change seed for the simulation tool change line 4 in job.py in the simulatorTool folder:
random.seed(42)
