from src.persistence.dao.sales_dao import SalesDAO


def test_generate_sales_report_empty_table(sales_dao: SalesDAO) -> None:
    sales_report = sales_dao.generate_sales_report()

    assert sales_report.n_receipts == 0
    assert sales_report.revenue == 0.0


def test_add_one_sale_and_generate_sales_report(sales_dao: SalesDAO) -> None:
    sales_dao.add_sale(100.0)
    sales_report = sales_dao.generate_sales_report()

    assert sales_report.n_receipts == 1
    assert sales_report.revenue == 100.0


def test_add_many_sales_and_generate_sales_report(sales_dao: SalesDAO) -> None:
    sales_dao.add_sale(10.0)
    sales_report = sales_dao.generate_sales_report()

    assert sales_report.n_receipts == 1
    assert sales_report.revenue == 10.0

    sales_dao.add_sale(12.0)
    sales_dao.add_sale(20.0)
    sales_dao.add_sale(12.50)
    sales_dao.add_sale(9.99)

    sales_report = sales_dao.generate_sales_report()

    assert sales_report.n_receipts == 5
    assert sales_report.revenue == 10.0 + 12.0 + 20.0 + 12.50 + 9.99
