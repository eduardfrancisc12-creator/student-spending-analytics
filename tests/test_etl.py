import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl import build_database, DB_PATH  # noqa: E402


def test_build_database_creates_expected_row_count(tmp_path):
    test_db = tmp_path / "test.db"
    build_database(test_db)

    conn = sqlite3.connect(test_db)
    try:
        count = conn.execute("SELECT COUNT(*) FROM spending").fetchone()[0]
        assert count == 400
    finally:
        conn.close()


def test_build_database_has_expected_columns(tmp_path):
    test_db = tmp_path / "test.db"
    build_database(test_db)

    conn = sqlite3.connect(test_db)
    try:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(spending)")]
        assert "student_id" in cols
        assert "monthly_income" in cols
        assert "major" in cols
    finally:
        conn.close()


def test_no_negative_spending_values(tmp_path):
    test_db = tmp_path / "test.db"
    build_database(test_db)

    conn = sqlite3.connect(test_db)
    try:
        row = conn.execute(
            "SELECT COUNT(*) FROM spending WHERE housing < 0 OR food < 0 OR tuition < 0"
        ).fetchone()
        assert row[0] == 0
    finally:
        conn.close()
