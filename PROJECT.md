# Torq Wings Design Studio V3 Project Specification

## 1. Project Overview

### What Is Torq Wings?

Torq Wings Design Studio V3 is a professional aerospace engineering software platform for the structured design and evaluation of unmanned aerial vehicles.

The platform is intended to support future development for:

- Multirotor UAVs
- Fixed-wing UAVs
- Hybrid VTOL UAVs

This document is the master project specification and the single source of truth for project direction, architecture boundaries, engineering principles, documentation expectations, and development standards.

### Vision

To provide a disciplined aerospace design environment where UAV concepts can be defined, evaluated, analyzed, optimized, validated, and documented through transparent engineering workflows.

### Mission

To support mission-driven UAV design by organizing aircraft requirements, platform decisions, component data, engineering knowledge, analysis outputs, validation evidence, and generated reports within a scalable software architecture.

### Long-Term Goal

The long-term goal is to develop Torq Wings Design Studio V3 into a commercial-grade aerospace engineering platform that helps users move from mission requirements to defensible UAV design decisions while preserving traceability, explainability, and engineering rigor.

## 2. Project Philosophy

### Mission-Driven Design

Aircraft design decisions should originate from mission intent, operational requirements, constraints, and validation targets. The platform should prioritize mission context before configuration, component, or optimization decisions.

### Engineering-First Approach

Engineering correctness, traceability, and maintainability take priority over automation, presentation, or convenience. Every future capability should be grounded in explicit engineering assumptions and documented validation limits.

### Data-Driven Decisions

Future system behavior should be based on structured data, defined schemas, controlled assumptions, and reproducible inputs. Design decisions should be inspectable and supported by stored evidence where appropriate.

### Explainable Engineering

The platform should make engineering reasoning visible. Users and developers should be able to understand why a recommendation, analysis result, sizing output, or validation decision was produced.

### Modular Architecture

The repository should remain organized around clear responsibilities. Mission logic, platform logic, component data, analysis engines, optimization workflows, APIs, and user interfaces should remain separable.

### Scalability

The project structure should support growth from early prototypes to production systems without requiring disruptive reorganization. New capabilities should fit into established architectural areas.

### 3. Core Capabilities

The following capabilities define the core functional areas of the project, highlighting what is currently implemented in Python versus future architectural targets.

### Mission Intelligence

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/common/mission/` and aircraft-specific mission modules. Represents mission goals, constraints, complexity scoring, operational profiles, payload requirements, endurance expectations, range targets, and environmental limits.

### Platform Intelligence & Vehicle Advisor

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/advisor/` and `backend/design/router/`. Evaluates mission profiles against multirotor (quadcopter, hexacopter, octocopter), fixed-wing, and hybrid VTOL suitability metrics, ranking layout choices and routing contexts to target design studios.

