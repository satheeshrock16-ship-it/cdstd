"""
Fixed-Wing Propulsion Optimization Specification Model
"""

from dataclasses import dataclass


@dataclass
class PropulsionSpecification:
    """
    Sized electric propulsion system configuration and simulated performance.
    """
    # Selected Hardware Components
    motor_name: str
    propeller_name: str
    esc_name: str
    battery_name: str

    # Electrical and Operating Parameters
    operating_voltage_v: float
    cruise_current_a: float
    max_climb_current_a: float
    cell_count_s: int
    battery_capacity_mah: float
    battery_weight_g: float
    total_propulsion_weight_g: float

    # Performance Metrics
    static_thrust_n: float
    cruise_thrust_n: float
    cruise_power_w: float
    takeoff_power_w: float
    motor_efficiency: float
    propeller_efficiency: float
    total_efficiency: float
    estimated_flight_time_min: float

    # Optimization Diagnostics
    optimization_score: float
    reasoning: str
