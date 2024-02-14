from random import choice, randint
from typing import Protocol

import src.static.characteristics as chars
from src.creature.creature_characteristics import CreatureCharacteristics
from src.static.movement import LEGS_TO_RUN, WINGS_TO_FLY


class CreatureEvolver(Protocol):
    @classmethod
    def evolve(cls, characteristics: CreatureCharacteristics) -> None:
        pass


class RandomCreatureEvolver(CreatureEvolver):
    @classmethod
    def evolve(cls, characteristics: CreatureCharacteristics) -> None:
        characteristics.legs = randint(chars.MINIMUM_AMOUNT_OF_LEGS, LEGS_TO_RUN)
        characteristics.wings = randint(chars.MINIMUM_AMOUNT_OF_WINGS, WINGS_TO_FLY)
        characteristics.claws_boost = choice(chars.CLAWS_BOOST_OPTIONS)
        characteristics.teeth_boost = choice(chars.TEETH_BOOST_OPTIONS)
