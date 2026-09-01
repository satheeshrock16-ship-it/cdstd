from typing import List
from .transition_result import TransitionResult
from .transition_constraints import TransitionConstraints

class TransitionValidator:
    """
    Validates conversion parameters against stability limits.
    """
    @staticmethod
    def validate(result: TransitionResult, constraints: TransitionConstraints) -> List[str]:
        warnings = []

        # Check conversion speed
        v_conv = result.transition_analysis.conversion_speed_kmh
        if v_conv < constraints.min_conversion_speed_kmh or v_conv > constraints.max_conversion_speed_kmh:
            warnings.append(
                f"Sized transition conversion speed ({v_conv:.1f} km/h) "
                f"is outside safe boundaries ({constraints.min_conversion_speed_kmh:.1f} - {constraints.max_conversion_speed_kmh:.1f} km/h)"
            )

        # Check duration
        t_conv = result.transition_analysis.duration_s
        if t_conv > constraints.max_transition_duration_s:
            warnings.append(
                f"Transition conversion duration ({t_conv:.1f} s) "
                f"exceeds safety threshold ({constraints.max_transition_duration_s:.1f} s)"
            )

        # Check stability margin
        margin = result.stability_analysis.min_stability_margin
        if margin < constraints.min_stability_margin_transition:
            warnings.append(
                f"Minimum transition stability margin ({margin * 100.0:.1f}%) "
                f"is below safety threshold ({constraints.min_stability_margin_transition * 100.0:.1f}%)"
            )

        return warnings
