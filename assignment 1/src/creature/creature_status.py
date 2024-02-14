from __future__ import annotations

from dataclasses import dataclass, field

from src.static.characteristics import STATUS_PREY


@dataclass
class CreatureStatus:
    status_id: int = field(default=STATUS_PREY)
