"""Utilities function."""
import matplotlib.pyplot as plt


def plot_result(result, mode: str, metric: str) -> None:
    """Plot the results."""
    steps = (
        result.metrics[mode]["steps"] * result.info[mode]["x"]["alpha"]
        + result.info[mode]["x"]["beta"]
    )
    y_mean = (
        result.metrics[mode][f"{metric}_mean"] * result.info[mode]["y"]["alpha"]
        + result.info[mode]["y"]["beta"]
    )

    y_stderr = result.metrics[mode][f"{metric}_stderr"]

    plt.plot(steps, y_mean, label=result.label)

    plt.fill_between(steps, y_mean - y_stderr, y_mean + y_stderr, alpha=0.1)
