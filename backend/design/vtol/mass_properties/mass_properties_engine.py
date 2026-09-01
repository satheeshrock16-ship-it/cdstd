from .mass_requirements import MassRequirements
from .mass_profile import MassProfile
from .mass_constraints import MassConstraints
from .mass_result import MassResult
from .mass_registry import MassRegistry
from .mass_validator import MassValidator

class MassPropertiesEngine:
    """
    Façade manager coordinating VTOL weight distributions and CG optimization loops.
    """
    def __init__(self, profile: MassProfile = None, constraints: MassConstraints = None):
        self.profile = profile or MassProfile()
        self.constraints = constraints or MassConstraints()

    def design(self, requirements: MassRequirements) -> MassResult:
        strategy = MassRegistry.get_strategy(requirements.mission_result.mission_profile.mission_category)
        result = strategy.design_mass_properties(requirements, self.profile)
        
        errors = MassValidator.validate(result, self.constraints)
        if errors:
            result.warnings.extend(errors)
            
        return result
