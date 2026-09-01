# Torq Wings Design Studio V3 Architecture Specification

## Purpose

This document is the official software architecture specification for Torq Wings Design Studio V3. It defines the approved architecture, subsystem responsibilities, interaction model, and development principles for the platform.

This document is a technical blueprint for future developers and AI coding assistants. It does not define implementation code, algorithms, formulas, or unapproved features.

## 1. High-Level Architecture

Torq Wings Design Studio V3 is composed of modular engineering engines that execute sequentially or iteratively through a mission-driven workflow.

The implemented engineering workflow execution flow is:

```text
Mission Requirements
       ↓
Mission Intelligence Engine  [IMPLEMENTED]
       ↓
Platform Intelligence / Vehicle Advisor  [IMPLEMENTED]
       ↓
Configuration Intelligence Engine  [IMPLEMENTED]
       ↓
Component Intelligence Engine  [IMPLEMENTED]
       ↓
Aircraft Sizing Synthesis Pipelines  [IMPLEMENTED]
(Multirotor / Fixed-Wing / Hybrid VTOL)
       ↓
Parametric CAD Generation Engine  [IMPLEMENTED - Script/Builder Output]
(OpenVSP direct binary integration boundary [PLANNED])
       ↓
Engineering Analysis Engines  [IMPLEMENTED - Analytical/Empirical]
(VSPAERO solver binary integration boundary [PLANNED])
       ↓
Subsystem Optimization Engines  [IMPLEMENTED]
       ↓
Design Verification Engine  [IMPLEMENTED]
       ↓
Explainability & Decision Tracing  [IMPLEMENTED]
       ↓
Report & Manufacturing Package Exporters  [IMPLEMENTED]
```

The architecture is strictly modular. Each subsystem remains independently testable and documented.

## 2. Core Software Modules

### Mission Intelligence Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/common/mission/` and aircraft-specific mission modules). Transforms raw mission intent into structured requirement objects (`RequirementModel`), operating environment limits, complexity metrics, and strategy priorities for downstream engines.

### Platform Intelligence & Vehicle Advisor Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/advisor/` and `backend/design/router/`). Evaluates platform suitability across multirotor, fixed-wing, and hybrid VTOL UAVs using multi-criteria decision matrices, feasibility assessors, and ranking strategies (`RecommendationEngine`).

### Configuration Intelligence Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/*/configuration/`). Freezes aircraft layout options, wing planforms, tail configurations, and propulsion layouts for multirotor, fixed-wing, and VTOL UAVs.

### Component Intelligence Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/components/`). Filters raw component repositories using mission constraints and compatibility rules to build candidate pools for motors, propellers, ESCs, batteries, avionics, cameras, and sensors.

### Aircraft Sizing Synthesis Engines

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/multirotor/pipeline/`, `backend/design/fixed_wing/pipeline/`, `backend/design/vtol/pipeline/`). Multidisciplinary synthesis orchestrators executing iterative convergence sizing loops to determine MTOW, geometry, propulsion requirements, mass breakdown, and electrical distribution.

### Geometry & CAD Generation Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/fixed_wing/cad/`, `backend/design/vtol/cad/`). Generates parametric coordinate systems, reference geometries, feature trees, assembly structures, and code-based CAD exports. *(External OpenVSP executable bindings represent a planned integration boundary).*

### Engineering Analysis Engines

**[IMPLEMENTED & OPERATIONAL]** Subsystem analysis modules in aerodynamics, flight performance, hover performance, transition dynamics, cruise performance, and 3D mass properties. *(External VSPAERO solver binary integration represents a planned boundary).*

### Optimization Engines

**[IMPLEMENTED & OPERATIONAL]** Subsystem sizers and optimizers (`frame_optimizer`, `motor_optimizer`, `battery_optimizer`, `wing_planform_optimizer`, etc.) driving constrained candidate evaluation.

### Validation & Verification Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/common/verification/`). Evaluates compliance against structural, thermal, electrical, safety, and performance certification rules, generating detailed compliance reports.

### Explainability Engine

**[IMPLEMENTED & OPERATIONAL]** Exposes rationale, design decisions, constraint warnings, and calculation traces embedded inside output specifications and context snapshots.

### Report & Manufacturing Generation Engine

**[IMPLEMENTED & OPERATIONAL]** (`backend/design/*/report/` and manufacturing generators). Compiles engineering reports (Markdown, HTML, JSON), Bill of Materials (BOM), cost breakdowns, cutting plans, 3D printing parameters, and build specifications.

