"""
VTOL Sizing and Multidisciplinary Design Synthesis Orchestrator.
"""

import logging
import os
import json
import csv
from typing import Optional, List, Dict, Any

from backend.design.common.requirements.requirement_model import RequirementModel
from backend.design.common.validation.requirement_validator import RequirementValidator
from backend.design.common.requirements.mission_type import MissionType
from backend.design.common.requirements.aircraft_type import AircraftType
from backend.design.common.requirements.takeoff_type import TakeoffType
from backend.design.common.requirements.landing_type import LandingType
from backend.design.common.requirements.operating_environment import OperatingEnvironment
from backend.design.router.design_engine import DesignEngine
from backend.design.common.context.design_context import DesignContext
from backend.design.common.context.design_stage import DesignStage
from backend.design.common.context.design_status import DesignStatus

# VTOL Stage requirements & engines
from backend.design.vtol.mission.mission_requirements import (
    MissionRequirements,
    VTOLMissionCategory,
    VTOLType,
    TakeoffMethod,
    LandingMethod,
    EnvironmentType,
    AutonomyLevel,
)
from backend.design.vtol.mission.hover_requirements import HoverRequirements as MissionHoverReq
from backend.design.vtol.mission.transition_requirements import TransitionRequirements as MissionTransReq
from backend.design.vtol.mission.cruise_requirements import CruiseRequirements as MissionCruiseReq
from backend.design.vtol.mission.mission_engine import MissionEngine

from backend.design.vtol.configuration.configuration_requirements import ConfigurationRequirements
from backend.design.vtol.configuration.configuration_engine import ConfigurationEngine
from backend.design.vtol.configuration.configuration_validator import ConfigurationValidationError

from backend.design.vtol.wing.wing_requirements import WingRequirements
from backend.design.vtol.wing.wing_engine import WingEngine
from backend.design.vtol.wing.wing_validator import WingValidationError

from backend.design.vtol.airfoil.airfoil_requirements import AirfoilRequirements
from backend.design.vtol.airfoil.airfoil_engine import AirfoilEngine
from backend.design.vtol.airfoil.airfoil_validator import AirfoilValidationError

from backend.design.vtol.tail.tail_requirements import TailRequirements
from backend.design.vtol.tail.tail_engine import TailEngine
from backend.design.vtol.tail.tail_validator import TailValidationError

from backend.design.vtol.fuselage.fuselage_requirements import FuselageRequirements
from backend.design.vtol.fuselage.fuselage_engine import FuselageEngine
from backend.design.vtol.fuselage.fuselage_validator import FuselageValidationError

from backend.design.vtol.lift_system.lift_system_requirements import LiftSystemRequirements
from backend.design.vtol.lift_system.lift_system_engine import LiftSystemEngine
from backend.design.vtol.lift_system.lift_system_validator import LiftSystemValidationError

from backend.design.vtol.forward_propulsion.forward_propulsion_requirements import ForwardPropulsionRequirements
from backend.design.vtol.forward_propulsion.forward_propulsion_engine import ForwardPropulsionEngine
from backend.design.vtol.forward_propulsion.forward_propulsion_validator import ForwardPropulsionValidationError

from backend.design.vtol.electrical.electrical_requirements import ElectricalRequirements
from backend.design.vtol.electrical.electrical_engine import ElectricalEngine
from backend.design.vtol.electrical.electrical_validator import ElectricalValidationError

from backend.design.vtol.avionics.avionics_requirements import AvionicsRequirements
from backend.design.vtol.avionics.avionics_engine import AvionicsEngine

from backend.design.vtol.payload.payload_requirements import PayloadRequirements
from backend.design.vtol.payload.payload_engine import PayloadEngine

from backend.design.vtol.mass_properties.mass_requirements import MassRequirements
from backend.design.vtol.mass_properties.mass_properties_engine import MassPropertiesEngine

from backend.design.vtol.hover_performance.hover_requirements import HoverRequirements as HPRequirements
from backend.design.vtol.hover_performance.hover_engine import HoverPerformanceEngine

