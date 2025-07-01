from .stargen import StarSystem
from .config.starsystem import StarSystemConfig

def generate_star_system(config: StarSystemConfig | None = None) -> StarSystem:
    """Create a StarSystem using the provided configuration."""
    return StarSystem(config=config)
from .star import Star
from .planet import Planet
from .world import World

__all__ = [
    'StarSystem',
    'StarSystemConfig',
    'generate_star_system',
    'Star',
    'Planet',
    'World',
]