### AI Intelligence Layer

**[PLANNED / ROADMAP]** Optional future assistant layer operating above established engineering workflows.

## 3. Backend Architecture

The backend architecture follows a layered structure:

```text
API Layer                        [PLANNED / IN DEVELOPMENT]
↓
Service Layer                    [IMPLEMENTED - Internal Python Services]
↓
Engineering Engines & Pipelines   [IMPLEMENTED & OPERATIONAL]
↓
Database Layer                   [PLANNED / IN DEVELOPMENT]
↓
Knowledge Base Engine & Parser   [IMPLEMENTED & OPERATIONAL]
```

### API Layer

The API Layer is the external access boundary for backend capabilities. It should expose controlled interfaces for frontend workflows, future integrations, and internal tools.

The API Layer should validate request shape, delegate business activity to services, and avoid embedding engineering logic directly.

### Service Layer

The Service Layer coordinates workflows across engines, databases, validation, reporting, and user-facing operations.

Services should orchestrate subsystem interactions while preserving clean boundaries between engineering engines and data access.

### Engineering Engines

Engineering Engines are responsible for domain-specific engineering workflows. Each engine should have clear inputs, outputs, assumptions, and validation expectations.

Engines should not own database persistence directly unless the architecture explicitly defines that boundary through services or repositories.

### Database Layer

The Database Layer manages structured project data, mission data, engineering data, component data, rules, compatibility records, formula records, analysis outputs, validation evidence, and report metadata.

The Database Layer should support traceability and reproducibility.

### Knowledge Base

The Knowledge Base is the controlled source for engineering rules, assumptions, methods, references, terminology, and validation knowledge.

Engineering engines should consume approved knowledge from the Knowledge Base rather than hardcoding engineering rules.

## 4. Frontend Architecture

The frontend should provide professional engineering workflows that reflect the approved backend architecture and engineering process.

### Dashboard

The Dashboard provides the project-level entry point, design status, workflow progress, validation state, and access to major platform areas.

### Mission Wizard

The Mission Wizard guides users through mission definition and requirement capture. It is the user-facing entry point for Mission Intelligence.

### Design Studio

The Design Studio provides the main workspace for platform, configuration, component, sizing, geometry, and design-state workflows.

### Optimization View

The Optimization View presents component optimization and whole-aircraft optimization workflows, candidate comparisons, objective progress, and constraint status.

### Validation View

The Validation View presents validation checks, validation evidence, warnings, failures, and review status.

### Engineering Report

The Engineering Report view presents structured report outputs generated from mission, design, analysis, optimization, validation, and explainability data.

### Component Database

The Component Database view provides access to approved component data, categories, compatibility information, and component evidence.

### Settings

Settings provide project configuration, user preferences, environment configuration, and future administrative controls within approved architecture boundaries.

## 5. Engineering Knowledge Base

The Engineering Knowledge Base exists to make engineering behavior controlled, auditable, and explainable.

Its purpose is to store approved:

- Engineering rules
- Assumptions
- Formula references
- Validation rules
- Compatibility rules
- Domain terminology
- Source references
- Method boundaries

Engineering rules are never hardcoded as isolated logic. The software must read approved engineering knowledge from the Knowledge Base or documented data sources designed for that purpose.

The Knowledge Base supports:

- Traceable engineering decisions
- Reproducible analysis
- Controlled validation
- Explainable outputs
- Reviewable engineering assumptions

## 6. Database Architecture

The database architecture is organized around engineering traceability and controlled data ownership.

### Mission Database

The Mission Database stores mission definitions, mission categories, operational context, constraints, payload requirements, endurance expectations, range expectations, and mission-level records.

### Engineering Database

The Engineering Database stores engineering data required by sizing, geometry, analysis, optimization, validation, explainability, and reporting workflows.

### Component Databases

Component Databases store structured component records, component categories, specifications, evidence, constraints, and source metadata.

### Rule Database

The Rule Database stores approved engineering, validation, compatibility, and workflow rules in a structured and reviewable form.

### Compatibility Database

The Compatibility Database stores relationships between missions, platform types, configurations, components, constraints, and validation requirements.

### Formula Database

The Formula Database stores approved formula references, formula metadata, assumptions, applicability boundaries, and source traceability.

