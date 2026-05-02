import matplotlib.pyplot as plt
from typing import List, Tuple
from src.simulatorTool.simulator import TaskSetMetrics

#most of this is made with AI
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
    return sum(1 for _, v in values if v is not None and v > 0)


def plot_all_task_metrics(metrics: TaskSetMetrics) -> None:

    task_ids = list(metrics.job_response_times_by_task.keys())
    n_tasks = len(task_ids)

    x_positions = list(range(1, n_tasks + 1))

    # 🔹 Map task_id -> period
    task_periods = {
        row["task_id"]: row["T_i"]
        for _, row in metrics.task_set.iterrows()
    }

    avg_response = [
        _extract_avg(metrics.job_response_times_by_task[t])
        for t in task_ids
    ]

    worst_response = [
        _extract_max(metrics.job_response_times_by_task[t])
        for t in task_ids
    ]

    # 🔹 Normalized WCRT (R / T)
    normalized_wcrt = [
        (_extract_max(metrics.job_response_times_by_task[t]) / task_periods[t])
        if task_periods[t] > 0 else 0
        for t in task_ids
    ]

    deadline_misses = [
        _count_deadline_misses(metrics.job_lateness_by_task.get(t, []))
        for t in task_ids
    ]

    fig, axs = plt.subplots(1, 4, figsize=(24, 5))

    fig.suptitle(
        f"{metrics.task_set_name} - {metrics.algorithm}",
        fontsize=14
    )

    rotation = 45 if n_tasks > 10 else 0

    # # 1️⃣ Average Response Time
    # axs[0].bar(x_positions, avg_response)
    # axs[0].set_title("Average Response Time")
    # axs[0].set_xlabel("Tasks")
    # axs[0].set_ylabel("Time")
    # axs[0].set_xticks(x_positions)
    # axs[0].tick_params(axis="x", rotation=rotation)

    # 2️⃣ Worst-Case Response Time
    axs[1].bar(x_positions, worst_response)
    axs[1].set_title("Worst-Case Response Time")
    axs[1].set_xlabel("Tasks")
    axs[1].set_ylabel("Time")
    axs[1].set_xticks(x_positions)
    axs[1].tick_params(axis="x", rotation=rotation)

        # 4️⃣ Normalized WCRT (R / T)
    axs[2].bar(x_positions, normalized_wcrt)
    axs[2].set_title("Normalized WCRT (R / T)")
    axs[2].set_xlabel("Tasks")
    axs[2].set_ylabel("Ratio")
    axs[2].set_xticks(x_positions)
    axs[2].tick_params(axis="x", rotation=rotation)

    # # 3️⃣ Deadline Miss Count
    # axs[2].bar(x_positions, deadline_misses)
    # axs[2].set_title("Number of Deadline Misses")
    # axs[2].set_xlabel("Tasks")
    # axs[2].set_ylabel("Count")
    # axs[2].set_xticks(x_positions)
    # axs[2].tick_params(axis="x", rotation=rotation)



    # 🔥 Deadline line
    axs[3].axhline(1, linestyle="--")
    import os

    # Get directory of this file
    current_dir = os.path.dirname(__file__)

    # Create images folder path
    images_dir = os.path.join(current_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Build full file path
    filename = os.path.join(images_dir, f"{metrics.algorithm}.png")

    plt.savefig(filename, bbox_inches="tight", dpi=300)

    plt.tight_layout()
    plt.show()


    import matplotlib.pyplot as plt

def plot_wcrt_table(metrics):
    #made with AI :)
    task_ids = list(metrics.job_response_times_by_task.keys())

    # Map task_id -> period
    task_periods = {
        row["task_id"]: row["T_i"]
        for _, row in metrics.task_set.iterrows()
    }

    table_data = []

    for t in task_ids:
        values = metrics.job_response_times_by_task[t]
        numeric = [v for _, v in values if v is not None]

        if numeric:
            wcrt = max(numeric)
        else:
            wcrt = 0

        period = task_periods[t]
        normalized = wcrt / period if period > 0 else 0

        table_data.append([
            t,
            round(wcrt, 2),
            period,
            round(normalized, 3)
        ])

    # Column labels
    columns = ["Task", "WCRT", "Period", "R / T"]

    fig, ax = plt.subplots(figsize=(8, len(task_ids) * 0.5 + 1))
    ax.axis("off")

    table = ax.table(
        cellText=table_data,
        colLabels=columns,
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.title(f"WCRT Table - {metrics.algorithm}", pad=10)

    # 🔥 Save
    import os
    current_dir = os.path.dirname(__file__)
    images_dir = os.path.join(current_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    filename = os.path.join(
        images_dir,
        f"{metrics.task_set_name}_{metrics.algorithm}_table.png"
    )

    plt.savefig(filename, bbox_inches="tight", dpi=300)
    # plt.show()