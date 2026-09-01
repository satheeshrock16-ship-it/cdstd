"""
VTOL Electrical Validator Subsystem

Purpose:
    Defines the `ElectricalValidator` class checking capacities, current ratings,
    voltage matching, and safety reserves.
"""

from typing import List
from backend.design.vtol.electrical.electrical_requirements import ElectricalRequirements
from backend.design.vtol.electrical.electrical_result import ElectricalResult


class ElectricalValidationError(ValueError):
    """
    Exception raised when VTOL electrical sizing violates capacity or voltage safety limits.
    """

    def __init__(self, errors: List[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


class ElectricalValidator:
    """
    Validates sized battery packs and protection systems.
    """

    def validate(self, requirements: ElectricalRequirements, result: ElectricalResult) -> None:
        """
        Validates the electrical sizing results.

        Args:
            requirements (ElectricalRequirements): Inputs.
            result (ElectricalResult): Outputs.

        Raises:
            ElectricalValidationError: If rules are violated.
        """
        errors: List[str] = []

        if requirements is None:
            raise ElectricalValidationError(["Requirements object is null."])

        pack = result.battery_pack
        analysis = result.electrical_analysis
        power_budget = result.power_budget

        # 1. Battery capacity check
        # Sized reserve factor
        min_reserve = requirements.metadata.get("min_reserve_energy_fraction", 0.20)
        required_energy_reserve = analysis.mission_energy_wh * (1.0 + min_reserve)
        if pack.energy_wh < required_energy_reserve:
            errors.append(
                f"Battery capacity failure: sized battery energy ({pack.energy_wh:.1f} Wh) "
                f"is less than required energy budget with reserve limit ({required_energy_reserve:.1f} Wh)."
            )

        # 2. Peak current capability check
        # Peak current is drawn during hover vertical takeoff/landing stages
        hover_current = result.metadata.get("hover_current_draw_a", 0.0)
        if hover_current > pack.peak_current_limit_a:
            errors.append(
                f"Discharge capability violation: total hover current ({hover_current:.1f} A) "
                f"exceeds maximum battery pack peak current limit ({pack.peak_current_limit_a:.1f} A)."
            )

        # 3. Voltage compatibility check
        # check nominal voltages align with motor KV RPM limits
        if not (11.1 <= pack.nominal_voltage_v <= 60.0):
            errors.append(
                f"Voltage compatibility error: pack voltage ({pack.nominal_voltage_v:.1f} V) "
                f"is outside acceptable ESC limits (11.1V to 60.0V)."
            )

        if errors:
            raise ElectricalValidationError(errors)
