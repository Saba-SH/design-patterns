from random import randint

from src.creature.creature import Creature
from src.creature.creature_status import CreatureStatus


class CreatureSpawner:
    @classmethod
    def spawn_in_range(cls, creature: Creature, range_start: int, range_end: int):
        creature.location = randint(range_start, range_end)


class CreatureInitializer:
    @classmethod
    def init_health(cls, creature: Creature, health: int):
        creature.health = health

    @classmethod
    def init_stamina(cls, creature: Creature, stamina: int):
        creature.stamina = stamina

    @classmethod
    def init_status(cls, creature: Creature, status: CreatureStatus):
        creature.status = status

    @classmethod
    def init_power(cls, creature: Creature, power: int):
        creature.power = power
