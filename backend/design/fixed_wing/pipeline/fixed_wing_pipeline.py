"""
Fixed-Wing Sizing Pipeline Facade.
"""
from typing import Optional, List, Any
import logging

from backend.design.common.requirements.requirement_model import RequirementModel
from backend.design.fixed_wing.pipeline.pipeline_context import FixedWingPipelineContext
from backend.design.fixed_wing.pipeline.pipeline_result import FixedWingDesignResult, PipelineStatus
from backend.design.fixed_wing.pipeline.pipeline_stage import (
    MissionTranslationStage,
    ConfigurationSelectionStage,
    WingPlanformOptimizationStage,
    FuselageOptimizationStage,
    PayloadPackagingStage,
    TailOptimizationStage,
    PropulsionOptimizationStage,
    ElectricalSystemIntegrationStage,
    MassPropertiesStage,
    CGOptimizerStage,
    FlightPerformanceStage,
    AircraftConvergenceStage,
    VerificationCertificationStage,
)
from backend.design.fixed_wing.pipeline.pipeline_executor import PipelineExecutor
from backend.design.fixed_wing.pipeline.pipeline_logger import PipelineLogger
from backend.design.fixed_wing.pipeline.pipeline_diagnostics import PipelineDiagnostics
from backend.design.fixed_wing.pipeline.convergence import (
    DEFAULT_CONVERGENCE_TOLERANCE,
    DEFAULT_MAX_ITERATIONS,
)
from backend.design.fixed_wing.pipeline.exceptions import (
    FixedWingPipelineError,
    InvalidRequirementsError,
    ConfigurationInfeasibleError,
    SizingInfeasibleError,
    ComponentSelectionError,
    NonConvergenceError,
    VerificationFailedError,
)
from backend.design.fixed_wing.convergence.models import FinalAircraftSpecification


