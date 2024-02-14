CREATE TABLE units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_id TEXT,
    name TEXT,
    barcode TEXT,
    price REAL
);

CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT,
    total REAL
);

-- many-to-many
CREATE TABLE products_in_receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    total REAL,
    FOREIGN KEY (receipt_id) REFERENCES receipts (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE sale_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    n_receipts INTEGER,
    revenue REAL
);
