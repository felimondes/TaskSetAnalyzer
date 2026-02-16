from abc import ABC, abstractmethod

class Scheduler(ABC):
    jobs = None
    tasks = None
    
    @abstractmethod
    def get_hyperperiod(self):
        pass
    
    @abstractmethod
    def get_next_task(self, current_time):
        pass

    @abstractmethod
    def execute_task(self, current_time):
        pass

    @abstractmethod
    def is_schedulable(self):
        pass

    @abstractmethod
    def set_tasks(self, tasks):
        pass
        

