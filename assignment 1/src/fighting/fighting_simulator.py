from dataclasses import dataclass

from src.creature.creature import Creature
from src.fighting.damage_calculator import DamageCalculator
from src.static.characteristics import NO_HEALTH, STATUS_PREDATOR, STATUS_PREY


@dataclass
class FightingSimulator:
    predator: Creature
    prey: Creature
    calculator: DamageCalculator

    def simulate_fight(self) -> int:
        while True:
            if self.predator.health == NO_HEALTH:
                return STATUS_PREY

            predator_damage = self.calculator.calculate_damage(self.predator, self.prey)
            self.prey.take_damage(predator_damage)

            if self.prey.health == NO_HEALTH:
                return STATUS_PREDATOR

            prey_damage = self.calculator.calculate_damage(self.prey, self.predator)
            self.predator.take_damage(prey_damage)
