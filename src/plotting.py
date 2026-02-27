import matplotlib.pyplot as plt
from typing import List, Tuple
from simulator import TaskSetMetrics



def _extract_avg(values: List[Tuple[str, float]]) -> float:
    numeric = [v for _, v in values if v is not None]
    if not numeric:
        return 0.0
    return sum(numeric) / len(numeric)


def plot_average_response_times(metrics: TaskSetMetrics) -> None:
    """Plot average response time per task."""
    task_ids = []
    avg_response_times = []

    for task_id, values in metrics.job_response_times_by_task.items():
        task_ids.append(task_id)
        avg_response_times.append(_extract_avg(values))

    plt.figure()
    plt.bar(task_ids, avg_response_times)
    plt.title("Average Response Time per Task")
    plt.xlabel("Task ID")
    plt.ylabel("Average Response Time")
    plt.xticks(rotation=45)
    plt.show()


def plot_average_lateness(metrics: TaskSetMetrics) -> None:
    """Plot average lateness per task."""
    task_ids = []
    avg_lateness = []

    for task_id, values in metrics.job_lateness_by_task.items():
        task_ids.append(task_id)
        avg_lateness.append(_extract_avg(values))

    plt.figure()
    plt.bar(task_ids, avg_lateness)
    plt.title("Average Lateness per Task")
    plt.xlabel("Task ID")
    plt.ylabel("Average Lateness")
    plt.xticks(rotation=45)
    plt.show()


def plot_activation_completion_spread(metrics: TaskSetMetrics) -> None:
    """Plot average activation vs completion time per task."""
    task_ids = []
    avg_activation = []
    avg_completion = []

    for task_id in metrics.job_activation_times_by_task.keys():
        task_ids.append(task_id)
        avg_activation.append(
            _extract_avg(metrics.job_activation_times_by_task.get(task_id, []))
        )
        avg_completion.append(
            _extract_avg(metrics.job_completion_times_by_task.get(task_id, []))
        )

    plt.figure()
    plt.bar(task_ids, avg_activation)
    plt.title("Average Activation Time per Task")
    plt.xlabel("Task ID")
    plt.ylabel("Average Activation Time")
    plt.xticks(rotation=45)
    plt.show()

    plt.figure()
    plt.bar(task_ids, avg_completion)
    plt.title("Average Completion Time per Task")
    plt.xlabel("Task ID")
    plt.ylabel("Average Completion Time")
    plt.xticks(rotation=45)
    plt.show()