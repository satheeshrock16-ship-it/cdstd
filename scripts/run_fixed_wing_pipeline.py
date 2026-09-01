#!/usr/bin/env python3
"""
Simple runner script for the Fixed-Wing Sizing Pipeline.
Instantiates FixedWingDesignPipeline, creates a sample RequirementModel,
executes the pipeline, and prints the complete FinalAircraftSpecification.
"""
import os
import sys
import json
import dataclasses
from typing import Any

# Ensure workspace root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.design.common.requirements.requirement_model import RequirementModel
from backend.design.common.requirements.mission_type import MissionType
from backend.design.common.requirements.takeoff_type import TakeoffType
from backend.design.common.requirements.landing_type import LandingType
from backend.design.common.requirements.operating_environment import OperatingEnvironment
from backend.design.fixed_wing.pipeline import FixedWingDesignPipeline
from backend.design.fixed_wing.pipeline.fixed_wing_pipeline import PipelineFinalAircraftSpecification


def to_dict(obj: Any) -> Any:
    """Recursively serializes dataclasses, enums, lists, and dicts to plain Python structures."""
    if dataclasses.is_dataclass(obj):
        res = {}
        for field in dataclasses.fields(obj):
            val = getattr(obj, field.name, None)
            res[field.name] = to_dict(val)
        return res
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_dict(x) for x in obj]
    elif isinstance(obj, tuple):
        return [to_dict(x) for x in obj]
    elif hasattr(obj, '__dict__'):
        return {k: to_dict(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
    elif hasattr(obj, 'value'):  # Enums
        return obj.value
    else:
        return obj


def main():
    print("Initializing Fixed-Wing Design Pipeline...")
    pipeline = FixedWingDesignPipeline(raise_on_failure=True)

    print("Creating sample mapping UAV RequirementModel...")
    req = RequirementModel(
        mission_type=MissionType.MAPPING,
        payload_weight_kg=0.5,
        target_flight_time_min=45.0,
        target_range_km=30.0,
        cruise_speed_kmh=95.0,
        takeoff_type=TakeoffType.RUNWAY,
        landing_type=LandingType.RUNWAY,
        environment=OperatingEnvironment.RURAL,
    )

    print("Executing design pipeline...")
    res = pipeline.execute(req)
    
    if not res.success:
        print(f"Pipeline execution failed: {res.errors}")
        sys.exit(1)

    print("Mapping to PipelineFinalAircraftSpecification...")
    spec = PipelineFinalAircraftSpecification(
        mission_summary={
            "category": res.mission_result.mission_profile.mission_category.value if hasattr(res.mission_result.mission_profile.mission_category, 'value') else str(res.mission_result.mission_profile.mission_category),
            "payload_kg": res.mission_result.mission_profile.payload_kg,
            "flight_time_min": res.mission_result.mission_profile.flight_time_min,
            "cruise_speed_kmh": res.mission_result.mission_profile.cruise_speed_kmh,
            "mission_range_km": res.mission_result.mission_profile.mission_range_km,
        } if res.mission_result and res.mission_result.mission_profile else {},
        wing_specification=res.wing_result,
        fuselage_specification=res.fuselage_result,
        payload_specification=res.payload_result,
        tail_specification=res.tail_result,
        propulsion_specification=res.propulsion_result,
        electrical_specification=None,  # Not present in FixedWingDesignResult
        mass_properties_specification=res.mass_properties_result,
        cg_specification=None,          # Not present in FixedWingDesignResult
        performance_specification=res.performance_result,
        iteration_history=res.convergence_history,
        convergence_status="Converged" if res.converged else "Failed",
        final_design_score=res.final_design_score if hasattr(res, "final_design_score") else 0.0,
    )
    
    if res.verification_result and hasattr(res.verification_result, "certification_report"):
        spec._certification_report = res.verification_result.certification_report
    
    spec._execution_diagnostics = {
        "warnings": res.warnings,
        "errors": res.errors,
        "iterations": res.iterations,
    }

    print("\n" + "="*80)
    print("FINAL AIRCRAFT SPECIFICATION")
    print("="*80)
    
    spec_dict = to_dict(spec)
    print(json.dumps(spec_dict, indent=2, default=str))
    print("="*80)
    print("Pipeline execution completed successfully!")


if __name__ == "__main__":
    main()
