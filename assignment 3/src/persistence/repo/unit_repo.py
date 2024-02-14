from dataclasses import dataclass
from typing import List, Protocol

from src.entities.models import Unit
from src.persistence.dao.unit_dao import UnitDAO


class UnitRepository(Protocol):
    def create_unit(self, name: str) -> Unit:
        raise NotImplementedError

    def get_unit_by_id(self, unit_id: int) -> Unit:
        raise NotImplementedError

    def all_units(self) -> List[Unit]:
        raise NotImplementedError


@dataclass
class DAOUnitRepository(UnitRepository):
    dao: UnitDAO

    def create_unit(self, name: str) -> Unit:
        return self.dao.create_unit(name)

    def get_unit_by_id(self, unit_id: int) -> Unit:
        return self.dao.get_unit_by_id(unit_id)

    def all_units(self) -> List[Unit]:
        return self.dao.get_all_units()  # type: ignore
