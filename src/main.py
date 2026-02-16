from job import Job
from simulator import Simulator
from task_set_parser import TaskSetParser
from earliest_deadline_first import EDF

if __name__ == '__main__':
    taskSetParser = TaskSetParser()
    task_set = taskSetParser.parse('automotive', 0.50, 0)
    simulator = Simulator()

    for index, row in task_set.iterrows():
        job = Job(row)
        
    
    edf = EDF()

    print(edf.get_hyperperiod(task_set))

    simulator.run(task_set, edf)








