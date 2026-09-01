from dataclasses import dataclass, field
from typing import Any, Dict, List

from .weight_budget import WeightBudget
from .mass_distribution import MassDistribution
from .cg_analysis import CenterOfGravity, CGEnvelope
from .inertia_analysis import InertiaTensor
from .payload_shift_analysis import PayloadShiftAnalysis
from .battery_shift_analysis import BatteryShiftAnalysis
from .mass_properties_analysis import MassPropertiesAnalysis

@dataclass(slots=True)
class MassResult:
    """
    Consolidated output of the VTOL Mass Properties and Center of Gravity sizing.
    """
    weight_budget: WeightBudget
    mass_distribution: MassDistribution
    center_of_gravity: CenterOfGravity
    cg_envelope: CGEnvelope
    inertia_tensor: InertiaTensor
    payload_shift_analysis: PayloadShiftAnalysis
    battery_shift_analysis: BatteryShiftAnalysis
    mass_analysis: MassPropertiesAnalysis

    engineering_notes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
