from typing import Protocol

from src.creature.creature import Creature


class DamageCalculator(Protocol):
    def calculate_damage(self, attacker: Creature, defender: Creature):
        pass


class BasicDamageCalculator:
    def calculate_damage(self, attacker: Creature, defender: Creature = None) -> int:
        return (
            attacker.power * attacker.characteristics.claws_boost
            + attacker.characteristics.teeth_boost
        )