from backend.design.vtol.transition.transition_requirements import TransitionRequirements as TransRequirements
from backend.design.vtol.transition.transition_engine import TransitionFlightEngine

from backend.design.vtol.cruise_performance.cruise_requirements import CruiseRequirements as CruiseReqs
from backend.design.vtol.cruise_performance.cruise_engine import CruisePerformanceEngine

from backend.design.vtol.optimization.optimization_requirements import OptimizationRequirements
from backend.design.vtol.optimization.optimization_engine import OptimizationEngine

from backend.design.vtol.verification.verification_requirements import VerificationRequirements
from backend.design.vtol.verification.verification_engine import VTOLVerificationEngine

from backend.design.vtol.cad.cad_requirements import CADRequirements
from backend.design.vtol.cad.cad_engine import VTOLCADEngine

from backend.design.vtol.manufacturing.manufacturing_requirements import ManufacturingRequirements
from backend.design.vtol.manufacturing.manufacturing_engine import VTOLManufacturingEngine

from backend.design.vtol.report.report_requirements import ReportRequirements
from backend.design.vtol.report.report_engine import VTOLReportEngine

# Pipeline models
from backend.design.vtol.pipeline.pipeline_result import VTOLDesignResult, VTOLAircraftSpecification, PipelineStatus
from backend.design.vtol.pipeline.convergence import VTOLConvergenceManager

logger = logging.getLogger(__name__)