### Relationships

Mission records drive platform, configuration, component, sizing, analysis, optimization, validation, and reporting workflows.

Engineering records must remain connected to mission context, platform decisions, configuration decisions, component choices, assumptions, rules, formulas, validation evidence, and report outputs.

Component data must be connected to compatibility records and validation rules before it can be used in selection or optimization workflows.

Formula records must be connected to engineering assumptions, applicability boundaries, and validation expectations.

## 7. Component Intelligence Architecture

All component selection must follow the approved component intelligence flow:

```text
Mission
↓
Mission Category
↓
Filtered Candidate Pool
↓
Optimization
↓
Validation
↓
Selected Component
```

No selector should search the entire component database directly.

The Component Intelligence Engine must first interpret the mission and mission category, then create a filtered candidate pool using approved compatibility rules and mission constraints.

Optimization should operate only on the filtered candidate pool. Validation must verify that selected components satisfy mission, platform, configuration, compatibility, safety, and performance constraints.

## 8. Optimization Architecture

Optimization is divided into component optimization and whole-aircraft optimization.

### Component Optimization

Component Optimization evaluates component candidates within mission-specific, platform-specific, configuration-specific, and compatibility-constrained candidate pools.

It must use approved objectives, constraints, and validation checks.

### Whole Aircraft Optimization

Whole Aircraft Optimization evaluates aircraft-level design states after mission, platform, configuration, component, sizing, geometry, and analysis information is available.

It must preserve full traceability from optimized outputs back to mission requirements and engineering assumptions.

### Candidate Generation

Candidate generation must be controlled by mission requirements, database records, compatibility constraints, configuration boundaries, and engineering knowledge.

Generated candidates must remain reviewable and traceable.

### Iterative Optimization

Iterative optimization should refine candidate designs through controlled feedback from analysis and validation outputs.

Iterations must not bypass validation or override engineering rules.

### Mission-Based Scoring

Optimization scoring must be based on mission requirements and approved objective definitions.

Scores should remain explainable and connected to the mission definition.

### Validation

Optimization outputs must pass validation before they can be promoted to selected or recommended design states.

## 9. Validation Architecture

Validation is a first-class subsystem. It verifies that design states, decisions, inputs, and outputs comply with approved engineering expectations.

Validation categories include:

- Electrical
- Mechanical
- Structural
- Mission
- Safety
- Performance
- Compatibility

Validation results should identify pass, fail, warning, and review-required states where appropriate. Validation evidence must remain traceable to rules, assumptions, data sources, and design records.

## 10. Explainability Architecture

Every engineering decision must be traceable.

The Explainability Engine provides an Engineering Decision Trace that records how a decision was produced, which inputs were used, which rules were applied, which assumptions were active, which candidates were considered, which constraints affected the result, and which validation checks were performed.

An Engineering Decision Trace should connect:

- Mission requirement
- Platform decision
- Configuration decision
- Component decision
- Sizing result
- Geometry artifact
- Analysis output
- Optimization result
- Validation evidence
- Report section

Explainability is required for engineering confidence, review, debugging, compliance, and future AI-assisted workflows.

## 11. AI Layer

The AI Intelligence Layer assists engineering. It never replaces engineering rules.

AI may support:

- Developer assistance
- Documentation assistance
- Workflow guidance
- Report drafting support
- Explanation summarization
- Review assistance

AI must operate within the approved architecture, engineering knowledge base, validation engine, explainability engine, and reporting workflow.

AI-generated outputs must remain reviewable, traceable, and subordinate to approved engineering data, rules, and validation procedures.

## 12. Development Principles

### Engineering First

Engineering correctness, traceability, and validation take priority over automation, presentation, or convenience.

### Database Driven

Structured data should guide platform behavior. Important engineering decisions should be supported by explicit records, schemas, relationships, and evidence.

### Knowledge Base Driven

Engineering rules, formulas, assumptions, compatibility knowledge, and validation expectations should come from the approved Knowledge Base and related structured records.

### Modular

Each subsystem should have clear responsibilities, inputs, outputs, and boundaries.

### Scalable

The architecture should support growth from early prototypes to commercial-grade aerospace software without requiring disruptive redesign.

### Explainable

Every engineering decision should be understandable, traceable, and reviewable.

### Production Ready

Future implementation should be maintainable, testable, documented, observable, and suitable for commercial aerospace software development.
