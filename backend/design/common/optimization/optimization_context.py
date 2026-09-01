"""
Fixed-Wing/Multirotor/VTOL Shared Optimization Context

Encapsulates requirements, configuration layouts, and specs passed across optimizers.
"""

from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class OptimizationContext:
    """
    Holds global mission requirements, aircraft configuration state,
    historical specification updates, and search metadata.
    """
    requirements: Any
    configuration: Any = None
    previous_specifications: Dict[str, Any] = field(default_factory=dict)
    global_constraints: Dict[str, Any] = field(default_factory=dict)
    iteration_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
