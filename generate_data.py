"""
Generates a synthetic student-spending dataset for the project.

This data is SYNTHETIC (randomly generated with realistic distributions),
not scraped or real student data. It exists so the project has something
to load, query, and analyze end-to-end. Swap data/students_spending.csv
for a real dataset (e.g. a Kaggle "student spending" CSV) any time --
the schema and queries are written to match common versions of that
dataset, so a real file should drop in with minimal changes.
"""
import csv
import random

random.seed(42)

MAJORS = ["Computer Science", "Economics", "Psychology", "Biology", "Mechanical Engineering", "Law", "Design"]
YEARS = [1, 2, 3, 4]
PAYMENT_METHODS = ["Credit/Debit Card", "Cash", "Mobile Payment App"]
GENDERS = ["Male", "Female", "Non-binary"]

N_STUDENTS = 400

FIELDS = [
    "student_id", "age", "gender", "year_in_school", "major",
    "monthly_income", "financial_aid", "tuition", "housing", "food",
    "transportation", "books_supplies", "entertainment", "personal_care",
    "technology", "health_wellness", "miscellaneous", "preferred_payment_method",
]

def gen_row(i):
    year = random.choice(YEARS)
    age = 18 + year + random.randint(0, 2)
    income = round(random.gauss(650, 220), 2)
    income = max(50, income)
    financial_aid = round(random.choice([0, 0, 0, 300, 500, 800, 1200]) * random.uniform(0.8, 1.2), 2)
    tuition = round(random.uniform(150, 900), 2)
    housing = round(random.uniform(150, 600), 2)
    food = round(random.uniform(80, 350), 2)
    transportation = round(random.uniform(15, 120), 2)
    books_supplies = round(random.uniform(10, 150), 2)
    entertainment = round(random.uniform(10, 200), 2)
    personal_care = round(random.uniform(10, 90), 2)
    technology = round(random.uniform(0, 150), 2)
    health_wellness = round(random.uniform(0, 100), 2)
    miscellaneous = round(random.uniform(0, 80), 2)
    return {
        "student_id": i,
        "age": age,
        "gender": random.choice(GENDERS),
        "year_in_school": year,
        "major": random.choice(MAJORS),
        "monthly_income": income,
        "financial_aid": financial_aid,
        "tuition": tuition,
        "housing": housing,
        "food": food,
        "transportation": transportation,
        "books_supplies": books_supplies,
        "entertainment": entertainment,
        "personal_care": personal_care,
        "technology": technology,
        "health_wellness": health_wellness,
        "miscellaneous": miscellaneous,
        "preferred_payment_method": random.choice(PAYMENT_METHODS),
    }

def main():
    with open("data/students_spending.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for i in range(1, N_STUDENTS + 1):
            writer.writerow(gen_row(i))
    print(f"Wrote {N_STUDENTS} rows to data/students_spending.csv")

if __name__ == "__main__":
    main()
