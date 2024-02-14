from __future__ import annotations

from dataclasses import dataclass, field

from src.chasing.creature_mover import CreatureMover, GreedyCreatureMover
from src.creature.creature_characteristics import CreatureCharacteristics
from src.creature.creature_status import CreatureStatus
from src.evolution.creature_evolver import CreatureEvolver, RandomCreatureEvolver
from src.static.characteristics import (
    MINIMUM_MAX_HEALTH,
    MINIMUM_MAX_STAMINA,
    NO_HEALTH,
)


@dataclass
class Creature:
    characteristics: CreatureCharacteristics = field(
        default_factory=CreatureCharacteristics
    )
    location: int = field(default=0)
    stamina: int = field(default=MINIMUM_MAX_STAMINA)
    health: int = field(default=MINIMUM_MAX_HEALTH)
    power: int = field(default=0)
    status: CreatureStatus = field(default_factory=CreatureStatus)
    evolver: CreatureEvolver = field(default_factory=RandomCreatureEvolver)
    mover: CreatureMover = field(default_factory=GreedyCreatureMover)

    def evolve(self) -> None:
        self.evolver.evolve(self.characteristics)

    def move(self) -> None:
        stamina_change, location_change = self.mover.take_step(
            self.characteristics, self.stamina
        )
        self.stamina += stamina_change
        self.location += location_change

    def take_damage(self, damage: int) -> None:
        self.health -= damage
        if self.health < NO_HEALTH:
            self.health = NO_HEALTH
