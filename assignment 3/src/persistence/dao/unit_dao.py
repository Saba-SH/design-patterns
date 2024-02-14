from dataclasses import dataclass
from sqlite3 import Connection
from typing import List, Protocol

from src.entities.models import Unit


class UnitDAO(Protocol):
    def create_unit(self, name: str) -> Unit:
        raise NotImplementedError

    def get_unit_by_id(self, unit_id: int) -> Unit:
        raise NotImplementedError

    def get_unit_by_name(self, unit_name: str) -> Unit:
        raise NotImplementedError

    def get_all_units(self) -> List[Unit]:
        raise NotImplementedError


@dataclass
class SqliteUnitDAO(UnitDAO):
    connection: Connection

    def create_unit(self, name: str) -> Unit:
        error_msg_on_exist = f"Unit with name<{name}> already exists."
        try:
            self.get_unit_by_name(name)
            raise ValueError(error_msg_on_exist)
        except ValueError as e:
            if str(e) == error_msg_on_exist:
                raise

            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO units (name) VALUES (?)", (name,))
            self.connection.commit()

            return self.get_unit_by_name(name)

    def get_unit_by_id(self, unit_id: int) -> Unit:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM units WHERE id = ?", (unit_id,))
        row = cursor.fetchone()
        if row:
            return Unit(id=row[0], name=row[1])
        else:
            raise ValueError(f"Unit with id<{unit_id}> does not exist")

    def get_unit_by_name(self, unit_name: str) -> Unit:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM units WHERE name = ?", (unit_name,))
        row = cursor.fetchone()
        if row:
            return Unit(id=row[0], name=row[1])
        else:
            raise ValueError(f"Unit with name<{unit_name}> does not exist")

    def get_all_units(self) -> List[Unit]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM units")
        rows = cursor.fetchall()
        return [Unit(id=row[0], name=row[1]) for row in rows]
