"""
VTOL Electrical result Subsystem

Purpose:
    Defines the consolidated `ElectricalResult` dataclass outputted by the electrical stage.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from backend.design.vtol.electrical.battery_pack import BatteryPack
from backend.design.vtol.electrical.power_distribution import PowerDistribution
from backend.design.vtol.electrical.power_budget import PowerBudget
from backend.design.vtol.electrical.electrical_analysis import ElectricalAnalysis
from backend.design.vtol.electrical.thermal_management import ThermalAnalysis
from backend.design.vtol.electrical.charging_system import ChargingAnalysis


@dataclass(slots=True)
class ElectricalResult:
    """
    Consolidated electrical sizing result package.

    Attributes:
        battery_selection (Dict[str, Any]): Sized cell chemistry profiles.
        battery_pack (BatteryPack): Cells configurations S/P, capacities, and weights.
        power_distribution (PowerDistribution): BECs and distribution rails.
        power_budget (PowerBudget): Subsystems power budgets.
        electrical_analysis (ElectricalAnalysis): Mission energy budgets.
        thermal_analysis (ThermalAnalysis): Heat generation and cooling requirements.
        charging_analysis (ChargingAnalysis): Charging times.
        engineering_notes (List[str]): Sizing observations.
        recommendations (List[str]): Downstream recommendations.
        warnings (List[str]): Safety/clearance warnings.
        metadata (Dict[str, Any]): execution timestamps.
    """

    battery_selection: Dict[str, Any]
    battery_pack: BatteryPack
    power_distribution: PowerDistribution
    power_budget: PowerBudget
    electrical_analysis: ElectricalAnalysis
    thermal_analysis: ThermalAnalysis
    charging_analysis: ChargingAnalysis
    engineering_notes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
