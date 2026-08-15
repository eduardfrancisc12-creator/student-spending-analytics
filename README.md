# Student Spending Analytics

A small end-to-end data project: raw CSV → SQLite database → SQL analysis → charts + a written report. Built as a portfolio piece to practice the same skills covered in the Databases and Probability & Statistics coursework.

## What it does

1. `generate_data.py` — generates a synthetic dataset of 400 students' monthly income, financial aid, and spending across 9 categories (housing, food, transportation, etc). The data is randomly generated with realistic distributions, not scraped or real — see the file for details. Swap in a real dataset with the same columns and everything downstream still works.
2. `etl.py` — loads the CSV into a local SQLite database (`student_spending.db`) using the schema in `schema.sql`.
3. `queries.sql` — five SQL queries answering concrete questions: spending by major, income vs. financial aid, category breakdown as % of total spend, students at deficit risk, and payment method preferences by year.
4. `analysis.py` — runs the queries with pandas, saves two charts (`reports/spending_by_major.png`, `reports/category_breakdown.png`), and writes a short findings summary to `reports/report.md`.
5. `tests/test_etl.py` — pytest tests that check the database builds correctly and the data is sane (no negative spending values, expected row count, expected columns).
6. `.github/workflows/ci.yml` — GitHub Actions workflow that runs the whole pipeline (build DB → test → analyze) on every push, so the badge below actually means something.

## Running it locally

```bash
pip install -r requirements.txt
python etl.py          # builds student_spending.db from data/students_spending.csv
python analysis.py     # runs the queries, writes charts + reports/report.md
pytest -v               # runs the test suite
```

## Sample output

See [`reports/report.md`](reports/report.md) for the generated findings and charts.

## Why this project

Databases and SQL are the most directly useful, most immediately monetizable skills in a Year 2 AI curriculum — this project is meant to be a concrete, verifiable example of that: a real (if small) pipeline with tests and CI, not just a notebook. Next planned addition: a second dataset variant with time-series data (monthly trends) to practice window functions.

## License

MIT — feel free to fork and adapt.
