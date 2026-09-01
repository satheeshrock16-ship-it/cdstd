"""
VTOL Tail Sizing Result Subsystem

Purpose:
    Defines the consolidated `TailResult` dataclass outputted by the tail stage.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from backend.design.vtol.tail.tail_geometry import TailGeometry
from backend.design.vtol.tail.tail_structure import TailStructure
from backend.design.vtol.tail.tail_controls import TailControls
from backend.design.vtol.tail.tail_analysis import TailStabilityAnalysis, TailControlAnalysis


@dataclass(slots=True)
class TailResult:
    """
    Consolidated tail sizing package detailing geometry, controls, and stability.

    Attributes:
        tail_geometry (TailGeometry): Sized stabilizer areas and spans.
        tail_structure (TailStructure): Weight and boom dimensions.
        control_surfaces (TailControls): Sized elevators/rudders and mixing type.
        stability_analysis (TailStabilityAnalysis): static margins and G capability.
        control_analysis (TailControlAnalysis): Control effectiveness and wash effects.
        engineering_notes (List[str]): Sizing observations.
        recommendations (List[str]): Downstream recommendations.
        warnings (List[str]): Stability margin warnings.
        metadata (Dict[str, Any]): execution timestamps and versions.
    """

    tail_geometry: TailGeometry
    tail_structure: TailStructure
    control_surfaces: TailControls
    stability_analysis: TailStabilityAnalysis
    control_analysis: TailControlAnalysis
    engineering_notes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
