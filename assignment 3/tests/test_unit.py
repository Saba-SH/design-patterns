import pytest

from src.persistence.dao.unit_dao import UnitDAO


def test_get_all_no_units_empty_list(unit_dao: UnitDAO) -> None:
    units = unit_dao.get_all_units()
    assert len(units) == 0


def test_create_unit(unit_dao: UnitDAO) -> None:
    unit_dao.create_unit("unit1")

    units = unit_dao.get_all_units()
    assert len(units) == 1
    assert units[0].name == "unit1"

    unit_dao.create_unit("unit2")

    units = unit_dao.get_all_units()
    assert len(units) == 2


def test_create_unit_raises_error_on_existing_unit(unit_dao: UnitDAO) -> None:
    unit_dao.create_unit("unit1")
    with pytest.raises(ValueError):
        unit_dao.create_unit("unit1")


def test_get_unit_by_id(unit_dao: UnitDAO) -> None:
    unit_dao.create_unit("unit1")
    unit_dao.create_unit("unit2")
    unit_dao.create_unit("unit3")

    unit = unit_dao.get_unit_by_id(1)
    assert unit.name == "unit1"

    unit = unit_dao.get_unit_by_id(3)
    assert unit.name == "unit3"


def test_get_unit_raises_error_on_nonexistent_id(unit_dao: UnitDAO) -> None:
    with pytest.raises(ValueError):
        unit_dao.get_unit_by_id(1)

    unit_dao.create_unit("unit1")

    with pytest.raises(ValueError):
        unit_dao.get_unit_by_id(2)


def test_get_unit_by_name(unit_dao: UnitDAO) -> None:
    unit_dao.create_unit("unit1")
    unit_dao.create_unit("unit2")
    unit_dao.create_unit("unit3")

    unit = unit_dao.get_unit_by_name("unit1")
    assert unit.name == "unit1"

    unit = unit_dao.get_unit_by_name("unit3")
    assert unit.name == "unit3"
