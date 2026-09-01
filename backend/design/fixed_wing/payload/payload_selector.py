"""
Fixed-Wing Mission Payload Selector Subsystem

Purpose:
    Defines the `PayloadSelector` class and the database of payload records.

Role in Architecture:
    `PayloadSelector` maps target strategy needs to concrete sensors or cargo specifications.
"""

from typing import List
from backend.design.fixed_wing.payload.payload_requirements import PayloadType


class PayloadRecord:
    """Payload item details."""

    def __init__(
        self,
        name: str,
        payload_type: PayloadType,
        weight_kg: float,
        power_w: float,
        bandwidth_mbps: float,
        dimensions_mm: List[float],  # [L, W, H]
    ) -> None:
        self.name = name
        self.payload_type = payload_type
        self.weight_kg = weight_kg
        self.power_w = power_w
        self.bandwidth_mbps = bandwidth_mbps
        self.dimensions_mm = dimensions_mm


class PayloadSelector:
    """
    Selector class matching payload types to database items.
    """

    _payloads: List[PayloadRecord] = [
        PayloadRecord("Sony RX1R II (RGB)", PayloadType.RGB_CAMERA, 0.51, 15.0, 5.0, [113, 72, 74]),
        PayloadRecord("MicaSense RedEdge (Multispectral)", PayloadType.MULTISPECTRAL, 0.35, 8.0, 2.0, [87, 59, 45.4]),
        PayloadRecord("FLIR Duo Pro R (Thermal)", PayloadType.THERMAL, 0.22, 12.0, 4.0, [87, 82, 69]),
        PayloadRecord("Velodyne VLP-16 (LiDAR)", PayloadType.LIDAR, 0.83, 10.0, 8.0, [103, 103, 72]),
        PayloadRecord("Agricultural Spray Tank System", PayloadType.SCIENTIFIC, 1.8, 12.0, 0.5, [250, 120, 120]),
        PayloadRecord("Standard Cargo Box Package", PayloadType.CARGO, 2.0, 0.0, 0.0, [180, 100, 100]),
        PayloadRecord("MetSens Environmental Probe", PayloadType.ENV_SENSORS, 0.15, 2.0, 0.1, [60, 40, 30]),
    ]

    def select_payload(self, target_type: PayloadType, max_weight_kg: float) -> PayloadRecord:
        """
        Selects the best database record of the target type.
        """
        candidates = [p for p in self._payloads if p.payload_type == target_type and p.weight_kg <= max_weight_kg]
        if not candidates:
            # Check if there are any components of this type at all in database
            all_of_type = [p for p in self._payloads if p.payload_type == target_type]
            if all_of_type:
                lightest = min(all_of_type, key=lambda p: p.weight_kg)
                raise ValueError(
                    f"COMPONENT_DATABASE_LIMITATION: Lightest available component of type '{target_type.value}' "
                    f"in database weighs {lightest.weight_kg:.2f} kg, which exceeds the maximum allowed "
                    f"structural payload limit of {max_weight_kg:.2f} kg."
                )
            else:
                raise ValueError(
                    f"COMPONENT_DATABASE_LIMITATION: No payload components of type '{target_type.value}' "
                    f"are available in the database."
                )

        return min(candidates, key=lambda p: p.weight_g if hasattr(p, 'weight_g') else p.weight_kg)
