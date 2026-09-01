"""
Fixed-Wing Wing Planform Optimization Constraints

Enforces feasibility checks such as maximum wingspan, minimum chord sizes, and structural weight fractions.
"""

from backend.design.fixed_wing.wing.wing_result import WingResult
from backend.design.fixed_wing.optimization.optimization_models import PlanformCandidate

class OptimizationConstraints:
    """
    Checks that sized candidate designs comply with physical and optimization constraints.
    """
    def __init__(
        self,
        max_wingspan_m: float | None = None,
        min_chord_m: float = 0.05,
        max_wing_mass_fraction: float = 0.25
    ) -> None:
        self.max_wingspan_m = max_wingspan_m
        self.min_chord_m = min_chord_m
        self.max_wing_mass_fraction = max_wing_mass_fraction

    def check_constraints(self, candidate: PlanformCandidate, result: WingResult) -> tuple[bool, list[str]]:
        """
        Runs feasibility checks on a sized wing design.
        """
        violations = []
        geom = result.wing_geometry

        # 1. Wingspan check
        if self.max_wingspan_m is not None and geom.span_m > self.max_wingspan_m:
            violations.append(f"Wingspan {geom.span_m:.3f} m exceeds maximum limit {self.max_wingspan_m} m.")

        # 2. Chord limits
        if geom.root_chord_m < self.min_chord_m:
            violations.append(f"Root chord {geom.root_chord_m:.3f} m is below minimum limit {self.min_chord_m} m.")
        if geom.tip_chord_m < self.min_chord_m:
            violations.append(f"Tip chord {geom.tip_chord_m:.3f} m is below minimum limit {self.min_chord_m} m.")

        # 3. Wing weight fraction check
        mtow = 5.0
        wing_weight = 0.5
        for note in result.engineering_notes:
            if "Estimated MTOW:" in note:
                try:
                    mtow = float(note.split("Estimated MTOW:")[1].split("kg")[0].strip())
                except Exception:
                    pass
            elif "Estimated Wing weight:" in note:
                try:
                    wing_weight = float(note.split("Estimated Wing weight:")[1].split("kg")[0].strip())
                except Exception:
                    pass

        fraction = wing_weight / max(0.1, mtow)
        if fraction > self.max_wing_mass_fraction:
            violations.append(f"Wing weight fraction {fraction*100.0:.1f}% exceeds limit {self.max_wing_mass_fraction*100.0:.1f}%.")

        return len(violations) == 0, violations
