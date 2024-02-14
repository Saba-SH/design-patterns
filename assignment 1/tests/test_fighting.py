import pytest

from src.creature.creature import Creature
from src.creature.creature_characteristics import CreatureCharacteristics
from src.evolution.creature_evolver import RandomCreatureEvolver
from src.fighting.damage_calculator import BasicDamageCalculator
from src.fighting.fighting_simulator import FightingSimulator
from src.static.characteristics import (
    CLAWS_BOOST_OPTIONS,
    MINIMUM_AMOUNT_OF_LEGS,
    MINIMUM_AMOUNT_OF_WINGS,
    MINIMUM_MAX_HEALTH,
    MINIMUM_POWER,
    NO_HEALTH,
    STATUS_PREDATOR,
    STATUS_PREY,
    TEETH_BOOST_OPTIONS,
)


@pytest.fixture
def damage_calculator():
    return BasicDamageCalculator()


def test_take_damage_takes_correct_damage():
    creature = Creature()

    creature.health = MINIMUM_MAX_HEALTH

    creature.take_damage(10)

    assert creature.health == MINIMUM_MAX_HEALTH - 10


def test_health_doesnt_get_below_no_health():
    creature = Creature()

    creature.health = 5

    creature.take_damage(10)

    assert creature.health == NO_HEALTH

    creature.take_damage(10)

    assert creature.health == NO_HEALTH


def test_damage_calculation(damage_calculator):
    creature = Creature()

    creature.power = MINIMUM_POWER
    creature.characteristics.claws_boost = CLAWS_BOOST_OPTIONS[1]
    creature.characteristics.teeth_boost = TEETH_BOOST_OPTIONS[1]

    assert (
        damage_calculator.calculate_damage(creature)
        == MINIMUM_POWER * CLAWS_BOOST_OPTIONS[1] + TEETH_BOOST_OPTIONS[1]
    )


def test_dead_predator_loses(damage_calculator):
    predator = Creature()
    prey = Creature()

    predator.health = NO_HEALTH
    prey.health = MINIMUM_MAX_HEALTH

    fighting_simulator = FightingSimulator(predator, prey, damage_calculator)

    assert fighting_simulator.simulate_fight() == STATUS_PREY


def test_dead_prey_loses(damage_calculator):
    predator = Creature()
    prey = Creature()

    predator.health = MINIMUM_MAX_HEALTH
    prey.health = NO_HEALTH

    fighting_simulator = FightingSimulator(predator, prey, damage_calculator)

    assert fighting_simulator.simulate_fight() == STATUS_PREDATOR


def test_predator_wins_with_everything_equal(damage_calculator):
    predator = Creature(evolver=RandomCreatureEvolver())
    predator.power = MINIMUM_POWER
    predator.evolve()

    prey = Creature()
    prey.power = predator.power
    prey.characteristics = predator.characteristics

    assert (
        FightingSimulator(predator, prey, damage_calculator).simulate_fight()
        == STATUS_PREDATOR
    )


def test_higher_health_same_stat_predator_wins(damage_calculator):
    predator = Creature(evolver=RandomCreatureEvolver())
    predator.power = MINIMUM_POWER
    predator.evolve()

    prey = Creature()
    prey.power = predator.power
    prey.characteristics = predator.characteristics

    predator.health = MINIMUM_MAX_HEALTH

    prey.health = int(predator.health / 2)

    assert (
        FightingSimulator(predator, prey, damage_calculator).simulate_fight()
        == STATUS_PREDATOR
    )


def test_lower_health_same_stat_predator_loses(damage_calculator):
    class WeakEvolver:
        @classmethod
        def evolve(cls, characteristics: CreatureCharacteristics) -> None:
            characteristics.legs = MINIMUM_AMOUNT_OF_LEGS
            characteristics.wings = MINIMUM_AMOUNT_OF_WINGS
            characteristics.claws_boost = CLAWS_BOOST_OPTIONS[0]
            characteristics.teeth_boost = TEETH_BOOST_OPTIONS[0]

    prey = Creature(evolver=WeakEvolver())
    prey.power = MINIMUM_POWER
    prey.evolve()

    predator = Creature()
    predator.power = prey.power
    predator.characteristics = prey.characteristics

    prey.health = MINIMUM_MAX_HEALTH

    predator.health = prey.health - int(prey.health / 2)

    assert (
        FightingSimulator(predator, prey, damage_calculator).simulate_fight()
        == STATUS_PREY
    )
