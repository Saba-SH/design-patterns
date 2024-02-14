import pytest

import src.static.movement as mv
from src.chasing.creature_mover import GreedyCreatureMover
from src.creature.creature import Creature
from src.creature.creature_status import CreatureStatus
from src.evolution.initializer import CreatureInitializer, CreatureSpawner
from src.static.characteristics import (
    MAXIMUM_MAX_HEALTH,
    MAXIMUM_MAX_STAMINA,
    STATUS_PREY,
)


@pytest.fixture
def creature() -> Creature:
    creature = Creature()
    CreatureSpawner.spawn_in_range(creature, 0, 0)
    CreatureInitializer.init_health(creature, MAXIMUM_MAX_HEALTH)
    CreatureInitializer.init_stamina(creature, MAXIMUM_MAX_STAMINA)
    CreatureInitializer.init_status(creature, CreatureStatus(status_id=STATUS_PREY))
    CreatureInitializer.init_power(creature, 5)
    # can be replaced with any other mover we want to test
    creature.mover = GreedyCreatureMover()
    return creature


def test_creature_moves_while_has_stamina(creature) -> None:
    creature.stamina = 100

    i = 0
    while creature.stamina > 0 and i < 20:
        start_loc = creature.location
        creature.move()
        assert creature.location > start_loc
        i += 1


def test_raises_error_on_move_with_no_stamina(creature) -> None:
    creature.stamina = 0

    with pytest.raises(RuntimeError):
        creature.move()


def test_creature_spends_stamina_on_move(creature) -> None:
    creature.stamina = 100

    while creature.stamina > 0:
        start_stamina = creature.stamina
        creature.move()
        assert creature.stamina < start_stamina


def test_speed_is_selected_from_correct_options(creature) -> None:
    creature.stamina = 100

    i = 0
    while creature.stamina > 0 and i < 20:
        start_location = creature.location
        creature.move()
        speed = creature.location - start_location

        assert speed in [
            mv.SPEED_CRAWL,
            mv.SPEED_HOP,
            mv.SPEED_WALK,
            mv.SPEED_RUN,
            mv.SPEED_FLY,
        ]
        i += 1


def test_creature_has_equipment_for_selected_movement(creature) -> None:
    creature.stamina = 100

    i = 0
    while creature.stamina > 0 and i < 20:
        start_location = creature.location
        creature.move()
        speed = creature.location - start_location

        if speed == mv.SPEED_HOP:
            assert creature.characteristics.legs >= mv.LEGS_TO_HOP
        elif speed == mv.SPEED_WALK:
            assert creature.characteristics.legs >= mv.LEGS_TO_WALK
        elif speed == mv.SPEED_RUN:
            assert creature.characteristics.legs >= mv.LEGS_TO_RUN
        elif speed == mv.SPEED_FLY:
            assert creature.characteristics.wings >= mv.WINGS_TO_FLY
        i += 1


def test_speed_and_stamina_usage_matches_required_stamina(creature) -> None:
    creature.stamina = 100

    i = 0
    while creature.stamina > 0 and i < 20:
        start_location = creature.location
        start_stamina = creature.stamina
        creature.move()
        speed = creature.location - start_location
        stamina_spent = start_stamina - creature.stamina

        if speed == mv.SPEED_FLY:
            assert (
                stamina_spent == mv.STAMINA_USED_BY_FLY
                and start_stamina >= mv.STAMINA_TO_FLY
            )
        elif speed == mv.SPEED_RUN:
            assert (
                stamina_spent == mv.STAMINA_USED_BY_RUN
                and start_stamina >= mv.STAMINA_TO_RUN
            )
        elif speed == mv.SPEED_WALK:
            assert (
                stamina_spent == mv.STAMINA_USED_BY_WALK
                and start_stamina >= mv.STAMINA_TO_WALK
            )
        elif speed == mv.SPEED_HOP:
            assert (
                stamina_spent == mv.STAMINA_USED_BY_HOP
                and start_stamina >= mv.STAMINA_TO_HOP
            )
        elif speed == mv.SPEED_CRAWL:
            assert (
                stamina_spent == mv.STAMINA_USED_BY_CRAWL
                and start_stamina >= mv.STAMINA_TO_CRAWL
            )

        i += 1
