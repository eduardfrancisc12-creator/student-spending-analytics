"""
ETL: loads data/students_spending.csv into a local SQLite database
(student_spending.db) using the schema in schema.sql.

Usage:
    python etl.py
"""
import csv
import sqlite3
from pathlib import Path

DB_PATH = Path("student_spending.db")
SCHEMA_PATH = Path("schema.sql")
CSV_PATH = Path("data/students_spending.csv")


def build_database(db_path: Path = DB_PATH) -> None:
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        with open(SCHEMA_PATH) as f:
            conn.executescript(f.read())

        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            rows = [tuple(row.values()) for row in reader]
            columns = next(csv.reader(open(CSV_PATH))).__len__()
            placeholders = ",".join(["?"] * columns)
            conn.executemany(f"INSERT INTO spending VALUES ({placeholders})", rows)

        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM spending").fetchone()[0]
        print(f"Loaded {count} rows into {db_path}")
    finally:
        conn.close()


if __name__ == "__main__":
    build_database()
