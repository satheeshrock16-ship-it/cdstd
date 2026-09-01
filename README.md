# Torq Wings Design Studio V3

A disciplined, multidisciplinary aerospace engineering software platform for mission-driven design, sizing, optimization, verification, and reporting of unmanned aerial vehicles (UAVs).

## Overview

Torq Wings Design Studio V3 is an advanced Python-based UAV preliminary design synthesis and analysis platform. The software translates mission requirements and operational profiles into fully converged, rule-verified aircraft design specifications.

The platform provides end-to-end engineering pipelines across three major aircraft categories: **Multirotor**, **Fixed-Wing**, and **Hybrid VTOL** UAVs. It integrates mission analysis, configuration recommendation, discrete component sizing, parametric CAD generation, multidisciplinary engineering checks, manufacturing artifact compilation, and report generation into reproducible execution workflows.

## Current Status

The core engineering engines, multidisciplinary synthesis pipelines, vehicle advisor recommendation engine, verification rule framework, CAD generation engines, manufacturing output builders, and report exporters are **IMPLEMENTED and OPERATIONAL** in Python.

### System Implementation Maturity

- **Multirotor Design Pipeline**: Implemented & Operational
- **Fixed-Wing Design Pipeline**: Implemented & Operational
- **Hybrid VTOL Design Pipeline**: Implemented & Operational
- **Vehicle Advisor / Recommendation Engine**: Implemented & Operational
- **Verification & Rule Engine**: Implemented & Operational
- **Parametric CAD Generation Framework**: Implemented & Operational (Script/Builder-based)
- **Manufacturing & BOM Exporters**: Implemented & Operational
- **Report Exporters (Markdown, HTML, JSON, TXT)**: Implemented & Operational
- **Engineering Knowledge Base Parser & Graph**: Implemented & Operational
- **REST API Layer (`backend/api/`)**: Planned / In Development
- **SQL Database Layer (`backend/database/`)**: Planned / In Development
- **Frontend User Interface (`frontend/`)**: Planned / In Development

## Current Capabilities

- **Mission Intelligence**: Requirement normalization, mission complexity calculation, operating environment constraints, and strategy priority mapping.
- **Vehicle Advisor**: Multi-criteria feasibility analysis and scoring to select/recommend quadcopter, hexacopter, octocopter, fixed-wing, or hybrid VTOL configurations for a given mission context.
- **Discrete & Continuous Component Sizing**: Catalog matching and optimization for motors, propellers, ESCs, batteries, flight controllers, cameras, companion computers, and sensors.
- **Aerodynamic & Flight Performance Analysis**: Airfoil polar calculations, wing planform optimization, drag breakdown, thrust/power requirements, endurance, range, climb, ceiling, stall, turn performance, hover efficiency, and VTOL transition dynamics.
- **Mass Properties & CG Tracking**: Component packaging layout, 3D Center of Gravity (CG) tracking, static stability margin computation, and moment of inertia estimations.
- **Rule-Based Design Verification**: Structural, electrical, thermal, mechanical, safety, and mission compliance audits against certification and engineering rules.
- **Parametric CAD & Geometry Outputs**: Part generation, coordinate system alignment, assembly structuring, and script export for fuselage, wings, tail surfaces, propulsion mounts, and internal components.
- **Manufacturing Package Compilation**: Bill of Materials (BOM) export (CSV/JSON), cost estimation, laser/CNC cutting plans, 3D printing export settings, build instructions, and quality checklists.
- **Automated Engineering Reports**: Comprehensive design reports exported to Markdown, HTML, JSON, and build specification text files.

## Aircraft Design Domains

| Aircraft Category | Implementation Status | Pipeline Execution | Key Implemented Features |
| :--- | :--- | :--- | :--- |
| **Multirotor** | **Implemented** | `MultirotorDesignPipeline` | Iterative sizing loop, catalog frame matching, propulsion optimization (motor/prop/ESC/battery), electrical harness routing, 3D CG tracking, BOM compilation, build instructions. |
| **Fixed-Wing** | **Implemented** | `FixedWingDesignPipeline` | Configuration freeze, wing & tail planform sizing, NACA airfoil database & polar analysis, fuselage sizing, propulsion matching, performance envelope, stability analysis, CAD framework, report engine. |
| **Hybrid VTOL** | **Implemented** | `VTOLDesignPipeline` | Multidisciplinary loop combining lift-rotor system sizing, forward propulsion sizing, hover performance, transition flight dynamics & scheduling, cruise performance, electrical power distribution, CAD & manufacturing package export. |

## Engineering Workflow

