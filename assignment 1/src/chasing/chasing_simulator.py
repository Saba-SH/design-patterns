from dataclasses import dataclass
from typing import Callable

from src.creature.creature import Creature
from src.static.characteristics import STATUS_PREDATOR, STATUS_PREY


@dataclass
class ChasingSimulator:
    predator: Creature
    prey: Creature
    runtime_error_handler: Callable[[Creature], None] = None

    def safe_move_creature(self, creature) -> None:
        try:
            creature.move()
        except RuntimeError:
            self.runtime_error_handler(
                creature
            ) if self.runtime_error_handler is not None else None

    def simulate_chase(self) -> int:
        while True:
            if self.predator.location >= self.prey.location:
                return STATUS_PREDATOR

            if self.predator.stamina == 0:
                return STATUS_PREY

            self.safe_move_creature(self.predator)
            self.safe_move_creature(self.prey)
