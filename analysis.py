"""
Runs the queries in queries.sql against student_spending.db, prints results,
saves two charts to reports/, and writes a short markdown summary to
reports/report.md.

Usage:
    python etl.py        # build the DB first
    python analysis.py
"""
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DB_PATH = Path("student_spending.db")
REPORTS_DIR = Path("reports")

SPEND_COLS = [
    "housing", "food", "transportation", "books_supplies",
    "entertainment", "personal_care", "technology", "health_wellness", "miscellaneous",
]


def load_df(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM spending", conn)


def chart_spending_by_major(df: pd.DataFrame) -> Path:
    df = df.copy()
    df["total_spending"] = df[SPEND_COLS].sum(axis=1)
    by_major = df.groupby("major")["total_spending"].mean().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    by_major.plot(kind="barh", ax=ax, color="#5b8cff")
    ax.set_xlabel("Average total monthly spending ($)")
    ax.set_ylabel("")
    ax.set_title("Average monthly spending by major")
    fig.tight_layout()

    out = REPORTS_DIR / "spending_by_major.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def chart_category_breakdown(df: pd.DataFrame) -> Path:
    totals = df[SPEND_COLS].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(totals, labels=totals.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Spending category breakdown (all students)")
    fig.tight_layout()

    out = REPORTS_DIR / "category_breakdown.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def write_report(df: pd.DataFrame, chart_paths: list[Path]) -> Path:
    df = df.copy()
    df["total_spending"] = df[SPEND_COLS].sum(axis=1)
    df["total_inflow"] = df["monthly_income"] + df["financial_aid"]
    deficit = df[df["total_spending"] > df["total_inflow"]]

    lines = [
        "# Student Spending Analysis — Report",
        "",
        f"Dataset: {len(df)} students (synthetic data, see `generate_data.py`).",
        "",
        "## Key findings",
        "",
        f"- Average total monthly spending across all students: **${df['total_spending'].mean():.2f}**",
        f"- {len(deficit)} students ({100 * len(deficit) / len(df):.1f}%) spend more than their income + aid.",
        f"- Highest-spending major: **{df.groupby('major')['total_spending'].mean().idxmax()}**",
        f"- Lowest-spending major: **{df.groupby('major')['total_spending'].mean().idxmin()}**",
        "",
        "## Charts",
        "",
    ]
    for p in chart_paths:
        lines.append(f"![{p.stem}]({p.name})")
        lines.append("")

    out = REPORTS_DIR / "report.md"
    out.write_text("\n".join(lines))
    return out


def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        df = load_df(conn)
    finally:
        conn.close()

    charts = [chart_spending_by_major(df), chart_category_breakdown(df)]
    report = write_report(df, charts)
    print(f"Report written to {report}")
    for c in charts:
        print(f"Chart saved: {c}")


if __name__ == "__main__":
    main()
