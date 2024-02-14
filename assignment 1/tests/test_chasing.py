from typing import List

from src.chasing.chasing_simulator import ChasingSimulator
from src.chasing.creature_mover import GreedyCreatureMover
from src.creature.creature import Creature
from src.evolution.initializer import CreatureInitializer, CreatureSpawner
from src.static.characteristics import (
    MAXIMUM_MAX_HEALTH,
    MAXIMUM_MAX_STAMINA,
    STATUS_PREDATOR,
    STATUS_PREY,
)


def creature(
    stamina: int = MAXIMUM_MAX_STAMINA, spawn_range_endpoints: List[int] = None
) -> Creature:
    if spawn_range_endpoints is None:
        spawn_range_endpoints = [0, 0]
    creat = Creature()
    CreatureSpawner.spawn_in_range(
        creat, spawn_range_endpoints[0], spawn_range_endpoints[1]
    )
    CreatureInitializer.init_health(creat, MAXIMUM_MAX_HEALTH)
    CreatureInitializer.init_stamina(creat, stamina)
    CreatureInitializer.init_power(creat, 5)
    # can be replaced with any other mover we want to test
    creat.mover = GreedyCreatureMover()
    return creat


def test_spawn_on_same_spot() -> None:
    predator = creature(spawn_range_endpoints=[0, 0])
    prey = creature(spawn_range_endpoints=[0, 0])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREDATOR

    predator = creature(spawn_range_endpoints=[10, 10])
    prey = creature(spawn_range_endpoints=[10, 10])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREDATOR


def test_exhausted_predator_cant_catch_prey() -> None:
    predator = creature(stamina=0, spawn_range_endpoints=[0, 0])
    prey = creature(spawn_range_endpoints=[10, 10])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREY


def test_cant_catch_creature_with_equal_stamina() -> None:
    predator = creature(stamina=100, spawn_range_endpoints=[0, 0])
    prey = creature(stamina=100, spawn_range_endpoints=[10, 10])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREY


def test_can_catch_very_tired_prey() -> None:
    predator = creature(stamina=100, spawn_range_endpoints=[0, 0])
    prey = creature(stamina=10, spawn_range_endpoints=[10, 10])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREDATOR


def test_very_tired_predator_cant_catch() -> None:
    predator = creature(stamina=10, spawn_range_endpoints=[0, 0])
    prey = creature(stamina=100, spawn_range_endpoints=[10, 10])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREY


def test_cant_catch_prey_when_he_is_too_far() -> None:
    predator = creature(stamina=100, spawn_range_endpoints=[0, 0])
    prey = creature(stamina=0, spawn_range_endpoints=[2000, 2000])

    assert ChasingSimulator(predator, prey).simulate_chase() == STATUS_PREY