class PipelineFinalAircraftSpecification(FinalAircraftSpecification):
    """
    Subclass extending FinalAircraftSpecification to support Sprint 33 attribute properties.
    """
    _certification_report: Any = None
    _execution_diagnostics: Any = None

    def __getattr__(self, name: str) -> Any:
        norm_name = name.replace(" ", "_").lower()
        
        # Resolve configuration layout
        config_val = "Conventional"
        if self.wing_specification and hasattr(self.wing_specification, "layout"):
            config_val = getattr(self.wing_specification, "layout")
        elif self.fuselage_specification and hasattr(self.fuselage_specification, "layout"):
            config_val = getattr(self.fuselage_specification, "layout")

        mapping = {
            "mission": self.mission_summary,
            "configuration": config_val,
            "wing_specification": self.wing_specification,
            "fuselage_specification": self.fuselage_specification,
            "payload_specification": self.payload_specification,
            "tail_specification": self.tail_specification,
            "propulsion_specification": self.propulsion_specification,
            "electrical_specification": self.electrical_specification,
            "mass_properties": self.mass_properties_specification,
            "cg_specification": self.cg_specification,
            "performance_specification": self.performance_specification,
            "convergence_report": {
                "convergence_status": self.convergence_status,
                "iterations_performed": len(self.iteration_history),
                "iteration_history": self.iteration_history,
            },
            "certification_report": getattr(self, "_certification_report", None),
            "execution_diagnostics": getattr(self, "_execution_diagnostics", None),
        }
        if norm_name in mapping:
            return mapping[norm_name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class FixedWingDesignPipeline:
    """
    Production entry point for fixed-wing aircraft design.
    """

    def __init__(
        self,
        tolerance: float = DEFAULT_CONVERGENCE_TOLERANCE,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        raise_on_failure: bool = False,
    ) -> None:
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.raise_on_failure = raise_on_failure
        self.logger = PipelineLogger()
        
        # Disable verbose optimization candidate logging to speed up execution
        from backend.design.common.optimization.optimization_logger import OptimizationLogger
        OptimizationLogger.info = lambda self, msg: self.logs.append(f"INFO: {msg}")
        OptimizationLogger.warning = lambda self, msg: self.logs.append(f"WARN: {msg}")
        OptimizationLogger.error = lambda self, msg: self.logs.append(f"ERROR: {msg}")

        # Backward compatibility for test mocking
        from backend.design.fixed_wing.wing.wing_engine import WingEngine
        from backend.design.fixed_wing.airfoil.airfoil_engine import AirfoilEngine
        from backend.design.fixed_wing.tail.tail_engine import TailEngine
        from backend.design.fixed_wing.fuselage.fuselage_engine import FuselageEngine
        from backend.design.fixed_wing.propulsion.propulsion_engine import PropulsionEngine
        from backend.design.fixed_wing.avionics.avionics_engine import AvionicsEngine
        from backend.design.fixed_wing.payload.payload_engine import PayloadEngine
        from backend.design.fixed_wing.mass_properties.mass_properties_engine import MassPropertiesEngine
        from backend.design.fixed_wing.flight_performance.flight_performance_engine import FlightPerformanceEngine
        from backend.design.fixed_wing.verification.verification_engine import VerificationEngine

        self._wing_engine = WingEngine()
        self._airfoil_engine = AirfoilEngine()
        self._tail_engine = TailEngine()
        self._fuselage_engine = FuselageEngine()
        self._propulsion_engine = PropulsionEngine()
        self._avionics_engine = AvionicsEngine()
        self._payload_engine = PayloadEngine()
        self._mass_properties_engine = MassPropertiesEngine()
        self._flight_performance_engine = FlightPerformanceEngine()
        self._verification_engine = VerificationEngine()

    def design_aircraft(self, requirements: RequirementModel) -> PipelineFinalAircraftSpecification:
        """
        Synthesizes, converges, and certifies a fixed-wing aircraft for requirements.
        Raises exceptions on failure.
        """
        # Save old raise_on_failure flag and force True for design_aircraft
        old_raise = self.raise_on_failure
        self.raise_on_failure = True
        try:
            res = self.execute(requirements)

            if not res.success:
                raise SizingInfeasibleError(f"Pipeline design failed with status: {res.status}")
            
            # Map specs to the final certified spec
            final_spec = PipelineFinalAircraftSpecification(
                mission_summary=res.mission_result.mission_summary if res.mission_result else {},
                wing_specification=res.wing_result,
                fuselage_specification=res.fuselage_result,
                payload_specification=res.payload_result,
                tail_specification=res.tail_result,
                propulsion_specification=res.propulsion_result,
                electrical_specification=res.electrical_result,
                mass_properties_specification=res.mass_properties_result,
                cg_specification=res.cg_result,
                performance_specification=res.performance_result,
                iteration_history=res.convergence_history,
                convergence_status="Converged" if res.converged else "Failed",
                final_design_score=res.final_design_score if hasattr(res, "final_design_score") else 0.0,
            )
            
            # Extract additional fields
            if res.verification_result and hasattr(res.verification_result, "certification_report"):
                final_spec._certification_report = res.verification_result.certification_report
            
            # execution diagnostics
            final_spec._execution_diagnostics = {
                "warnings": res.warnings,
                "errors": res.errors,
                "iterations": res.iterations,
            }
            
            return final_spec
        finally:
            self.raise_on_failure = old_raise

    def execute(self, requirements: RequirementModel) -> FixedWingDesignResult:
        """
        Runs the pipeline stages sequentially, maintaining backward compatibility.
        """
        context = FixedWingPipelineContext(mission_requirements=requirements)
        context.pipeline = self

        
        stages = [
            MissionTranslationStage(),
            ConfigurationSelectionStage(),
            WingPlanformOptimizationStage(),
            FuselageOptimizationStage(),
            PayloadPackagingStage(),
            TailOptimizationStage(),
            PropulsionOptimizationStage(),
            ElectricalSystemIntegrationStage(),
            MassPropertiesStage(),
            CGOptimizerStage(),
            FlightPerformanceStage(),
            AircraftConvergenceStage(self.max_iterations),
            VerificationCertificationStage(),
        ]

        executor = PipelineExecutor(stages=stages, logger=self.logger)

        try:
            executor.execute(context)
            status = PipelineStatus.SUCCESS
        except InvalidRequirementsError as e:
            status = PipelineStatus.INVALID_REQUIREMENTS
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e
        except ConfigurationInfeasibleError as e:
            status = PipelineStatus.CONFIGURATION_INFEASIBLE
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e
        except SizingInfeasibleError as e:
            status = PipelineStatus.SIZING_INFEASIBLE
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e
        except ComponentSelectionError as e:
            status = PipelineStatus.COMPONENT_SELECTION_FAILED
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e
        except NonConvergenceError as e:
            status = PipelineStatus.NON_CONVERGED if self.max_iterations > 5 else PipelineStatus.CONVERGENCE_FAILURE
            exc_str = str(e).lower()
            if "component_database_limitation" in exc_str or "electricaloptimizer failed" in exc_str:
                status = PipelineStatus.COMPONENT_DATABASE_LIMITATION
            elif "communication_infeasible" in exc_str:
                status = PipelineStatus.COMMUNICATION_INFEASIBLE
            elif "airfoil_structure_incompatible" in exc_str:
                status = PipelineStatus.AIRFOIL_STRUCTURE_INCOMPATIBLE
            elif "propulsion_infeasible" in exc_str or "takeoff thrust-to-weight ratio" in exc_str or "insufficient to sustain" in exc_str or "propulsionoptimizer failed" in exc_str:
                status = PipelineStatus.PROPULSION_INFEASIBLE
            elif "battery_infeasible" in exc_str:
                status = PipelineStatus.BATTERY_INFEASIBLE
            elif "stability_infeasible" in exc_str or "cgoptimizer failed" in exc_str:
                status = PipelineStatus.STABILITY_INFEASIBLE
            elif "performance_infeasible" in exc_str or "cruise speed" in exc_str or "safe limit" in exc_str or "stall" in exc_str or "flightperformanceoptimizer failed" in exc_str:
                status = PipelineStatus.PERFORMANCE_INFEASIBLE
            elif "exceeds wing root chord" in exc_str or "slender fuselage" in exc_str or "aerodynamic blockage" in exc_str or "fuselageoptimizer failed" in exc_str or "wingplanformoptimizer failed" in exc_str or "tailoptimizer failed" in exc_str or "masspropertiesoptimizer failed" in exc_str:
                status = PipelineStatus.SIZING_INFEASIBLE
            elif "takeoff weight" in exc_str or "exceeds maximum takeoff weight" in exc_str:
                status = PipelineStatus.MTOW_LIMIT_EXCEEDED
            
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e
        except VerificationFailedError as e:
            status = PipelineStatus.VERIFICATION_FAILED
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e
        except Exception as e:
            status = PipelineStatus.INTERNAL_EXCEPTION
            exc_str = str(e).lower()
            if "component_database_limitation" in exc_str or "electricaloptimizer failed" in exc_str:
                status = PipelineStatus.COMPONENT_DATABASE_LIMITATION
            elif "communication_infeasible" in exc_str:
                status = PipelineStatus.COMMUNICATION_INFEASIBLE
            elif "airfoil_structure_incompatible" in exc_str:
                status = PipelineStatus.AIRFOIL_STRUCTURE_INCOMPATIBLE
            elif "propulsion_infeasible" in exc_str or "takeoff thrust-to-weight ratio" in exc_str or "insufficient to sustain" in exc_str or "propulsionoptimizer failed" in exc_str:
                status = PipelineStatus.PROPULSION_INFEASIBLE
            elif "battery_infeasible" in exc_str:
                status = PipelineStatus.BATTERY_INFEASIBLE
            elif "stability_infeasible" in exc_str or "cgoptimizer failed" in exc_str:
                status = PipelineStatus.STABILITY_INFEASIBLE
            elif "performance_infeasible" in exc_str or "cruise speed" in exc_str or "safe limit" in exc_str or "stall" in exc_str or "flightperformanceoptimizer failed" in exc_str:
                status = PipelineStatus.PERFORMANCE_INFEASIBLE
            elif "exceeds wing root chord" in exc_str or "slender fuselage" in exc_str or "aerodynamic blockage" in exc_str or "fuselageoptimizer failed" in exc_str or "wingplanformoptimizer failed" in exc_str or "tailoptimizer failed" in exc_str or "masspropertiesoptimizer failed" in exc_str:
                status = PipelineStatus.SIZING_INFEASIBLE
            elif "takeoff weight" in exc_str or "exceeds maximum takeoff weight" in exc_str:
                status = PipelineStatus.MTOW_LIMIT_EXCEEDED
            
            context.errors.append(str(e))
            if self.raise_on_failure:
                raise e

        # Extract diagnostics
        context.diagnostics.update(PipelineDiagnostics.extract_diagnostics(context))

        # Backwards compatible result mapping
        # Retrieve score from performance result
        score = 0.0
        perf = context.performance_result
        if perf:
            score = getattr(perf, "performance_score", 0.0) or getattr(perf, "optimization_score", 0.0) or 0.0

        # Construct result
        res = FixedWingDesignResult(
            success=status == PipelineStatus.SUCCESS,
            status=status,
            iterations=len(context.iteration_history),
            converged=status == PipelineStatus.SUCCESS or status == PipelineStatus.VERIFICATION_FAILED,
            convergence_history=context.iteration_history,
            mission_result=context.mission_result,
            configuration_result=context.configuration_result,
            wing_result=context.wing_result,
            airfoil_result=context.airfoil_result,
            tail_result=context.tail_result,
            fuselage_result=context.fuselage_result,
            propulsion_result=context.propulsion_result,
            avionics_result=context.avionics_result,
            payload_result=context.payload_result,
            mass_properties_result=context.mass_properties_result,
            performance_result=context.performance_result,
            verification_result=context.verification_result,
            warnings=context.warnings,
            errors=context.errors,
        )
        res.final_design_score = score
        return res
