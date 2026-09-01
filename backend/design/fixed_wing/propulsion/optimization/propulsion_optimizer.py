"""
Fixed-Wing Propulsion Optimization Engine

Subclasses OptimizerBase to orchestrate motor, propeller, ESC, and battery searches.
"""

from typing import List, Any
from backend.design.common.optimization.optimizer_base import OptimizerBase
from backend.design.common.optimization.optimization_context import OptimizationContext
from backend.design.common.optimization.optimization_candidate import OptimizationCandidate
from backend.design.fixed_wing.propulsion.optimization.models import PropulsionSpecification
from backend.design.fixed_wing.propulsion.optimization.result import PropulsionOptimizationResult
from backend.design.fixed_wing.propulsion.optimization.candidate_generator import GridSearchPropulsionCandidateGenerator
from backend.design.fixed_wing.propulsion.optimization.constraints import build_propulsion_constraints
from backend.design.fixed_wing.propulsion.optimization.objective_function import PropulsionObjectiveFunction


class PropulsionOptimizer(OptimizerBase):
    """
    Subsystem optimizer resolving the optimal electric motor, propeller, ESC,
    and battery pack using a deterministic grid search evaluated against
    the PropulsionEngine backend.
    """

    def __init__(self) -> None:
        super().__init__("PropulsionOptimizer")
        # Define objective scoring backend
        self.propulsion_objective = PropulsionObjectiveFunction()

        # Register physical and safety constraints
        for check in build_propulsion_constraints():
            self.constraints.add_constraint(check.__name__, check)

        # Register objectives in self.objective
        self.objective.add_objective(
            name="propulsion_score",
            score_fn=lambda cand, ctx: self.propulsion_objective.evaluate(cand, ctx),
            weight=1.0,
            minimize=False  # We want to maximize the fitness score
        )

    def optimize(self, context: OptimizationContext) -> PropulsionOptimizationResult:
        """Runs the optimization search and returns a typed result."""
        res = super().optimize(context)
        return PropulsionOptimizationResult(
            winning_candidate=res.winning_candidate,
            generated_specification=res.generated_specification,
            success=res.success,
            message=res.message,
            evaluated_count=res.evaluated_count,
            feasible_count=res.feasible_count,
            history=res.history,
            rejected_summary=res.rejected_summary,
            execution_time_seconds=res.execution_time_seconds,
            iteration_count=res.iteration_count,
            diagnostics=res.diagnostics,
        )

    # ------------------------------------------------------------------
    #  OptimizerBase lifecycle hooks
    # ------------------------------------------------------------------

    def generate_candidates(
        self, context: OptimizationContext
    ) -> List[OptimizationCandidate]:
        generator = GridSearchPropulsionCandidateGenerator()
        return generator.generate_candidates(context)

    def evaluate_candidate(
        self, candidate: OptimizationCandidate, context: OptimizationContext
    ) -> None:
        # Evaluation is handled dynamically on-demand during constraint checks
        pass

    def build_specification(
        self, candidate: OptimizationCandidate, context: OptimizationContext
    ) -> PropulsionSpecification:
        dv = candidate.design_variables
        derived = candidate.derived_variables

        # Extract values
        motor = dv["motor"]
        prop = dv["propeller"]
        esc = dv["esc"]
        batt = dv["battery"]

        # Re-extract positive score from objective scores dictionary
        pos_score = candidate.objective_scores.get("propulsion_score", 0.0)

        reasoning = (
            f"Selected optimal propulsion configuration: Motor={motor['name']} (KV={motor['kv']:.0f}), "
            f"Propeller={prop['name']}, ESC={esc['name']}, Battery={batt['name']}. "
            f"Cruise current draw: {derived.get('cruise_current_a', 0.0):.2f} A, "
            f"estimated flight time: {derived.get('estimated_flight_time_min', 0.0):.1f} min, "
            f"static thrust: {derived.get('static_thrust_n', 0.0):.1f} N. "
            f"Optimization Score: {pos_score:.4f}."
        )

        return PropulsionSpecification(
            motor_name=motor["name"],
            propeller_name=prop["name"],
            esc_name=esc["name"],
            battery_name=batt["name"],
            operating_voltage_v=round(batt["nominal_voltage_v"], 2),
            cruise_current_a=round(derived.get("cruise_current_a", 0.0), 2),
            max_climb_current_a=round(derived.get("climb_current_a", 0.0), 2),
            cell_count_s=batt["cell_count_s"],
            battery_capacity_mah=batt["capacity_mah"],
            battery_weight_g=round(batt["weight_g"], 1),
            total_propulsion_weight_g=round(derived.get("total_propulsion_weight_g", 0.0), 1),
            static_thrust_n=round(derived.get("static_thrust_n", 0.0), 2),
            cruise_thrust_n=round(derived.get("cruise_thrust_n", 0.0), 2),
            cruise_power_w=round(derived.get("cruise_power_w", 0.0), 1),
            takeoff_power_w=round(derived.get("takeoff_power_w", 0.0), 1),
            motor_efficiency=round(derived.get("motor_efficiency", 0.0), 3),
            propeller_efficiency=round(derived.get("propeller_efficiency", 0.0), 3),
            total_efficiency=round(derived.get("total_efficiency", 0.0), 3),
            estimated_flight_time_min=round(derived.get("estimated_flight_time_min", 0.0), 1),
            optimization_score=round(pos_score, 4),
            reasoning=reasoning,
        )