class VTOLDesignPipeline:
    """
    Multidisciplinary VTOL Aircraft Synthesis Orchestrator.
    """
    def __init__(
        self,
        tolerance: float = 0.01,
        max_iterations: int = 15,
        raise_on_failure: bool = False,
    ) -> None:
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.raise_on_failure = raise_on_failure

        # Initialize individual stage sizers
        self._req_validator = RequirementValidator()
        self._mission_engine = MissionEngine()
        self._configuration_engine = ConfigurationEngine()
        self._wing_engine = WingEngine()
        self._airfoil_engine = AirfoilEngine()
        self._tail_engine = TailEngine()
        self._fuselage_engine = FuselageEngine()
        self._lift_engine = LiftSystemEngine()
        self._fwd_engine = ForwardPropulsionEngine()
        self._elec_engine = ElectricalEngine()
        self._avionics_engine = AvionicsEngine()
        self._payload_engine = PayloadEngine()
        self._mass_engine = MassPropertiesEngine()
        self._hover_engine = HoverPerformanceEngine()
        self._trans_engine = TransitionFlightEngine()
        self._cruise_engine = CruisePerformanceEngine()
        self._opt_engine = OptimizationEngine()
        self._verif_engine = VTOLVerificationEngine()
        self._cad_engine = VTOLCADEngine()
        self._mfg_engine = VTOLManufacturingEngine()
        self._report_engine = VTOLReportEngine()

    def execute(self, requirements: RequirementModel) -> VTOLDesignResult:
        """
        Runs the complete end-to-end design synthesis loop.
        """
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Input Requirements Validation
        if requirements is None or requirements.payload_weight_kg <= 0.0 or requirements.target_range_km <= 0.0 or requirements.target_flight_time_min <= 0.0:
            err_msg = "Invalid requirement parameters: payload, range, and endurance must be positive."
            errors.append(err_msg)
            return VTOLDesignResult(success=False, status=PipelineStatus.INVALID_REQUIREMENTS, iterations=0, converged=False, errors=errors)

        try:
            val_res = self._req_validator.validate(requirements)
            if hasattr(val_res, "is_valid") and not val_res.is_valid:
                err_msg = f"Requirements validation failed: {getattr(val_res, 'errors', [])}"
                errors.append(err_msg)
                return VTOLDesignResult(success=False, status=PipelineStatus.INVALID_REQUIREMENTS, iterations=0, converged=False, errors=errors)
        except Exception as e:
            errors.append(f"Validation error: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.INVALID_REQUIREMENTS, iterations=0, converged=False, errors=errors)

        # 2. Mission Requirements Translation
        try:
            mission_reqs = self._translate_requirements(requirements)
            mission_res = self._mission_engine.process_mission(mission_reqs)
        except Exception as e:
            errors.append(f"Mission compilation failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.INVALID_REQUIREMENTS, iterations=0, converged=False, errors=errors)

        # 3. VTOL Configuration selection (Frozen configuration layout)
        try:
            config_reqs = ConfigurationRequirements(mission_result=mission_res)
            config_res = self._configuration_engine.design_configuration(config_reqs)
        except (ConfigurationValidationError, Exception) as e:
            errors.append(f"Configuration selection failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.CONFIGURATION_INFEASIBLE, iterations=0, converged=False, errors=errors)

        # 4. Sizing Loop setup
        initial_mtow = requirements.maximum_takeoff_weight_kg
        if initial_mtow is None or initial_mtow <= 0.0:
            initial_mtow = max(2.0, requirements.payload_weight_kg * 3.0)

        current_mtow = initial_mtow
        conv_mgr = VTOLConvergenceManager(tolerance=self.tolerance, max_iterations=self.max_iterations)
        
        iteration = 0
        converged = False
        status = PipelineStatus.SUCCESS

        wing_res = None
        airfoil_res = None
        tail_res = None
        fuselage_res = None
        lift_res = None
        fwd_res = None
        elec_res = None
        avionics_res = None
        payload_res = None
        mass_res = None
        hover_res = None
        trans_res = None
        cruise_res = None

        # 5. Multidisciplinary Sizing Convergence Loop
        while iteration < self.max_iterations and not converged:
            iteration += 1
            old_mtow = current_mtow
            mission_res.mission_analysis.estimated_mtow_kg = old_mtow

            try:
                meta = requirements.metadata or {}
                # A. Wing Sizing
                wing_reqs = WingRequirements(mission_result=mission_res, configuration_result=config_res, metadata=meta)
                wing_res = self._wing_engine.size_wing_system(wing_reqs)

                # B. Airfoil Sizing
                airfoil_reqs = AirfoilRequirements(mission_result=mission_res, configuration_result=config_res, wing_result=wing_res, metadata=meta)
                airfoil_res = self._airfoil_engine.design_airfoil(airfoil_reqs)

                # C. Tail Sizing (Must run before Fuselage because Fuselage depends on Tail)
                tail_reqs = TailRequirements(mission_result=mission_res, configuration_result=config_res, wing_result=wing_res, airfoil_result=airfoil_res, metadata=meta)
                tail_res = self._tail_engine.size_tail_system(tail_reqs)

                # D. Fuselage Sizing
                fuselage_reqs = FuselageRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    metadata=meta
                )
                fuselage_res = self._fuselage_engine.design_fuselage(fuselage_reqs)

                # E. Lift System Sizing
                lift_reqs = LiftSystemRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    metadata=meta
                )
                lift_res = self._lift_engine.design_lift_system(lift_reqs)

                # F. Forward Propulsion Sizing
                fwd_reqs = ForwardPropulsionRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    metadata=meta
                )
                fwd_res = self._fwd_engine.design_forward_propulsion(fwd_reqs)

                # G. Electrical Sizing
                elec_reqs = ElectricalRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    metadata=meta
                )
                elec_res = self._elec_engine.design_electrical_system(elec_reqs)
                from backend.design.vtol.electrical.electrical_validator import ElectricalValidator
                ElectricalValidator().validate(elec_reqs, elec_res)

                # H. Avionics Sizing
                avionics_reqs = AvionicsRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    electrical_result=elec_res,
                    metadata=meta
                )
                avionics_res = self._avionics_engine.design(avionics_reqs)

                # I. Payload Sizing
                payload_reqs = PayloadRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    electrical_result=elec_res,
                    avionics_result=avionics_res,
                    metadata=meta
                )
                payload_res = self._payload_engine.design(payload_reqs)

                # J. Mass Properties Sizing
                mass_reqs = MassRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    electrical_result=elec_res,
                    avionics_result=avionics_res,
                    payload_result=payload_res,
                    metadata=meta
                )
                mass_res = self._mass_engine.design(mass_reqs)

                # K. Hover Performance Sizing
                hover_reqs = HPRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    electrical_result=elec_res,
                    avionics_result=avionics_res,
                    payload_result=payload_res,
                    mass_properties_result=mass_res
                )
                hover_res = self._hover_engine.design(hover_reqs)

                # L. Transition Sizing
                trans_reqs = TransRequirements(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    electrical_result=elec_res,
                    avionics_result=avionics_res,
                    payload_result=payload_res,
                    mass_properties_result=mass_res,
                    hover_performance_result=hover_res
                )
                trans_res = self._trans_engine.design(trans_reqs)

                # M. Cruise Performance Sizing
                cruise_reqs = CruiseReqs(
                    mission_result=mission_res,
                    configuration_result=config_res,
                    wing_result=wing_res,
                    airfoil_result=airfoil_res,
                    tail_result=tail_res,
                    fuselage_result=fuselage_res,
                    lift_system_result=lift_res,
                    forward_propulsion_result=fwd_res,
                    electrical_result=elec_res,
                    avionics_result=avionics_res,
                    payload_result=payload_res,
                    mass_properties_result=mass_res,
                    hover_performance_result=hover_res,
                    transition_result=trans_res
                )
                cruise_res = self._cruise_engine.design(cruise_reqs)

            except AirfoilValidationError as e:
                errors.append(f"Airfoil validation failed: {e}")
                return VTOLDesignResult(success=False, status=PipelineStatus.AIRFOIL_STRUCTURE_INCOMPATIBLE, iterations=iteration, converged=False, errors=errors)
            except (LiftSystemValidationError, ForwardPropulsionValidationError) as e:
                errors.append(f"Propulsion layout failed constraints: {e}")
                return VTOLDesignResult(success=False, status=PipelineStatus.PROPULSION_INFEASIBLE, iterations=iteration, converged=False, errors=errors)
            except ElectricalValidationError as e:
                errors.append(f"Electrical integration limit exceeded: {e}")
                return VTOLDesignResult(success=False, status=PipelineStatus.BATTERY_INFEASIBLE, iterations=iteration, converged=False, errors=errors)
            except (WingValidationError, TailValidationError, FuselageValidationError, Exception) as e:
                errors.append(f"Sizing loop failure at iteration {iteration}: {e}")
                return VTOLDesignResult(success=False, status=PipelineStatus.SIZING_INFEASIBLE, iterations=iteration, converged=False, errors=errors)

            # Check convergence limit
            raw_new_mtow = mass_res.weight_budget.max_takeoff_weight_kg
            relaxed_mtow = 0.75 * raw_new_mtow + 0.25 * old_mtow
            current_mtow = relaxed_mtow
            
            step_record = conv_mgr.evaluate_step(iteration, old_mtow, relaxed_mtow)
            converged = step_record.converged

        # 6. Sizing Convergence failure verification
        if not converged:
            errors.append("Aircraft sizing convergence failed: maximum iterations limit reached.")
            return VTOLDesignResult(success=False, status=PipelineStatus.CONVERGENCE_FAILED, iterations=iteration, converged=False, errors=errors)

        # 7. Verification stage execution
        try:
            verif_reqs = VerificationRequirements(
                mission_result=mission_res,
                configuration_result=config_res,
                wing_result=wing_res,
                airfoil_result=airfoil_res,
                tail_result=tail_res,
                fuselage_result=fuselage_res,
                lift_system_result=lift_res,
                forward_propulsion_result=fwd_res,
                electrical_result=elec_res,
                avionics_result=avionics_res,
                payload_result=payload_res,
                mass_properties_result=mass_res,
                hover_performance_result=hover_res,
                transition_result=trans_res,
                cruise_performance_result=cruise_res
            )
            verif_res = self._verif_engine.design(verif_reqs)
            if hasattr(verif_res, "warnings") and any("compliance" in w.lower() for w in verif_res.warnings):
                warnings.extend(verif_res.warnings)
        except Exception as e:
            errors.append(f"Verification engine failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.VERIFICATION_FAILED, iterations=iteration, converged=True, errors=errors)

        # 8. Optimization stage execution
        try:
            opt_reqs = OptimizationRequirements(
                mission_result=mission_res,
                configuration_result=config_res,
                wing_result=wing_res,
                airfoil_result=airfoil_res,
                tail_result=tail_res,
                fuselage_result=fuselage_res,
                lift_system_result=lift_res,
                forward_propulsion_result=fwd_res,
                electrical_result=elec_res,
                avionics_result=avionics_res,
                payload_result=payload_res,
                mass_properties_result=mass_res,
                hover_performance_result=hover_res,
                transition_result=trans_res,
                cruise_performance_result=cruise_res,
                verification_result=verif_res
            )
            opt_res = self._opt_engine.design(opt_reqs)
        except Exception as e:
            errors.append(f"Optimization engine failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.SIZING_INFEASIBLE, iterations=iteration, converged=True, errors=errors)

        # 9. CAD generation
        try:
            cad_reqs = CADRequirements(
                mission_result=mission_res,
                configuration_result=config_res,
                wing_result=wing_res,
                airfoil_result=airfoil_res,
                tail_result=tail_res,
                fuselage_result=fuselage_res,
                lift_system_result=lift_res,
                forward_propulsion_result=fwd_res,
                electrical_result=elec_res,
                avionics_result=avionics_res,
                payload_result=payload_res,
                mass_properties_result=mass_res,
                hover_performance_result=hover_res,
                transition_result=trans_res,
                cruise_performance_result=cruise_res,
                verification_result=verif_res,
                optimization_result=opt_res
            )
            cad_res = self._cad_engine.design(cad_reqs)
        except Exception as e:
            errors.append(f"CAD generation failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.SIZING_INFEASIBLE, iterations=iteration, converged=True, errors=errors)

        # 10. Manufacturing package compilation
        try:
            mfg_reqs = ManufacturingRequirements(
                mission_result=mission_res,
                configuration_result=config_res,
                wing_result=wing_res,
                airfoil_result=airfoil_res,
                tail_result=tail_res,
                fuselage_result=fuselage_res,
                lift_system_result=lift_res,
                forward_propulsion_result=fwd_res,
                electrical_result=elec_res,
                avionics_result=avionics_res,
                payload_result=payload_res,
                mass_properties_result=mass_res,
                hover_performance_result=hover_res,
                transition_result=trans_res,
                cruise_performance_result=cruise_res,
                verification_result=verif_res,
                optimization_result=opt_res,
                cad_result=cad_res
            )
            mfg_res = self._mfg_engine.design(mfg_reqs)
        except Exception as e:
            errors.append(f"Manufacturing compiler failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.SIZING_INFEASIBLE, iterations=iteration, converged=True, errors=errors)

        # 11. Report Sheet Generation
        try:
            rep_reqs = ReportRequirements(
                mission_result=mission_res,
                configuration_result=config_res,
                wing_result=wing_res,
                airfoil_result=airfoil_res,
                tail_result=tail_res,
                fuselage_result=fuselage_res,
                lift_system_result=lift_res,
                forward_propulsion_result=fwd_res,
                electrical_result=elec_res,
                avionics_result=avionics_res,
                payload_result=payload_res,
                mass_properties_result=mass_res,
                hover_performance_result=hover_res,
                transition_result=trans_res,
                cruise_performance_result=cruise_res,
                verification_result=verif_res,
                optimization_result=opt_res,
                cad_result=cad_res,
                manufacturing_result=mfg_res
            )
            rep_res = self._report_engine.design(rep_reqs)
        except Exception as e:
            errors.append(f"Report sheet compiler failed: {e}")
            return VTOLDesignResult(success=False, status=PipelineStatus.SIZING_INFEASIBLE, iterations=iteration, converged=True, errors=errors)

        # 12. VTOL Specification Assembly
        spec = VTOLAircraftSpecification(
            mtow_kg=round(current_mtow, 3),
            empty_weight_kg=round(mass_res.weight_budget.empty_weight_kg, 3),
            payload_weight_kg=round(requirements.payload_weight_kg, 2),
            estimated_endurance_min=round(cruise_res.cruise_analysis.endurance_min, 1),
            estimated_range_km=round(cruise_res.cruise_analysis.range_km, 2),
            configuration_type=config_res.selected_configuration.value,
            mission=mission_res,
            configuration=config_res,
            wing=wing_res,
            airfoil=airfoil_res,
            tail=tail_res,
            fuselage=fuselage_res,
            lift_system=lift_res,
            forward_propulsion=fwd_res,
            electrical=elec_res,
            avionics=avionics_res,
            payload=payload_res,
            mass_properties=mass_res,
            hover_performance=hover_res,
            transition=trans_res,
            cruise_performance=cruise_res,
            verification=verif_res,
            cad=cad_res,
            manufacturing=mfg_res,
            report=rep_res
        )

        # 13. Exporter to reports directory
        self._write_reports(spec)

        return VTOLDesignResult(
            success=True,
            status=PipelineStatus.SUCCESS,
            iterations=iteration,
            converged=True,
            convergence_history=conv_mgr.history,
            final_specification=spec,
            warnings=warnings,
            errors=errors
        )

    def _translate_requirements(self, req: RequirementModel) -> MissionRequirements:
        """
        Translates the canonical requirement model to the VTOL mission requirements.
        """
        cat_mapping = {
            MissionType.MAPPING: VTOLMissionCategory.MAPPING,
            MissionType.SURVEY: VTOLMissionCategory.SURVEY,
            MissionType.INSPECTION: VTOLMissionCategory.INSPECTION,
            MissionType.DELIVERY: VTOLMissionCategory.DELIVERY,
            MissionType.AGRICULTURE: VTOLMissionCategory.AGRICULTURE,
        }
        category = cat_mapping.get(req.mission_type, VTOLMissionCategory.SURVEY)

        vtype = VTOLType.LIFT_CRUISE
        if req.metadata and "preferred_vtol_type" in req.metadata:
            vt_str = req.metadata["preferred_vtol_type"]
            for vt in VTOLType:
                if vt.value.lower() == vt_str.lower() or vt.name.lower() == vt_str.lower():
                    vtype = vt
                    break

        meta = req.metadata or {}
        hover = MissionHoverReq(
            hover_duration_min=meta.get("hover_duration_min", 5.0),
            hover_altitude_m=meta.get("hover_altitude_m", 100.0),
            wind_limit_hover_kts=meta.get("wind_limit_hover_kts", 15.0),
            climb_rate_vertical_m_s=meta.get("climb_rate_vertical_m_s", 2.5),
            descent_rate_vertical_m_s=meta.get("descent_rate_vertical_m_s", 2.0)
        )

        transition = MissionTransReq(
            transition_speed_kmh=meta.get("transition_speed_kmh", 65.0),
            transition_duration_s=meta.get("transition_duration_s", 15.0),
            transition_altitude_m=meta.get("transition_altitude_m", 120.0),
            max_transition_pitch_deg=meta.get("max_transition_pitch_deg", 20.0)
        )

        cruise = MissionCruiseReq(
            cruise_speed_kmh=req.cruise_speed_kmh,
            cruise_altitude_m=meta.get("cruise_altitude_m", 150.0),
            cruise_range_km=req.target_range_km,
            cruise_endurance_min=req.target_flight_time_min,
            wind_limit_cruise_kts=meta.get("wind_limit_cruise_kts", 20.0)
        )

        takeoff_m = TakeoffMethod.VERTICAL
        if req.takeoff_type == TakeoffType.RUNWAY:
            takeoff_m = TakeoffMethod.RUNWAY

        landing_m = LandingMethod.VERTICAL
        if req.landing_type == LandingType.RUNWAY:
            landing_m = LandingMethod.RUNWAY

        env = EnvironmentType.RURAL
        if req.environment == OperatingEnvironment.URBAN:
            env = EnvironmentType.URBAN

        autonomy = meta.get("autonomy_level", AutonomyLevel.FULLY_AUTONOMOUS)
        if isinstance(autonomy, str):
            for au in AutonomyLevel:
                if au.value.lower() == autonomy.lower() or au.name.lower() == autonomy.lower():
                    autonomy = au
                    break

        return MissionRequirements(
            mission_category=category,
            vtol_type=vtype,
            payload_kg=req.payload_weight_kg,
            hover_reqs=hover,
            transition_reqs=transition,
            cruise_reqs=cruise,
            max_altitude_m=meta.get("max_altitude_m", 1000.0),
            environment=env,
            takeoff_method=takeoff_m,
            landing_method=landing_m,
            wind_limit_max_kts=meta.get("wind_limit_max_kts", 22.0),
            temperature_limit_min_c=meta.get("temperature_limit_min_c", -10.0),
            temperature_limit_max_c=meta.get("temperature_limit_max_c", 40.0),
            rain_tolerance=meta.get("rain_tolerance", "Light"),
            autonomy_level=autonomy,
            safety_requirements=meta.get("safety_requirements", "Dual GNSS and parachute backup"),
            budget=req.budget,
            manufacturing_preference=meta.get("manufacturing_preference", "Composite"),
            metadata=meta
        )

    def _write_reports(self, spec: VTOLAircraftSpecification) -> None:
        """Writes reporting sheets to workspace reports directory."""
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)

        # 1. Spec JSON
        json_data = {
            "mtow_kg": spec.mtow_kg,
            "empty_weight_kg": spec.empty_weight_kg,
            "payload_weight_kg": spec.payload_weight_kg,
            "endurance_min": spec.estimated_endurance_min,
            "range_km": spec.estimated_range_km,
            "configuration_type": spec.configuration_type,
            "subsystems": {
                "wing": {
                    "span_m": spec.wing.wing_geometry.span_m,
                    "area_m2": spec.wing.wing_geometry.area_m2,
                },
                "lift_system": spec.lift_system.lift_motor_selection,
                "forward_propulsion": spec.forward_propulsion.motor_selection,
                "battery": {
                    "chemistry": spec.electrical.battery_pack.chemistry,
                    "series_count": spec.electrical.battery_pack.series_count_s,
                    "parallel_count": spec.electrical.battery_pack.parallel_count_p,
                }
            }
        }
        with open(os.path.join(reports_dir, "vtol_specification.json"), "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)

        # 2. CSV BOM
        with open(os.path.join(reports_dir, "vtol_bom.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Subsystem", "Component Model / Description", "Mass (kg)", "Key Sizing Metric"])
            writer.writerow(["Wing Structure", "Sized Wing planform", spec.wing.wing_structure.estimated_wing_weight_kg, f"Span: {spec.wing.wing_geometry.span_m:.2f}m"])
            writer.writerow(["Tail Structure", spec.tail.tail_structure.structural_concept, spec.tail.tail_structure.estimated_tail_weight_kg, f"Horizontal Area: {spec.tail.tail_geometry.horizontal_area_m2:.3f}m2"])
            writer.writerow(["Fuselage Structure", spec.fuselage.fuselage_geometry.fuselage_type, 0.0, f"Volume: {spec.fuselage.fuselage_geometry.volume_m3:.3f}m3"])
            writer.writerow(["Lift Motor", spec.lift_system.lift_motor_selection.get("name", "Unknown"), 0.0, f"Disk Loading: {spec.lift_system.engineering_analysis.disk_loading_n_m2:.1f} N/m2"])
            writer.writerow(["Forward Motor", spec.forward_propulsion.motor_selection.get("name", "Unknown"), 0.0, f"Cruise range margin: {spec.forward_propulsion.performance_analysis.cruise_range_margin_km:.1f} km"])
            writer.writerow(["Battery Pack", spec.electrical.battery_pack.chemistry, spec.electrical.battery_pack.mass_kg, f"Energy: {spec.electrical.battery_pack.energy_wh:.1f} Wh"])
            writer.writerow(["Avionics", spec.avionics.flight_controller.name, 0.0, f"Redundancy level: {spec.avionics.flight_controller.redundancy_level}"])
            writer.writerow(["Payload", spec.payload.payload_selection.name, spec.payload.payload_selection.weight_kg, f"Mount: {spec.payload.payload_mount.mount_type}"])

        # 3. Build Spec TXT
        with open(os.path.join(reports_dir, "vtol_build_specification.txt"), "w", encoding="utf-8") as f:
            f.write("VTOL Complete Sizing Build Specifications\n")
            f.write("=========================================\n")
            f.write(f"MTOW: {spec.mtow_kg} kg\n")
            f.write(f"Configuration: {spec.configuration_type}\n")
            f.write(f"Rotor positions count: {len(spec.lift_system.rotor_layout.rotors)}\n")

        # 4. Markdown engineering report
        md_report = f"""# VTOL Sizing Synthesis & Engineering Report
## Sprint 44 — End-to-End Design Pipeline

This report summarizes the sizing results for the VTOL hybrid platform.

### Sizing Executive Summary
*   **Total Takeoff Weight (MTOW)**: {spec.mtow_kg:.3f} kg
*   **Empty Weight**: {spec.empty_weight_kg:.3f} kg
*   **Payload Capacity**: {spec.payload_weight_kg:.2f} kg
*   **Estimated Endurance**: {spec.estimated_endurance_min:.1f} min
*   **Estimated Range**: {spec.estimated_range_km:.2f} km

### Subsystem Sizing Details
*   **Wing Span**: {spec.wing.wing_geometry.span_m:.2f} m (AR: {spec.wing.wing_geometry.aspect_ratio:.1f})
*   **Selected Airfoil**: {spec.airfoil.selected_airfoil}
*   **Tail Configuration**: {spec.tail.tail_geometry.tail_configuration} (Arm: {spec.tail.tail_geometry.tail_arm_m:.2f}m)
*   **Fuselage volume**: {spec.fuselage.fuselage_geometry.volume_m3:.3f} m3
*   **Lift Motors**: {spec.lift_system.lift_motor_selection.get('name', 'Unknown')}
*   **Forward Motors**: {spec.forward_propulsion.motor_selection.get('name', 'Unknown')}
*   **Battery Pack**: {spec.electrical.battery_pack.chemistry} ({spec.electrical.battery_pack.series_count_s}S {spec.electrical.battery_pack.parallel_count_p}P, {spec.electrical.battery_pack.energy_wh:.1f} Wh)
"""
        with open(os.path.join(reports_dir, "vtol_engineering_report.md"), "w", encoding="utf-8") as f:
            f.write(md_report)


class VTOLDesignEngine(DesignEngine):
    """
    Adapter bridging the abstract DesignEngine contract to the VTOLDesignPipeline orchestrator.
    """
    def __init__(self) -> None:
        self.pipeline = VTOLDesignPipeline()

    @property
    def engine_id(self) -> str:
        return "VTOLDesignEngine"

    @property
    def supported_aircraft_types(self) -> list[AircraftType]:
        return [AircraftType.VTOL]

    def execute_design(self, context: DesignContext) -> DesignContext:
        """
        Executes the VTOL pipeline and writes final specification to context.
        """
        reqs = context.requirement_model
        res = self.pipeline.execute(reqs)
        
        if res.success:
            context.design_data["vtol_aircraft_specification"] = res.final_specification
            context.current_stage = DesignStage.VTOL_DESIGN
            context.current_status = DesignStatus.COMPLETED
            context.add_snapshot(f"VTOLDesignEngine successfully completed sizing workflow: MTOW = {res.final_specification.mtow_kg:.2f}kg.")
        else:
            context.current_status = DesignStatus.FAILED
            context.metadata.notes = "; ".join(res.errors)
            context.add_snapshot(f"VTOLDesignEngine failed: {'; '.join(res.errors)}.")
            
        return context
