import os
import sqlite3
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from src.entities.models import Product, Receipt, SaleReport, Unit
from src.persistence.dao.product_dao import SqliteProductDAO
from src.persistence.dao.receipt_dao import SqliteReceiptDAO
from src.persistence.dao.sales_dao import SqliteSalesDAO
from src.persistence.dao.unit_dao import SqliteUnitDAO
from src.persistence.repo.big_repo import POSRepository
from src.persistence.repo.product_repo import DAOProductRepository
from src.persistence.repo.receipt_repo import DAOReceiptRepository
from src.persistence.repo.sales_repo import DAOSalesRepository
from src.persistence.repo.unit_repo import DAOUnitRepository

SOURCE_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "src", "db", "pos.db"
)

TEST_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "src", "db", "test.db"
)

db_path = TEST_DB_PATH

app = FastAPI()


def get_db() -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def get_repository(connection: sqlite3.Connection = Depends(get_db)) -> POSRepository:
    return POSRepository(
        DAOUnitRepository(SqliteUnitDAO(connection)),
        DAOProductRepository(SqliteProductDAO(connection)),
        DAOReceiptRepository(SqliteReceiptDAO(connection)),
        DAOSalesRepository(SqliteSalesDAO(connection)),
    )


# Routes for managing units
@app.post("/units", response_model=Unit, status_code=201)
def create_unit(
    unit_json: dict, repository: POSRepository = Depends(get_repository)
) -> Unit:
    try:
        unit_json["name"]
    except KeyError:
        raise HTTPException(status_code=400, detail="The 'name' field is required.")

    try:
        return repository.unit_repository.create_unit(unit_json["name"])
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/units/{unit_id}", response_model=Unit, status_code=200)
def read_unit(
    unit_id: str, repository: POSRepository = Depends(get_repository)
) -> Unit:
    try:
        return repository.unit_repository.get_unit_by_id(int(unit_id))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/units", response_model=List[Unit], status_code=200)
def list_units(repository: POSRepository = Depends(get_repository)) -> List[Unit]:
    return repository.unit_repository.all_units()


# Routes for managing products
@app.post("/products", response_model=Product, status_code=201)
def create_product(
    product_json: dict, repository: POSRepository = Depends(get_repository)
) -> Product:
    try:
        return repository.product_repository.create_product(
            product_json["unit_id"],
            product_json["name"],
            product_json["barcode"],
            product_json["price"],
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/products/{product_id}", response_model=Product, status_code=200)
def read_product(
    product_id: str, repository: POSRepository = Depends(get_repository)
) -> Product:
    try:
        return repository.product_repository.get_product_by_id(int(product_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/products", response_model=List[Product], status_code=200)
def list_products(repository: POSRepository = Depends(get_repository)) -> List[Product]:
    return repository.product_repository.get_all_products()


@app.patch("/products/{product_id}", response_model=Product, status_code=200)
def update_product(
    product_id: str,
    updated_fields: dict,
    repository: POSRepository = Depends(get_repository),
) -> dict:
    try:
        repository.product_repository.update_product(
            Product(
                id=product_id,
                unit_id=None,
                name=None,
                barcode=None,
                price=float(updated_fields["price"]),
            )
        )
        return dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Routes for managing receipts
@app.post("/receipts", response_model=Receipt, status_code=201)
def create_receipt(repository: POSRepository = Depends(get_repository)) -> Receipt:
    return repository.receipt_repository.create_receipt()


@app.post("/receipts/{receipt_id}/products", response_model=Receipt, status_code=201)
def add_product_to_receipt(
    receipt_id: str,
    product_dict: dict,
    repository: POSRepository = Depends(get_repository),
) -> Receipt:
    return repository.receipt_repository.add_product_to_receipt(
        int(receipt_id),
        repository.product_repository.get_product_by_id(int(product_dict["id"])),
        int(product_dict["quantity"]),
    )


@app.get("/receipts/{receipt_id}", response_model=Receipt, status_code=201)
def read_receipt(
    receipt_id: str, repository: POSRepository = Depends(get_repository)
) -> Receipt:
    try:
        return repository.receipt_repository.get_receipt_by_id(int(receipt_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/receipts/{receipt_id}", response_model=Receipt, status_code=200)
def close_receipt(
    receipt_id: str,
    status_update: dict,
    repository: POSRepository = Depends(get_repository),
) -> dict:
    try:
        repository.receipt_repository.close_receipt(int(receipt_id))
        repository.sales_repository.add_sale(
            sum(
                p.total
                for p in repository.receipt_repository.get_receipt_by_id(
                    int(receipt_id)
                ).products
            )
        )
        return dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/receipts/{receipt_id}", response_model=dict)
def delete_receipt(
    receipt_id: str, repository: POSRepository = Depends(get_repository)
) -> dict:
    try:
        repository.receipt_repository.delete_receipt(int(receipt_id))
        return dict()
    except AssertionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/sales", response_model=SaleReport)
def generate_sales_report(
    repository: POSRepository = Depends(get_repository),
) -> SaleReport:
    return repository.sales_repository.generate_sales_report()
