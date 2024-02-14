from dataclasses import dataclass
from typing import Protocol

import src.static.movement as mv
from src.creature.creature_characteristics import CreatureCharacteristics


class CreatureMover(Protocol):
    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        pass


class NoMove:
    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        raise RuntimeError("Creature couldn't move")


class GreedyCreatureMover:
    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        return FlyMove(RunMove(WalkMove(CrawlMove(NoMove())))).take_step(
            characteristics, stamina
        )


@dataclass
class FlyMove:
    nextMove: CreatureMover

    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        if (
            characteristics.wings < mv.WINGS_TO_FLY
            or stamina < mv.STAMINA_TO_FLY
            or stamina < mv.STAMINA_USED_BY_FLY
        ):
            return self.nextMove.take_step(characteristics, stamina)

        return -mv.STAMINA_USED_BY_FLY, mv.SPEED_FLY


@dataclass
class RunMove:
    nextMove: CreatureMover

    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        if (
            characteristics.legs < mv.LEGS_TO_RUN
            or stamina < mv.STAMINA_TO_RUN
            or stamina < mv.STAMINA_USED_BY_RUN
        ):
            return self.nextMove.take_step(characteristics, stamina)

        return -mv.STAMINA_USED_BY_RUN, mv.SPEED_RUN


@dataclass
class WalkMove:
    nextMove: CreatureMover

    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        if (
            characteristics.legs < mv.LEGS_TO_WALK
            or stamina < mv.STAMINA_TO_WALK
            or stamina < mv.STAMINA_USED_BY_WALK
        ):
            return self.nextMove.take_step(characteristics, stamina)

        return -mv.STAMINA_USED_BY_WALK, mv.SPEED_WALK


@dataclass
class CrawlMove:
    nextMove: CreatureMover

    def take_step(
        self, characteristics: CreatureCharacteristics, stamina: int
    ) -> (int, int):
        if stamina < mv.STAMINA_TO_CRAWL or stamina < mv.STAMINA_USED_BY_CRAWL:
            return self.nextMove.take_step(characteristics, stamina)

        return -mv.STAMINA_USED_BY_CRAWL, mv.SPEED_CRAWL