### Configuration Intelligence

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/*/configuration/`. Freezes layout families, tail/wing geometry types, propulsion arrangements, and configuration-level trade spaces across supported aircraft categories.

### Component Intelligence

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/components/` and subsystem-specific selectors. Manages catalog component candidate pools (motors, propellers, ESCs, batteries, avionics, sensors), compatibility scoring, constraint filtering, and component evidence.

### Aircraft Sizing & Synthesis Pipelines

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/multirotor/pipeline/`, `backend/design/fixed_wing/pipeline/`, and `backend/design/vtol/pipeline/`. Multidisciplinary iterative sizing loops converging takeoff mass, wing/tail geometry, lift/thrust requirements, and battery mass.

### Geometry & CAD Generation

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/fixed_wing/cad/` and `backend/design/vtol/cad/`. Generates parametric CAD feature trees, coordinate systems, reference geometries, assembly structures, and script/builder exports. *(Direct binary bindings to external solvers like OpenVSP remain a future integration boundary).*

### Engineering Analysis

**[CURRENT IMPLEMENTATION]** Implemented across subsystem analysis engines (`flight_performance`, `mass_properties`, `aerodynamics`, `hover_performance`, `transition`, `cruise_performance`). Computes drag polars, stability margins, CG locations, thrust/power curves, and energy consumption. *(VSPAERO solver execution remains a future integration boundary).*

### Optimization

**[CURRENT IMPLEMENTATION]** Implemented in subsystem sizers and optimizers (`frame_optimizer`, `motor_optimizer`, `wing_planform_optimizer`, etc.). Evaluates design candidates against multi-objective functions and physical constraints.

### Validation & Verification

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/common/verification/` and subsystem validators. Runs rule-based certification and safety checks (electrical current limits, static margin, thrust-to-weight, thermal limits) producing structured pass/fail reports.

### Explainability

**[CURRENT IMPLEMENTATION]** Implemented via reasoning strings, decision logs, and audit snapshots embedded within design contexts and generated specifications.

### Report & Package Generation

**[CURRENT IMPLEMENTATION]** Implemented in `backend/design/*/report/` and manufacturing generators. Produces structured Markdown/HTML/JSON reports, Bills of Materials (BOM), cost estimates, cutting plans, 3D printing guidelines, and build specifications.

## 4. Supported Aircraft

### Multirotor UAV

**[CURRENT IMPLEMENTATION]** Fully supported via `MultirotorDesignPipeline`. Includes mission strategy, catalog frame selection, motor/prop/ESC/battery matching, electrical harness routing, component layout packaging, mass properties/CG calculation, flight performance strategy, verification audit, BOM compilation, and build instructions.

### Fixed-Wing UAV

**[CURRENT IMPLEMENTATION]** Fully supported via `FixedWingDesignPipeline`. Includes mission analysis, configuration freeze, wing and tail planform sizing, airfoil database and polar analysis, fuselage sizing, propulsion matching, performance envelope calculation, mass & static stability margin analysis, verification audit, parametric CAD feature tree generation, manufacturing package export, and report generation.

### Hybrid VTOL UAV

**[CURRENT IMPLEMENTATION]** Fully supported via `VTOLDesignPipeline`. Includes multidisciplinary synthesis loop combining lift-rotor system sizing, forward propulsion sizing, wing/tail/fuselage design, hover performance, transition dynamics and scheduling, cruise performance, electrical power distribution, verification audit, CAD generation, manufacturing package export, and report generation.

## 5. Development Principles

### Production-Quality Code

All future implementation should be written with commercial software quality in mind, including maintainability, observability, clear interfaces, and controlled dependencies.

### Clean Architecture

The system should preserve separation of concerns between domain models, engineering engines, services, APIs, data access, validation, and presentation layers.

### SOLID Principles

Future code should follow SOLID design principles where applicable, especially for shared services, engineering engines, validators, and extensible aircraft-type workflows.

### Documentation-First

Major concepts, architectural boundaries, engineering assumptions, database schemas, API contracts, and validation expectations should be documented before or alongside implementation.

### Testing-First

Future implementation should be accompanied by appropriate tests. Engineering behavior should be testable, repeatable, and validated against documented expectations.

### Reusable Modules

Reusable modules should be preferred over duplicated logic. Shared behavior should be extracted only when it represents a stable concept or reduces meaningful complexity.

### Engineering Before AI

AI-assisted features, if introduced later, must support defined engineering workflows. They must not replace documented engineering methods, validation procedures, or traceable decision-making.

## 6. Repository Structure Overview

The repository structure houses implemented Python backend engines, test suites, automation scripts, and project documentation, while reserving clear boundaries for planned layers.

- `docs/`: Project documentation, architecture records, engineering references, domain handbooks, API notes, and developer guides.
- `backend/`: Core backend application containing implemented engineering studios (`backend/design/`), knowledge base engine (`backend/knowledge/`), domain models (`backend/models/`), application lifecycle container (`backend/application/`), as well as planned areas (`backend/api/` and `backend/database/`).
- `frontend/`: Planned user interface application layer.
- `shared/`: Shared contracts, constants, and cross-layer definitions.
- `tests/`: Implemented unit, integration, and validation test suites for sizers, algorithms, engines, and multidisciplinary pipelines (`tests/design/`).
- `scripts/`: Implemented project automation, pipeline runners, diagnostic tools, and validation campaign execution scripts.
- `reports/`: Implemented directory containing generated validation reports, CSV case ledgers, datasheet summaries, and test logs.
- `prompts/`: AI-assistant prompt templates and workflow guidance.
- `.github/`: Repository automation and workflow definitions.
- `assets/`: Static assets, reference diagrams, and project media.

## 7. Documentation Structure

Project documentation is organized under `docs/` and should remain aligned with this specification.

- `docs/roadmap/`: Detailed roadmap notes, planning documents, and phased delivery records.
- `docs/architecture/`: Architecture decisions, diagrams, boundaries, and system design records.
- `docs/engineering_knowledge_base/`: Approved engineering references, assumptions, methods, and domain knowledge.
- `docs/database_schemas/`: Future database schema documentation and data model notes.
- `docs/api/`: Future API contracts, endpoint documentation, and integration references.
- `docs/developer_guides/`: Developer setup, workflows, standards, and implementation guidance.

Root-level documents provide project-wide direction:

- `README.md`: Public-facing project overview.
- `PROJECT.md`: Master project specification and single source of truth.
- `ROADMAP.md`: High-level development roadmap.
- `ARCHITECTURE.md`: High-level architecture overview.
- `CONTRIBUTING.md`: Contribution expectations and workflow.
- `LICENSE`: Project license notice.

## 8. Engineering Knowledge Base

The engineering knowledge base is the future controlled source for approved aerospace engineering references, assumptions, terminology, methods, constraints, and validation notes.

It should be treated as an auditable engineering resource. Future entries should be structured, reviewed, traceable, and aligned with supported aircraft categories.

The knowledge base should not become an uncontrolled collection of notes. It should support explainable engineering, reproducible analysis, and defensible design decisions.

## 9. Database Philosophy

Database design should prioritize structured data, explicit relationships, traceability, and long-term maintainability.

Future database schemas should be documented before implementation and should support:

- Mission definitions
- Aircraft platforms
- Configurations
- Components
- Analysis records
- Optimization records
- Validation evidence
- Report metadata

Database work should avoid premature complexity. Schemas should evolve from approved project needs and documented architecture decisions.

## 10. Coding Standards

Future code should be clear, modular, typed where appropriate, and organized according to repository boundaries.

Development standards should include:

- Consistent formatting
- Meaningful names
- Small, focused modules
- Explicit interfaces
- Minimal hidden side effects
- Controlled dependencies
- Clear error handling
- Documentation for non-obvious engineering assumptions

Implementation must remain aligned with the approved architecture and should not introduce unapproved feature areas.

## 11. Testing Strategy

Testing should be treated as a core engineering requirement.

The future test structure is divided into:

- `tests/unit/`: Tests for isolated functions, models, validators, and modules.
- `tests/integration/`: Tests for interactions between services, APIs, databases, engines, and shared contracts.
- `tests/validation/`: Tests that verify engineering behavior against documented assumptions, known cases, approved methods, or validation benchmarks.

Engineering tests should be reproducible and should clearly separate software correctness from engineering validation.

## 12. Contribution Guidelines

Contributions should follow the project architecture, documentation standards, and development principles defined in this document.

Before contributing implementation work, contributors should confirm that the work is aligned with:

- Approved project scope
- Current roadmap phase
- Architecture boundaries
- Documentation requirements
- Testing expectations
- Engineering validation requirements

Contributors should avoid adding features, abstractions, dependencies, or workflows that are not supported by the current project phase or approved architecture.

## 13. Versioning Strategy

Versioning should be introduced when the project reaches a stage where releases, API contracts, database migrations, or user-facing capabilities require stable version identifiers.

Future versioning should distinguish between:

- Repository development state
- Application releases
- API versions
- Database schema versions
- Engineering knowledge base revisions
- Validation dataset revisions

Until a formal release process is established, versioning decisions should remain documented and conservative.

## 14. Future Vision

Torq Wings Design Studio V3 is intended to grow into a disciplined aerospace design environment that supports the complete journey from mission definition to aircraft design evidence.

The future platform should help developers, engineers, and users work with complex UAV design decisions through modular software, structured data, validated methods, and transparent engineering reasoning.

The project should evolve carefully. Each new capability should strengthen the platform's engineering foundation, preserve explainability, and support commercial-grade reliability.
