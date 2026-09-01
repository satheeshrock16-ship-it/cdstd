"""
Pipeline Result and Aircraft Specification Models for VTOL Design Execution.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

from backend.design.vtol.mission.mission_result import MissionResult
from backend.design.vtol.configuration.configuration_result import ConfigurationResult
from backend.design.vtol.wing.wing_result import WingResult
from backend.design.vtol.airfoil.airfoil_result import AirfoilResult
from backend.design.vtol.tail.tail_result import TailResult
from backend.design.vtol.fuselage.fuselage_result import FuselageResult
from backend.design.vtol.lift_system.lift_system_result import LiftSystemResult
from backend.design.vtol.forward_propulsion.forward_propulsion_result import ForwardPropulsionResult
from backend.design.vtol.electrical.electrical_result import ElectricalResult
from backend.design.vtol.avionics.avionics_result import AvionicsResult
from backend.design.vtol.payload.payload_result import PayloadResult
from backend.design.vtol.mass_properties.mass_result import MassResult
from backend.design.vtol.hover_performance.hover_result import HoverResult
from backend.design.vtol.transition.transition_result import TransitionResult
from backend.design.vtol.cruise_performance.cruise_result import CruiseResult
from backend.design.vtol.verification.verification_result import VerificationResult
from backend.design.vtol.cad.cad_result import CADResult
from backend.design.vtol.manufacturing.manufacturing_result import ManufacturingResult
from backend.design.vtol.report.report_result import ReportResult

from backend.design.vtol.pipeline.convergence import IterationRecord


class PipelineStatus(str, Enum):
    """Execution status codes for VTOL Design Pipeline."""
    SUCCESS = "SUCCESS"
    INVALID_REQUIREMENTS = "INVALID_REQUIREMENTS"
    CONFIGURATION_INFEASIBLE = "CONFIGURATION_INFEASIBLE"
    SIZING_INFEASIBLE = "SIZING_INFEASIBLE"
    CONVERGENCE_FAILED = "CONVERGENCE_FAILED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    
    # Phase 5B / Sizing error categories
    AIRFOIL_STRUCTURE_INCOMPATIBLE = "AIRFOIL_STRUCTURE_INCOMPATIBLE"
    PAYLOAD_INFEASIBLE = "PAYLOAD_INFEASIBLE"
    PROPULSION_INFEASIBLE = "PROPULSION_INFEASIBLE"
    BATTERY_INFEASIBLE = "BATTERY_INFEASIBLE"
    COMMUNICATION_INFEASIBLE = "COMMUNICATION_INFEASIBLE"
    COMPONENT_DATABASE_LIMITATION = "COMPONENT_DATABASE_LIMITATION"
    MTOW_LIMIT_EXCEEDED = "MTOW_LIMIT_EXCEEDED"
    STABILITY_INFEASIBLE = "STABILITY_INFEASIBLE"
    PERFORMANCE_INFEASIBLE = "PERFORMANCE_INFEASIBLE"
    INTERNAL_EXCEPTION = "INTERNAL_EXCEPTION"


@dataclass
class VTOLAircraftSpecification:
    """
    Comprehensive specification containing all design and analysis results for the VTOL.
    """
    # High-level outputs
    mtow_kg: float
    empty_weight_kg: float
    payload_weight_kg: float
    estimated_endurance_min: float
    estimated_range_km: float
    configuration_type: str

    # Subsystem Sizing Results
    mission: MissionResult
    configuration: ConfigurationResult
    wing: WingResult
    airfoil: AirfoilResult
    tail: TailResult
    fuselage: FuselageResult
    lift_system: LiftSystemResult
    forward_propulsion: ForwardPropulsionResult
    electrical: ElectricalResult
    avionics: AvionicsResult
    payload: PayloadResult
    mass_properties: MassResult
    hover_performance: HoverResult
    transition: TransitionResult
    cruise_performance: CruiseResult
    
    # Validation, CAD, and manufacturing outputs
    verification: Optional[VerificationResult] = None
    cad: Optional[CADResult] = None
    manufacturing: Optional[ManufacturingResult] = None
    report: Optional[ReportResult] = None


@dataclass
class VTOLDesignResult:
    """
    Consolidated response payload from the VTOL design synthesis orchestrator.
    """
    success: bool
    status: PipelineStatus
    iterations: int
    converged: bool

    convergence_history: List[IterationRecord] = field(default_factory=list)
    final_specification: Optional[VTOLAircraftSpecification] = None

    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