The implemented multidisciplinary design synthesis workflow follows a strict, traceable execution path:

```text
Mission Requirements Definition
       ↓
Mission Intelligence & Validation
       ↓
Vehicle Advisor / Platform Recommendation
       ↓
Configuration Freeze / Selection
       ↓
Multidisciplinary Iterative Sizing Loop
(Wing / Tail / Fuselage / Lift System / Forward Propulsion / Electrical / Avionics / Payload)
       ↓
Mass Properties, Packaging & 3D CG Tracking
       ↓
Flight Performance & Aerodynamic Analysis
       ↓
Certification & Verification Rule Audit
       ↓
CAD Assembly & Feature Tree Generation
       ↓
Manufacturing Package & BOM Compilation
       ↓
Engineering Report & Data Export
```

## Implemented Engineering Systems

- `backend/design/common/`: Shared requirement models, design context, validation rules, verification rule engines, and verification context models.
- `backend/design/router/`: Engine registry and router (`DesignEngineRouter`) dispatching design context to category-specific studios.
- `backend/design/studio/`: Workflow stage manager (`DesignStageManager`) and workflow orchestrator (`DesignWorkflow`).
- `backend/design/advisor/`: Vehicle recommendation engine (`RecommendationEngine`), feasibility assessor, and ranking strategies.
- `backend/design/components/`: Component repositories, candidate scoring, compatibility rules, and component selectors.
- `backend/design/multirotor/`: Multirotor mission strategy, frame optimizer, motor/propeller/ESC/battery optimizers, electrical engine, layout engine, mass properties engine, and synthesis pipeline.
- `backend/design/fixed_wing/`: Fixed-wing mission engine, configuration engine, wing engine, airfoil engine, tail engine, fuselage engine, propulsion engine, avionics engine, payload engine, mass properties engine, flight performance engine, verification engine, CAD engine, manufacturing engine, report engine, and synthesis pipeline.
- `backend/design/vtol/`: Hybrid VTOL mission engine, configuration engine, wing engine, airfoil engine, tail engine, fuselage engine, lift system engine, forward propulsion engine, electrical engine, avionics engine, payload engine, mass properties engine, hover performance engine, transition engine, cruise performance engine, CAD engine, manufacturing engine, report engine, and synthesis pipeline.
- `backend/knowledge/`: Knowledge engine (`KnowledgeEngine`), markdown document parser, graph builder, and entity repository.
- `backend/application/`: Root application container (`TorqWingsApplication`) managing backend lifecycle and knowledge loading.

## Validation & Testing

The repository contains an extensive test suite and validation campaign infrastructure:

- **Unit Tests**: Test suites covering individual sizers, selectors, models, and validators under `tests/design/`.
- **Integration & Pipeline Tests**: Full pipeline synthesis tests verifying convergence and output contracts for Multirotor, Fixed-Wing, and VTOL UAVs under `tests/design/*/pipeline/`.
- **Validation Campaigns**: Automated execution scripts under `scripts/` (e.g., `run_validation_campaign.py`, `export_all_600_cases.py`) that evaluate hundreds of design test cases, recording convergence metrics and engineering invariant compliance.

## CAD & Manufacturing

- **Parametric CAD Framework**: Generates feature trees, reference geometries, coordinate alignments, and code-driven CAD exports for fuselages, wings, tails, propulsion mounts, and internal packaging layouts.
- **Manufacturing Outputs**: Automatically produces itemized Bills of Materials (BOM), manufacturing cost breakdowns, laser/CNC cutting plans, 3D printing export settings, procurement lists, and step-by-step build specifications.

## Repository Structure

