from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CreatureCharacteristics:
    legs: int = field(default=0)
    wings: int = field(default=0)
    claws_boost: int = field(default=0)
    teeth_boost: int = field(default=0)
