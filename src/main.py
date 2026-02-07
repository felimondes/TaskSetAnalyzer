from src.task_set_parser import TaskSetParser


if __name__ == '__main__':
    parser = TaskSetParser()
    task_set = parser.parse_task_set('automotive', 0.50, 0)
    print(task_set)






