"""
Fixed-Wing Propulsion Section Compiler

Purpose:
    Defines the propulsion performance content generation.

Role in Architecture:
    `PropulsionSectionCompiler` writes motor, engine, and propeller parameters.
"""

from backend.design.fixed_wing.report.report_requirements import ReportRequirements


class PropulsionSectionCompiler:
    """
    Compiler for the Propulsion chapter.
    """

    def compile(self, requirements: ReportRequirements) -> str:
        prop = requirements.propulsion_result

        content = (
            f"# Propulsion Powertrain\n\n"
            f"The sized propulsion system has the following features:\n"
            f"*   **Power Unit**: {prop.selected_motor_or_engine}\n"
            f"*   **Propeller**: {prop.selected_propeller}\n"
            f"*   **Takeoff Acceleration Force**: {prop.takeoff_analysis.acceleration_force_n:.1f} N\n"
            f"*   **Cruise Current Draw**: {prop.power_analysis.current_draw_cruise_a:.1f} A\n"
            f"*   **Estimated Cruise Throttle**: {prop.cruise_analysis.throttle_setting_pct:.1f}%\n"
        )
        return content
