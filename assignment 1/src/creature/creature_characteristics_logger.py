from typing import Protocol

import src.static.characteristics as chars
from src.creature.creature import Creature


class CreatureCharacteristicsDescriptor(Protocol):
    @classmethod
    def description(cls, creature: Creature) -> str:
        pass


class CreatureCharacteristicsDescriptorImpl:
    @classmethod
    def description(cls, creature: Creature) -> str:
        return (
            f"Creature status: {chars.STATUS_DESCRIPTIONS[creature.status]}\n"
            f"Location: {creature.location}, "
            f"Stamina: {creature.stamina}, "
            f"Health: {creature.health}, Power: {creature.power}\n"
            f"Legs: {creature.characteristics.legs}, "
            f"Wings: {creature.characteristics.wings}, "
            f"Claws: {chars.CLAWS_DESCRIPTIONS[creature.characteristics.claws_boost]}, "
            f"Teeth: {chars.TEETH_DESCRIPTIONS[creature.characteristics.teeth_boost]}"
        )
