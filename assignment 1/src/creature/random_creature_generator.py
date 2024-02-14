from random import randint
from typing import Tuple

from src.chasing.creature_mover import GreedyCreatureMover
from src.creature.creature import Creature
from src.evolution.creature_evolver import RandomCreatureEvolver
from src.static.characteristics import (
    MAXIMUM_MAX_HEALTH,
    MAXIMUM_MAX_STAMINA,
    MAXIMUM_POWER,
    MINIMUM_MAX_HEALTH,
    MINIMUM_MAX_STAMINA,
    MINIMUM_POWER,
)


def random_creature(location_endpoints: Tuple[int, int], status: int) -> Creature:
    creature = Creature()

    creature.status = status

    creature.location = randint(location_endpoints[0], location_endpoints[1])
    creature.stamina = randint(MINIMUM_MAX_STAMINA, MAXIMUM_MAX_STAMINA)
    creature.health = randint(MINIMUM_MAX_HEALTH, MAXIMUM_MAX_HEALTH)
    creature.power = randint(MINIMUM_POWER, MAXIMUM_POWER)
    creature.health = randint(MINIMUM_MAX_HEALTH, MAXIMUM_MAX_HEALTH)

    creature.evolver = RandomCreatureEvolver()
    creature.evolve()

    creature.mover = GreedyCreatureMover()

    return creature
