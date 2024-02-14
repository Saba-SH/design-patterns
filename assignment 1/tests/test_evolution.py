import src.static.characteristics as chars
from src.creature.creature import Creature
from src.creature.creature_characteristics import CreatureCharacteristics
from src.creature.creature_status import CreatureStatus
from src.evolution.creature_evolver import CreatureEvolver, RandomCreatureEvolver
from src.evolution.initializer import CreatureInitializer, CreatureSpawner
from src.static.movement import LEGS_TO_RUN, WINGS_TO_FLY


def test_spawn_in_range_falls_in_range() -> None:
    creature = Creature(CreatureCharacteristics())

    range_start = 0
    range_end = 10
    CreatureSpawner.spawn_in_range(creature, range_start, range_end)
    assert creature.location in range(range_start, range_end + 1)


def test_spawn_in_range_on_spot() -> None:
    creature = Creature()

    spot = 0
    CreatureSpawner.spawn_in_range(creature, spot, spot)
    assert creature.location == spot

    spot = 10
    CreatureSpawner.spawn_in_range(creature, spot, spot)
    assert creature.location == spot


def test_init_health() -> None:
    creature = Creature()

    CreatureInitializer.init_health(creature, chars.MAXIMUM_MAX_HEALTH)

    assert creature.health == chars.MAXIMUM_MAX_HEALTH


def test_init_stamina() -> None:
    creature = Creature()

    CreatureInitializer.init_stamina(creature, chars.MAXIMUM_MAX_STAMINA)

    assert creature.stamina == chars.MAXIMUM_MAX_STAMINA


def test_init_status_inits_id_correctly() -> None:
    status = CreatureStatus(status_id=chars.STATUS_PREY)
    creature = Creature()

    CreatureInitializer.init_status(creature, status)
    assert creature.status.status_id == chars.STATUS_PREY

    status = CreatureStatus(status_id=chars.STATUS_PREDATOR)
    creature = Creature()

    CreatureInitializer.init_status(creature, status)
    assert creature.status.status_id == chars.STATUS_PREDATOR


def test_init_power() -> None:
    creature = Creature()

    CreatureInitializer.init_power(creature, chars.MAXIMUM_POWER)

    assert creature.power == chars.MAXIMUM_POWER


def test_random_evolve_selects_correct_values() -> None:
    creature = Creature()
    creature.evolver = RandomCreatureEvolver()

    creature.evolve()

    assert creature.characteristics.legs in range(
        chars.MINIMUM_AMOUNT_OF_LEGS, LEGS_TO_RUN + 1
    )
    assert creature.characteristics.wings in range(
        chars.MINIMUM_AMOUNT_OF_WINGS, WINGS_TO_FLY + 1
    )
    assert creature.characteristics.claws_boost in chars.CLAWS_BOOST_OPTIONS
    assert creature.characteristics.teeth_boost in chars.TEETH_BOOST_OPTIONS


def test_custom_evolve_strategy() -> None:
    creature = Creature()

    class StrongEvolver(CreatureEvolver):
        @classmethod
        def evolve(cls, characteristics: CreatureCharacteristics) -> None:
            characteristics.legs = LEGS_TO_RUN
            characteristics.wings = WINGS_TO_FLY
            characteristics.claws_boost = chars.CLAWS_BOOST_OPTIONS[-1]
            characteristics.teeth_boost = chars.TEETH_BOOST_OPTIONS[-1]

    creature.evolver = StrongEvolver
    creature.evolve()

    assert creature.characteristics.legs == LEGS_TO_RUN
    assert creature.characteristics.wings == WINGS_TO_FLY
    assert creature.characteristics.claws_boost == chars.CLAWS_BOOST_OPTIONS[-1]
    assert creature.characteristics.teeth_boost == chars.TEETH_BOOST_OPTIONS[-1]
