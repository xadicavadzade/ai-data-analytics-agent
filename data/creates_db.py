import sqlite3

conn = sqlite3.connect("data/sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    sale_date TEXT NOT NULL
)
""")

rows = [
    ("Laptop", "Electronics", 2, 1200, "2026-01-10"),
    ("Laptop", "Electronics", 1, 1200, "2026-01-15"),
    ("Mouse", "Electronics", 10, 25, "2026-01-18"),
    ("Keyboard", "Electronics", 5, 60, "2026-01-20"),
    ("Chair", "Furniture", 4, 180, "2026-02-01"),
    ("Desk", "Furniture", 2, 350, "2026-02-05"),
    ("Monitor", "Electronics", 3, 300, "2026-02-08"),
    ("Phone", "Electronics", 7, 900, "2026-02-10"),
    ("Notebook", "Stationery", 20, 5, "2026-02-12"),
    ("Pen", "Stationery", 50, 2, "2026-02-15"),
    ("Tablet", "Electronics", 3, 700, "2026-03-01"),
    ("Printer", "Electronics", 2, 250, "2026-03-05"),
    ("Lamp", "Furniture", 6, 40, "2026-03-07"),
    ("Headphones", "Electronics", 8, 120, "2026-03-09"),
    ("Book", "Stationery", 15, 18, "2026-03-10"),
]

cursor.executemany(
    """
    INSERT INTO sales
    (product, category, quantity, price, sale_date)
    VALUES (?, ?, ?, ?, ?)
    """,
    rows,
)

conn.commit()
conn.close()

print("sales.db created successfully!")