import matplotlib.pyplot as plt
from typing import List, Tuple
from simulator import TaskSetMetrics


def _extract_avg(values: List[Tuple[str, float]]) -> float:
    numeric = [v for _, v in values if v is not None]
    if not numeric:
        return 0.0
    return sum(numeric) / len(numeric)


def _extract_max(values: List[Tuple[str, float]]) -> float:
    numeric = [v for _, v in values if v is not None]
    if not numeric:
        return 0.0
    return max(numeric)


def _count_deadline_misses(values: List[Tuple[str, float]]) -> int:
    """
    Count jobs with positive lateness (ignore negative values).
    """
    return sum(1 for _, v in values if v is not None and v > 0)


def plot_all_task_metrics(metrics: TaskSetMetrics) -> None:

    task_ids = list(metrics.job_response_times_by_task.keys())
    n_tasks = len(task_ids)

    x_positions = list(range(1, n_tasks + 1))

    avg_response = [
        _extract_avg(metrics.job_response_times_by_task[t])
        for t in task_ids
    ]

    worst_response = [
        _extract_max(metrics.job_response_times_by_task[t])
        for t in task_ids
    ]

    # 🔹 Count deadline misses instead of averaging lateness
    deadline_misses = [
        _count_deadline_misses(
            metrics.job_lateness_by_task.get(t, [])
        )
        for t in task_ids
    ]

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    fig.suptitle(
        f"{metrics.task_set_name} - {metrics.algorithm}",
        fontsize=14
    )

    rotation = 45 if n_tasks > 10 else 0

    # 1️⃣ Average Response Time
    axs[0].bar(x_positions, avg_response, color="steelblue")
    axs[0].set_title("Average Response Time")
    axs[0].set_xlabel("Tasks")
    axs[0].set_ylabel("Time")
    axs[0].set_xticks(x_positions)
    axs[0].tick_params(axis="x", rotation=rotation)

    # 2️⃣ Worst-Case Response Time
    axs[1].bar(x_positions, worst_response, color="darkorange")
    axs[1].set_title("Worst-Case Response Time")
    axs[1].set_xlabel("Tasks")
    axs[1].set_ylabel("Time")
    axs[1].set_xticks(x_positions)
    axs[1].tick_params(axis="x", rotation=rotation)

    # 3️⃣ Deadline Miss Count
    axs[2].bar(x_positions, deadline_misses, color="crimson")
    axs[2].set_title("Number of Deadline Misses")
    axs[2].set_xlabel("Tasks")
    axs[2].set_ylabel("Count")
    axs[2].set_xticks(x_positions)
    axs[2].tick_params(axis="x", rotation=rotation)

    plt.tight_layout()
    plt.show()