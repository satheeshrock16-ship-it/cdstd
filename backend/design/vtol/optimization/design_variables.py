from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass(slots=True)
class DesignVariable:
    """
    A single variable adjusted during optimization loops.
    """
    name: str
    base_value: float
    optimized_value: float
    min_bound: float
    max_bound: float

@dataclass(slots=True)
class DesignVariables:
    """
    Set of design parameters.
    """
    variables: List[DesignVariable]
    metadata: Dict[str, Any] = field(default_factory=dict)
