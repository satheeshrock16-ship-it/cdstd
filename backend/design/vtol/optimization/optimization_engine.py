from .optimization_requirements import OptimizationRequirements
from .optimization_profile import OptimizationProfile
from .optimization_constraints import OptimizationConstraints
from .optimization_result import OptimizationResult
from .optimization_registry import OptimizationRegistry
from .optimization_validator import OptimizationValidator

class OptimizationEngine:
    """
    Façade manager coordinating VTOL design space explorations and tradeoff evaluations.
    """
    def __init__(self, profile: OptimizationProfile = None, constraints: OptimizationConstraints = None):
        self.profile = profile or OptimizationProfile()
        self.constraints = constraints or OptimizationConstraints()

    def design(self, requirements: OptimizationRequirements) -> OptimizationResult:
        strategy = OptimizationRegistry.get_strategy(requirements.preferred_optimizer_type)
        result = strategy.optimize_design(requirements, self.profile)
        
        errors = OptimizationValidator.validate(result, self.constraints)
        if errors:
            result.warnings.extend(errors)
            
        return result
