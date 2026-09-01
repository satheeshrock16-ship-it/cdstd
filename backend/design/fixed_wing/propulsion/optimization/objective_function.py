"""
Fixed-Wing Propulsion Sizing Objective Function

Calculates the overall optimization score based on efficiency, mass,
thrust margin, reliability, and flight endurance.
"""

from backend.design.common.optimization.optimization_context import OptimizationContext
from backend.design.common.optimization.optimization_candidate import OptimizationCandidate


class PropulsionObjectiveFunction:
    """Computes the overall optimization score for a propulsion candidate."""

    def __init__(self) -> None:
        self.weights = {
            "electrical_efficiency": 0.15,
            "weight": 0.15,
            "cruise_efficiency": 0.15,
            "takeoff_margin": 0.15,
            "endurance": 0.20,
            "reliability": 0.10,
            "future_upgrade_margin": 0.10,
        }

    def evaluate(self, candidate: OptimizationCandidate, context: OptimizationContext) -> float:
        """Evaluates the multi-objective score of the candidate."""
        if candidate.status == "FAILED" or not candidate.constraints_passed:
            candidate.overall_score = -999.0
            return -999.0

        dv = candidate.design_variables
        derived = candidate.derived_variables

        motor = dv["motor"]
        esc = dv["esc"]

        # 1. Electrical Efficiency
        total_eff = derived.get("total_efficiency", 0.50)
        score_eff = max(0.0, min(1.0, (total_eff - 0.35) / 0.35))

        # 2. Weight (minimize total mass)
        total_w = derived.get("total_propulsion_weight_g", 500.0)
        score_weight = max(0.0, min(1.0, 1.0 - (total_w / 4000.0)))

        # 3. Cruise Efficiency (minimize cruise power)
        cruise_pwr = derived.get("cruise_power_w", 200.0)
        score_cruise_pwr = max(0.0, min(1.0, 1.0 - (cruise_pwr / 2000.0)))

        # 4. Takeoff Margin (maximize thrust-to-weight ratio)
        static_thrust = derived.get("static_thrust_n", 10.0)
        req_thrust = derived.get("takeoff_thrust_n", 5.0)
        t_w_margin = static_thrust / max(1.0, req_thrust)
        score_takeoff = max(0.0, min(1.0, (t_w_margin - 1.0) / 1.5)) if t_w_margin >= 1.0 else 0.0

        # 5. Endurance (maximize estimated flight time)
        flight_time = derived.get("estimated_flight_time_min", 30.0)
        score_endur = max(0.0, min(1.0, flight_time / 180.0))

        # 6. Reliability (minimize climb current vs motor limit)
        climb_curr = derived.get("climb_current_a", 10.0)
        motor_max_curr = motor["max_current_a"]
        climb_current_ratio = climb_curr / max(1.0, motor_max_curr)
        score_rel = max(0.0, min(1.0, 1.0 - climb_current_ratio))

        # 7. Future Upgrade Margin (maximize ESC current headroom)
        esc_max_curr = esc["continuous_current_a"]
        esc_margin_ratio = climb_curr / max(1.0, esc_max_curr)
        score_esc_margin = max(0.0, min(1.0, 1.0 - esc_margin_ratio))

        # Adjust weights based on mission category (Mission Suitability)
        category = context.requirements.mission_result.mission_category
        cat_name = category.value if hasattr(category, 'value') else str(category)

        weights = self.weights.copy()
        if any(w in cat_name for w in ["Endurance", "Survey", "Mapping", "Agriculture"]):
            weights["endurance"] = 0.35
            weights["electrical_efficiency"] = 0.15
            weights["weight"] = 0.10
            weights["cruise_efficiency"] = 0.15
            weights["takeoff_margin"] = 0.05
        elif "Cargo" in cat_name:
            weights["takeoff_margin"] = 0.35
            weights["weight"] = 0.15
            weights["reliability"] = 0.15
            weights["endurance"] = 0.10
        elif "Racing" in cat_name:
            weights["takeoff_margin"] = 0.30
            weights["weight"] = 0.20
            weights["electrical_efficiency"] = 0.05
            weights["endurance"] = 0.05

        # Normalize weights
        total_weight_sum = sum(weights.values())
        for k in weights:
            weights[k] /= total_weight_sum

        # Calculate score
        score = (
            weights["electrical_efficiency"] * score_eff +
            weights["weight"] * score_weight +
            weights["cruise_efficiency"] * score_cruise_pwr +
            weights["takeoff_margin"] * score_takeoff +
            weights["endurance"] * score_endur +
            weights["reliability"] * score_rel +
            weights["future_upgrade_margin"] * score_esc_margin
        )

        candidate.objective_scores = {
            "electrical_efficiency": score_eff,
            "weight": score_weight,
            "cruise_efficiency": score_cruise_pwr,
            "takeoff_margin": score_takeoff,
            "endurance": score_endur,
            "reliability": score_rel,
            "future_upgrade_margin": score_esc_margin,
        }
        candidate.overall_score = score
        return score
