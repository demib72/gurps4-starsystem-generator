from dataclasses import dataclass
from typing import Optional

@dataclass
class StarSystemConfig:
    open_cluster: Optional[bool] = None
    num_stars: Optional[int] = None
    age: Optional[float] = None
