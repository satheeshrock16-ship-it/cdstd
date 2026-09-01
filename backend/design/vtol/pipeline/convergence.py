"""
Convergence and Iteration Tracking Subsystem for VTOL Multidisciplinary Design.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class IterationRecord:
    """
    State tracking record for a single sizing loop iteration.
    """
    iteration: int
    old_mtow: float
    new_mtow: float
    residual: float
    converged: bool


class VTOLConvergenceManager:
    """
    Evaluator responsible for tracking MTOW convergence across design iterations.
    """
    def __init__(self, tolerance: float = 0.01, max_iterations: int = 15) -> None:
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.history: list[IterationRecord] = []

    def evaluate_step(self, iteration: int, old_mtow: float, new_mtow: float) -> IterationRecord:
        """
        Evaluates convergence for the current iteration step and saves record in history.
        """
        residual = abs(new_mtow - old_mtow)
        converged = residual < self.tolerance
        record = IterationRecord(
            iteration=iteration,
            old_mtow=old_mtow,
            new_mtow=new_mtow,
            residual=residual,
            converged=converged
        )
        self.history.append(record)
        return record
