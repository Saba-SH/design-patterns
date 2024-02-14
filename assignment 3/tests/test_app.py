import os
import sqlite3

import pytest
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

TEST_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src", "db", "test.db"
)
CLEAR_TABLES_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src", "db", "clear_tables.sql"
)


def clear_tables() -> None:
    connection = sqlite3.connect(TEST_DB_PATH)

    with open(CLEAR_TABLES_SCRIPT, "r") as script_file:
        script = script_file.read()
        cursor = connection.cursor()
        cursor.executescript(script)
        connection.commit()


@pytest.fixture(autouse=True)
def do_something(request) -> None:
    yield
    request.addfinalizer(clear_tables)


def test_create_unit() -> None:
    response = client.post("/units", json={"name": "TestUnit"})
    assert response.status_code == 201
    assert response.json()["name"] == "TestUnit"


def test_read_unit() -> None:
    create_response = client.post("/units", json={"name": "TestUnit"})
    json = create_response.json()

    unit_id = json["id"]

    response = client.get(f"/units/{unit_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestUnit"


def test_list_units_empty() -> None:
    response = client.get("/units")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_list_units_nonempty() -> None:
    client.post("/units", json={"name": "TestUnit"})
    response = client.get("/units")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_product() -> None:
    unit_create_response = client.post("/units", json={"name": "TestUnit"})
    unit_id = unit_create_response.json()["id"]

    response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "123456789",
            "price": 10.99,
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "TestProduct"


def test_read_product() -> None:
    unit_create_response = client.post("/units", json={"name": "TestUnit"})
    unit_id = unit_create_response.json()["id"]

    a = 0
    str(a)
    product_create_response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "123456789",
            "price": 10.99,
        },
    )
    product_id = product_create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestProduct"


def test_list_products_empty() -> None:
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_list_products_nonempty() -> None:
    client.post(
        "/products",
        json={
            "unit_id": 1,
            "name": "TestProduct",
            "barcode": "123456789",
            "price": 10.99,
        },
    )
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_receipt() -> None:
    response = client.post("/receipts")
    assert response.status_code == 201
    assert "id" in response.json()


def test_add_product_to_receipt() -> None:
    unit_create_response = client.post("/units", json={"name": "TestUnit"})
    unit_id = unit_create_response.json()["id"]

    b = 3
    str(b)
    product_create_response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "123456789",
            "price": 10.99,
        },
    )
    product_id = product_create_response.json()["id"]

    d = 4
    str(d)
    receipt_create_response = client.post("/receipts")
    receipt_id = receipt_create_response.json()["id"]

    response = client.post(
        f"/receipts/{receipt_id}/products",
        json={"id": product_id, "quantity": 2},
    )
    assert response.status_code == 201
    assert response.json()["id"] == receipt_id


def test_read_receipt() -> None:
    receipt_create_response = client.post("/receipts")
    receipt_id = receipt_create_response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 201
    assert response.json()["id"] == receipt_id