```text
torqwings studio v2/
├── ARCHITECTURE.md          # Architecture specification & subsystem boundaries
├── CONTRIBUTING.md            # Guidelines for code, documentation, and testing
├── LICENSE                    # Software license terms
├── PROJECT.md                 # Master project specification & single source of truth
├── README.md                  # Public-facing project documentation
├── ROADMAP.md                 # Phased development roadmap and milestone tracking
├── assets/                    # Project media, diagrams, and static assets
├── backend/                   # Core Python application & engineering engines
│   ├── api/                   # (Planned) REST API layer
│   ├── application/           # Application lifecycle container
│   ├── database/              # (Planned) Database persistence layer
│   ├── design/                # Engineering design studios & synthesis engines
│   │   ├── advisor/           # Vehicle recommendation & feasibility engine
│   │   ├── common/            # Shared requirements, context, validation, verification
│   │   ├── components/        # Component repository & selection engine
│   │   ├── drone/             # Drone performance & avionics subsystem adapters
│   │   ├── fixed_wing/        # Fixed-wing design engine (21+ subsystems)
│   │   ├── multirotor/        # Multirotor design engine (10+ subsystems)
│   │   ├── router/            # Design engine registry & router
│   │   ├── studio/            # Workflow stage orchestration & artifact management
│   │   └── vtol/              # Hybrid VTOL design engine (21+ subsystems)
│   ├── knowledge/             # Engineering knowledge base engine & parser
│   └── models/                # Domain entities & knowledge models
├── docs/                      # Technical documentation & engineering frameworks
├── exports/                   # Output directory for generated engineering artifacts
├── frontend/                  # (Planned) User interface application
├── reports/                   # Generated validation reports, CSV ledgers, and datasheets
├── scratch/                   # Scratch scripts and temporary analysis tools
├── scripts/                   # Runnable pipeline scripts, diagnostics, and campaign runners
└── tests/                     # Comprehensive unit, integration, and validation test suite
```

## Running the Project

### Prerequisites

- Python 3.10+
- `pytest` (for running tests)

### Executing a Design Pipeline

You can run the existing standalone design synthesis pipeline scripts directly:

```bash
# Execute Fixed-Wing Aircraft Synthesis Pipeline
python scripts/run_fixed_wing_pipeline.py

# Execute Fixed-Wing Pipeline Diagnostics
python scripts/run_fixed_wing_pipeline_diagnostic.py

# Execute Fixed-Wing Smoke Tests
python scripts/run_fixed_wing_smoke_tests.py

# Execute Multirotor & Vehicle Selection Validation Campaign
python scripts/run_validation_campaign.py
```

### Running Test Suite

```bash
# Run all tests
pytest

# Run multirotor pipeline tests
pytest tests/design/multirotor/pipeline/

# Run fixed-wing pipeline tests
pytest tests/design/fixed_wing/pipeline/
```

### Programmatic Python Usage

```python
from backend.design.common.requirements.requirement_model import RequirementModel
from backend.design.common.requirements.mission_type import MissionType
from backend.design.common.requirements.takeoff_type import TakeoffType
from backend.design.common.requirements.landing_type import LandingType
from backend.design.common.requirements.operating_environment import OperatingEnvironment
from backend.design.fixed_wing.pipeline import FixedWingDesignPipeline

# Define mission requirements
requirements = RequirementModel(
    mission_type=MissionType.MAPPING,
    payload_weight_kg=0.5,
    target_flight_time_min=45.0,
    target_range_km=30.0,
    cruise_speed_kmh=95.0,
    takeoff_type=TakeoffType.RUNWAY,
    landing_type=LandingType.RUNWAY,
    environment=OperatingEnvironment.RURAL,
)

# Execute fixed-wing synthesis pipeline
pipeline = FixedWingDesignPipeline(raise_on_failure=True)
result = pipeline.execute(requirements)

if result.success:
    print(f"Synthesis Succeeded in {result.iterations} iterations!")
    print(f"MTOW: {result.final_specification.mass_properties.total_mass_kg:.2f} kg")
    print(f"Wing Span: {result.final_specification.wing.span_m:.2f} m")
else:
    print(f"Synthesis Failed: {result.errors}")
```

## Documentation

Comprehensive project and engineering documentation is available at root and under `docs/`:

- [PROJECT.md](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/PROJECT.md): Master Project Specification
- [ARCHITECTURE.md](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/ARCHITECTURE.md): Software Architecture Blueprint
- [ROADMAP.md](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/ROADMAP.md): Development Phasing & Phased Milestones
- [CONTRIBUTING.md](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/CONTRIBUTING.md): Contribution & Development Guidelines
- [docs/](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/docs/): Engineering Frameworks, API References, and Domain Handbooks

## Development Status / Roadmap

Core engineering logic, multidisciplinary synthesis loops, verification engines, CAD generation frameworks, and report output generators are fully implemented in Python.

Future roadmap phases focus on:
1. REST API endpoint layer (`backend/api/`)
2. SQL Database persistence layer (`backend/database/`)
3. Web-based User Interface (`frontend/`)
4. Direct binary bindings for external solvers (OpenVSP / VSPAERO)

See [ROADMAP.md](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/ROADMAP.md) for full phase details.

## Contributing

See [CONTRIBUTING.md](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/CONTRIBUTING.md) for contribution rules, code standards, and PR workflows.

## License

Refer to the [LICENSE](file:///c:/Users/acer/Documents/torqwings%20studio%20v2/LICENSE) file for licensing terms.
