"""Module with some tools for timing stuff."""
from datetime import timedelta


def est_runtime_delta(prog, cur_runtime) -> timedelta:
    """Estimate the remaining runtime as a timedelta function.
    Rounds up to make things look nicer.

    Args:
        prog (float): The current progress, between 0 and 1.
        cur_runtime (float): How long the process has been running.
    """
    return timedelta(seconds=round(est_runtime(prog, cur_runtime)))


def est_runtime(prog: float, cur_runtime: float) -> float:
    """Estimate the remaining runtime.

    Args:
        prog (float): The current progress, between 0 and 1.
        cur_runtime (float): How long the process has been running.
    """
    # Example:
    # 30 % progress, 10 seconds => 10 / 30 = 1/3 s per %.
    # Est.: 1/3 * 70 % = 23.3 s
    if prog == 0:
        # cannot do an estimate with 0 progressed time.
        return 0.0

    return (cur_runtime / prog) * (1.0 - prog)
